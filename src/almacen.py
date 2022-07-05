import time
import datetime as dt
import pandas as pd
import os
import re

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from tkinter import messagebox
import sys
import os

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath('AppScraping'))

class AlmacenElements:
    content = (By.CSS_SELECTOR, "body > div:nth-child(19)")
    body = (By.CSS_SELECTOR, "#main-menu-navigation > li:nth-child(5) > a > i > div > svg > g > g > g > g > g > path:nth-child(2)")

    search = (By.CSS_SELECTOR,
            "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
class Almacen:
    browser = None
    size = 0
    timeout = 560  # The timeout is set for about ten seconds

    def __init__(self, wait, screenshot=None, session=None):
        if self.browser is None:
            try:
                self.browser = webdriver.Chrome(
                    executable_path="chromedriver.exe")  # change path
                # to open the WhatsApp web
                self.browser.get("http://mundonegocio.org/")

                # you need to scan the QR code in here (to eliminate this step, I will publish another blog

                WebDriverWait(self.browser, wait).until(
                    EC.presence_of_element_located(AlmacenElements.content))  # wait till search element appears
            except Exception as e:
                WebDriverWait(self.browser, 560)
                messagebox.showwarning(
                    message="Ups, no se pudo tener conexión con el sistema de almacén", title="Iniciar Almacén")
                print(e)
        else:
            WebDriverWait(self.browser, 560)
            messagebox.showwarning(
                message="Reconectando...", title="Iniciar WhatsApp")

    def goto_main(self):
        try:
            attach_button_xpath = '/html/body/div[3]/div/div[3]/button[1]'
            attach_button = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(attach_button_xpath))

            time.sleep(1)
            attach_button.click()

            Alert(self.browser).accept()

        except Exception as e:
            print(e)
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                AlmacenElements.content))

    def send_campaña(self):
        self.goto_main()

        ########## IMPORTANDO ARCHIVOS EXCEL CONTACTOS Y LLAVES ##########
        usuarios = pd.ExcelFile(
            r'{}\assets\files\maestros\UsuariosAlmacen.xlsx'.format(application_path)).parse(0)

        print('Importado', usuarios.shape[1], 'numeros de celular')

        """""
        x = contactos.shape[0]
        contactos = contactos.drop_duplicates()
        y = contactos.shape[0]
        z = x - y
        print(z, 'duplicados encontrados y removidos')
        """""
        # REMOVER ESPACIOS
        def espacios(texto):
            texto = re.sub(r'[\s]+', '', texto)
            return texto

        usuarios['ID'] = usuarios['ID'].astype(str).apply(espacios)

        usuarios['Celular'] = usuarios['ID'].astype(str)

        a = 0
        df = pd.DataFrame(columns=['ID', 'TIPO DOCUMENTO', 'NUMERO DE DOCUMENTO', '¿ES PROSPECTO?', 'NOMBRES', 'APELLIDO PATERNO', 'APELLIDO MATERNO',
                            'E-MAIL', 'TELÉFONO 1', 'TELÉFONO 2', 'ESTADO', 'UBIGEO', 'DIRECCIÓN', 'URBANIZACIÓN', 'NÚMERO EXTERIOR', 'NÚMERO INTERIOR', 'REFERENCIA'])

        cel = usuarios['ID']

        for i in cel:
            print('-----------------------------------------------')
            print('Obteniendo registros de #', i)

            a = a + 1
            df.at[a, 'ID'] = i

            print('Cantidad: ', a)
            try:
                link = 'http://mundonegocio.org/clientes/detalle/' + i
                self.browser.get(link)

                WebDriverWait(self.browser, 560).until(
                    EC.presence_of_element_located(AlmacenElements.body))  # wait till search element appears

                type_doc_xpath = '//*[@id="select2-selDocumentType-container"]'
                type_doc = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(type_doc_xpath))
                type_doc_value = type_doc.get_attribute('title')

                df.at[a, 'TIPO DOCUMENTO'] = type_doc_value

                documento_xpath = '//*[@id="txtDocument"]'
                documento = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(documento_xpath))
                documento_value = documento.get_attribute('value')

                df.at[a, 'NUMERO DE DOCUMENTO'] = documento_value

                prospecto_xpath = '//*[@id="txtLeaflet"]'
                prospecto = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(prospecto_xpath))
                prospecto_value = prospecto.get_attribute('value')

                df.at[a, '¿ES PROSPECTO?'] = prospecto_value

                nombres_xpath = '//*[@id="txtName"]'
                nombres = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(nombres_xpath))
                nombres_value = nombres.get_attribute('value')

                df.at[a, 'NOMBRES'] = nombres_value

                apellido_paterno_xpath = '//*[@id="txtFatherLastName"]'
                apellido_paterno = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(apellido_paterno_xpath))
                apellido_paterno_value = apellido_paterno.get_attribute('value')

                df.at[a, 'APELLIDO PATERNO'] = apellido_paterno_value

                apellido_materno_xpath = '//*[@id="txtMotherLastName"]'
                apellido_materno = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(apellido_materno_xpath))
                apellido_materno_value = apellido_materno.get_attribute('value')

                df.at[a, 'APELLIDO MATERNO'] = apellido_materno_value

                email_xpath = '//*[@id="txtEmail"]'
                email = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(email_xpath))
                email_value = email.get_attribute('value')

                df.at[a, 'E-MAIL'] = email_value

                phone1_xpath = '//*[@id="txtPhone1"]'
                phone1 = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(phone1_xpath))
                phone1_value = phone1.get_attribute('value')

                df.at[a, 'TELÉFONO 1'] = phone1_value

                phone2_xpath = '//*[@id="txtPhone2"]'
                phone2 = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(phone2_xpath))
                phone2_value = phone2.get_attribute('value')

                df.at[a, 'TELÉFONO 2'] = phone2_value

                estado_xpath = '//*[@id="select2-selState-container"]'
                estado = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(estado_xpath))
                estado_value = estado.get_attribute('title')

                df.at[a, 'ESTADO'] = estado_value


                ubigeo_xpath = '//*[@id="txtUbigeoID"]'
                ubigeo = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(ubigeo_xpath))
                ubigeo_value = ubigeo.get_attribute('value')

                df.at[a, 'UBIGEO'] = ubigeo_value

                direccion_xpath = '//*[@id="txtAddress"]'
                direccion = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(direccion_xpath))
                direccion_value = direccion.get_attribute('value')

                df.at[a, 'DIRECCIÓN'] = direccion_value

                urbanizacion_xpath = '//*[@id="txtUrbanization"]'
                urbanizacion = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(urbanizacion_xpath))
                urbanizacion_value = urbanizacion.get_attribute('value')

                df.at[a, 'URBANIZACIÓN'] = urbanizacion_value

                numero_exterior_xpath = '//*[@id="txtNumber"]'
                numero_exterior = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(numero_exterior_xpath))
                numero_exterior_value = numero_exterior.get_attribute('value')

                df.at[a, 'NÚMERO EXTERIOR'] = numero_exterior_value

                numero_interior_xpath = '//*[@id="txtInside"]'
                numero_interior = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(numero_interior_xpath))
                numero_interior_value = numero_interior.get_attribute('value')

                df.at[a, 'NÚMERO INTERIOR'] = numero_interior_value

                referencia_xpath = '//*[@id="txtReference"]'
                referencia = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(referencia_xpath))
                referencia_value = referencia.get_attribute('value')

                df.at[a, 'REFERENCIA'] = referencia_value


#select2-selDocumentType-container
#txtDocument
#txtLeaflet
#txtName
#txtFatherLastName
#txtMotherLastName
#txtEmail
#txtPhone1
#txtPhone2
#select2-selState-container
#txtUbigeoID
#txtAddress
#txtUrbanization
#txtNumber
#txtInside
#txtReference

            except Exception as e:
                WebDriverWait(self.browser, 560)
                messagebox.showwarning(message="Ups, no se pudo tener conexión con el sistema de almacén", title="Iniciar Almacén")
                print("Este numero no tienen WhatsApp: +{}".format(i))


        messagebox.showinfo(
            message="Registros obtenidos... Exportando reporte", title="Registros")

        now = dt.datetime.now()
        FFH = now.strftime("%Y%m%d_%H%M")
        nombre = FFH + '_reporte'

        df.to_excel(r'{}\assets\files\maestros\{}.xlsx'.format(
            application_path, nombre), index=False)

        if messagebox.askyesno(message="¿Desea abrir el archivo?", title="Clientes"):
            os.startfile(r'{}\assets\files\maestros\{}.xlsx'.format(
                application_path, nombre))

        # browser.quit()
        return True
