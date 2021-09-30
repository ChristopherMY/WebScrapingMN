import time
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


class WhatsAppElements:
    search = (By.CSS_SELECTOR,
              "#side > div.uwk68 > div > label > div > div._13NKt.copyable-text.selectable-text")
    aside = (By.CSS_SELECTOR, "#main > header > div._24-Ff > div > div > span")


class WhatsApp:
    browser =  None
    size = 0
    timeout = 15  # The timeout is set for about ten seconds
    def __init__(self, wait, screenshot=None, session=None):
        if self.browser is None:
            try:
                self.browser = webdriver.Chrome(executable_path="chromedriver.exe")# change path
                self.browser.get("https://web.whatsapp.com/") #to open the WhatsApp web

                # you need to scan the QR code in here (to eliminate this step, I will publish another blog

                WebDriverWait(self.browser, wait).until( 
                EC.presence_of_element_located(WhatsAppElements.search)) #wait till search element appears
            except Exception as e:
                WebDriverWait(self.browser, 60)
                messagebox.showwarning(message="Ups, no se pudo tener conexión con WhatsApp", title="Iniciar WhatsApp")
                print(e)
        else:
            WebDriverWait(self.browser, 60)
            messagebox.showwarning(message="Reconectando...", title="Iniciar WhatsApp")

    def goto_main(self):
        try:
            self.browser.refresh()
            Alert(self.browser).accept()

        except Exception as e:
            print(e)
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(
                WhatsAppElements.search))

    def unread_usernames(self, scrolls=100):
        self.goto_main()
        initial = 10
        usernames = []

        e = self.browser.find_element_by_xpath("//*[@id='pane-side']")
        content = e.size
        size = content['height'] + content['width']
        #38432
        #48432
        #28415
        #18415
        for i in range(0, 2600):
            self.browser.execute_script(
                "document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_3OvU8"):  # replace for _1V5O7
                if i.find("div", class_="_3vPI2"):
                    if i.find("div", class_="zoWT4"):
                        if i.find("span", class_="_3q9s6"):
                            username = i.find("span", class_="_ccCW").text
                            usernames.append(username)
            initial += 10
        # Remove duplicates
        usernames = list(set(usernames))
        return usernames

    def get_last_message_for(self, name):
        messages = list()
        search = self.browser.find_element(*WhatsAppElements.search)
        search.send_keys(name+Keys.ENTER)

        # time.sleep(1)

        element = self.browser.find_element(*WhatsAppElements.aside)
        element.click()

        ActionChains(self.browser).move_to_element(element).perform()
        #
        # time.sleep(1)

        row = 0
        message = ""
        phone = ""
        phone2 = ""

        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="_36FbL"):

            row = row + 1
            # Persona Natural
            if i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div > div"):
                phone = i.find("div", class_='_1ER5I')
                # message = "Ingreso 1° IF : {}".format(row)
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(7) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(5) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(7) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(7) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div

            #-app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(7) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(5) > div:nth-child(3) > div
            #app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div

            elif i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div > div"):
                phone = i.find("div", class_='_1ER5I')

            elif i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_1ER5I')

            elif i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div > div"):
                phone = i.find("div", class_='_1ER5I')

            elif i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(7) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_1ER5I')

            elif i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(5) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_1ER5I')

            elif i.select("#app > div._1ADa8._3Nsgw.app-wrapper-web.font-fix.os-win > div._1XkO3.three > div._3ArsE > div.ldL67._1bLj8 > span > div._1N4rE > span > div.nBIOd._2T-Z0.tm2tP.copyable-area > div > section > div:nth-child(6) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_1ER5I')

            if phone:
                phone2 = phone.find("span", class_='selectable-text')

            if phone2:
                message = phone2.find("span", class_='_3NUK1').text

        # messages = list(filter(None, messages))

        return message
