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


class WhatsAppElements:
    content = (By.CSS_SELECTOR, "#pane-side")
    search = (By.CSS_SELECTOR,
              "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")


class Campaña:
    browser = None
    size = 0
    timeout = 560  # The timeout is set for about ten seconds

    def __init__(self, wait, screenshot=None, session=None):
        if self.browser is None:
            try:
                self.browser = webdriver.Chrome(
                    executable_path="chromedriver.exe")  # change path
                # to open the WhatsApp web
                self.browser.get("https://web.whatsapp.com/")

                # you need to scan the QR code in here (to eliminate this step, I will publish another blog

                WebDriverWait(self.browser, wait).until(
                    EC.presence_of_element_located(WhatsAppElements.content))  # wait till search element appears
            except Exception as e:
                WebDriverWait(self.browser, 560)
                messagebox.showwarning(
                    message="Ups, no se pudo tener conexión con WhatsApp", title="Iniciar WhatsApp")
                print(e)
        else:
            WebDriverWait(self.browser, 560)
            messagebox.showwarning(
                message="Reconectando...", title="Iniciar WhatsApp")

    def goto_main(self):
        try:
            self.browser.refresh()
            Alert(self.browser).accept()

        except Exception as e:
            print(e)
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                WhatsAppElements.content))

    def send_campaña(self):
        self.goto_main()

        ########## IMPORTANDO ARCHIVOS EXCEL CONTACTOS Y LLAVES ##########
        contactos = pd.ExcelFile(
            r'{}\assets\files\maestros\NumerosCampaña.xlsx'.format(application_path)).parse(0)
        llaves = pd.ExcelFile(
            r'{}\assets\files\maestros\Campaña.xlsx'.format(application_path)).parse(0)
        print('Importado', contactos.shape[0], 'numeros de celular')

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

        contactos['Celular'] = contactos['Celular'].astype(str).apply(espacios)

        # OBJETOS LIST
        mensaje = list(llaves.mensaje)
        mensaje = [x for x in mensaje if str(x) != 'nan']

        ruta_imagen = list(llaves.ruta_imagen)
        ruta_imagen = [x for x in ruta_imagen if str(x) != 'nan']

        #mensaje_imagen = list(llaves.mensaje_imagen)
        #mensaje_imagen = [x for x in mensaje_imagen if str(x) != 'nan']

        ruta_video = list(llaves.ruta_video)
        ruta_video = [x for x in ruta_video if str(x) != 'nan']

        mensaje_video = list(llaves.mensaje_video)
        mensaje_video = [x for x in mensaje_video if str(x) != 'nan']

        ruta_documento = list(llaves.ruta_documento)
        ruta_documento = [x for x in ruta_documento if str(x) != 'nan']

        contactos['Celular'] = contactos['Codigo_Pais'].astype(
            str) + contactos['Celular']

        a = 0
        count = 6
        df = pd.DataFrame(columns=['Celular', 'Estado'])

        #message_image = "¡Hola! 🤩 Llegó el CyberWow a Mundo Negocio! Usa el cupón MUNDOWOW y ten S/.50 de descuento en nuestros productos. ¡Vive esta experiencia en Mundo Negocio!🙀 \n¡Tu mejor opción a un solo clic! 👉🏼 www.mundonegocio.com.pe/mundowow 👈🏼 \n🔸Compras seguras. \n🔸Envíos rápidos. \n🔸Mejores precios del mercado. \n🤯¿Necesitas ayuda con tu proceso de compra?😮"

        cel = contactos['Celular']
        for i in cel:
            print('-----------------------------------------------')
            print('Enviando mensaje a: +', i)
            link = 'https://web.whatsapp.com/send?phone='+i

            self.browser.get(link)
            a = a + 1
            df.at[a, 'Celular'] = i

            print('Cantidad: ', a)
            if a == count:
                print("Calma, esperemos 1 minuto y 5 segundos.")
                count = count + 5
                time.sleep(65)

            #search = self.browser.find_element(*WhatsAppElements.search)
            # search.send_keys(i+Keys.ENTER)

            try:
                text = 0
                if ruta_imagen:
                    for k in ruta_imagen:
                        print('Enviando imagen')
                        attach_button_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
                        attach_button = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(attach_button_xpath))

                        time.sleep(1)
                        attach_button.click()

                        image_box_xpath = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
                        image_box = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(image_box_xpath))
                        image_box.send_keys(k)

                        # if llaves['mensaje_imagen'][text] != "nan":

                        #    input_box_image_xpath = '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]'
                        #    input_box_image = WebDriverWait(self.browser, 40).until(
                        #        lambda driver: driver.find_element_by_xpath(input_box_image_xpath))
                        #    ##input_box_image.send_keys(llaves['mensaje_imagen'][text])
                        #    self.browser.execute_script(
                        #        "arguments[0].innerHTML = '{}'".format(llaves['mensaje_imagen'][text]), input_box_image)

                        #    input_box_image.send_keys(".")
                        #    input_box_image.send_keys(Keys.BACKSPACE)

                        time.sleep(1)

                        send_button = WebDriverWait(self.browser, 40).until(lambda driver: driver.find_element_by_xpath(
                            '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div'))
                        send_button.click()

                        time.sleep(1)
                        text = text + 1

                    print('Imagen enviada')
                    df.at[a, 'Estado'] = 'Mensaje enviado satisfactoriamente'

                if ruta_video:
                    text = 0
                    for k in ruta_video:
                        print('Enviando video')
                        attach_button_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div'
                        attach_button = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(attach_button_xpath))

                        time.sleep(1)
                        attach_button.click()

                        image_box_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input'
                        image_box = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(image_box_xpath))
                        image_box.send_keys(k)

                        input_box_image_xpath = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/div[2]'
                        input_box_image = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(input_box_image_xpath))
                        self.browser.execute_script(
                            "arguments[0].innerHTML = '{}'".format(llaves['mensaje_video'][text]), input_box_image)
                        input_box_image.send_keys(".")
                        input_box_image.send_keys(Keys.BACKSPACE)
                        time.sleep(1)

                        send_button = WebDriverWait(self.browser, 40).until(lambda driver: driver.find_element_by_xpath(
                            '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div'))
                        send_button.click()
                        time.sleep(1)

                        text = text + 1

                    print('Video enviado')
                    df.at[a, 'Estado'] = 'Mensaje enviado satisfactoriamente'
                """
                if mensaje:
                    for j in mensaje:
                        print('Escribiendo mensaje: ', j)
                        input_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
                        input_box = WebDriverWait(self.browser, 40).until(
                            lambda driver: driver.find_element_by_xpath(input_xpath))

                        time.sleep(1)

                        # input_box_image.send_keys(llaves['mensaje_imagen'][text])
                        self.browser.execute_script(
                            "arguments[0].innerHTML = '{}'".format(j), input_box)
                        input_box.send_keys(".")
                        input_box.send_keys(Keys.BACKSPACE)
                        input_box.send_keys(Keys.ENTER)

                        time.sleep(1)

                        print('Mensaje enviado')
                        df.at[a, 'Estado'] = 'Mensaje enviado satisfactoriamente'
                """
                if ruta_documento:
                    for k in ruta_documento:
                        print('Enviando documento')
                        attach_button_xpath = '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div'
                        attach_button = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(attach_button_xpath))

                        time.sleep(1)
                        attach_button.click()

                        doc_box_xpath = '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[3]/button'
                        doc_box = WebDriverWait(self.browser, 20).until(
                            lambda driver: driver.find_element_by_xpath(doc_box_xpath))
                        doc_box.send_keys(k)

                        time.sleep(1)

                        send_button = WebDriverWait(self.browser, 40).until(lambda driver: driver.find_element_by_xpath(
                            '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div'))
                        send_button.click()

                        time.sleep(1)

                        print('Documento enviado')
                        df.at[a, 'Estado'] = 'Mensaje enviado satisfactoriamente'

            except:
                print("Este numero no tienen WhatsApp: +{}".format(i))
                # messagebox.showerror(
                #    message="Este numero no tienen WhatsApp: +{}".format(i), title="Campaña")
                df.at[a, 'Estado'] = 'Numero sin WhatsApp'

        messagebox.showinfo(
            message="Campaña enviada... Exportando reporte", title="Campaña")

        now = dt.datetime.now()
        FFH = now.strftime("%Y%m%d_%H%M")
        nombre = FFH + '_reporte'

        df.to_excel(r'{}\assets\files\logs\{}.xlsx'.format(
            application_path, nombre), index=False)

        if messagebox.askyesno(message="¿Desea abrir ultimo log de envio?", title="Campaña"):
            os.startfile(r'{}\assets\files\logs\{}.xlsx'.format(
                application_path, nombre))

        # browser.quit()
        return True
