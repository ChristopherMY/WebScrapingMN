from math import nan
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
from lxml import etree


class WhatsAppElements:
    search = (By.CSS_SELECTOR,
              "#side > div.uwk68 > div > div > div._16C8p > div > div._13NKt.copyable-text.selectable-text")
    aside = (By.CSS_SELECTOR,
             "#main > header > div._24-Ff > div._2rlF7 > div > span")

    remove = (By.CSS_SELECTOR, "#side > div.uwk68 > div > button")


class WhatsApp:
    browser = None
    size = 0
    timeout = 500  # The timeout is set for about ten seconds

    def __init__(self, wait, screenshot=None, session=None):
        if self.browser is None:
            try:
                self.browser = webdriver.Chrome(
                    executable_path="chromedriver.exe")  # change path
                # to open the WhatsApp web
                self.browser.get("https://web.whatsapp.com/")

                # you need to scan the QR code in here (to eliminate this step, I will publish another blog

                WebDriverWait(self.browser, 560).until(
                    EC.presence_of_element_located(WhatsAppElements.search))  # wait till search element appears

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
                WhatsAppElements.search))

    def unread_usernames(self, scrolls=100):
        self.goto_main()
        initial = 10
        usernames = []

        e = self.browser.find_element_by_xpath("//*[@id='pane-side']")
        content = e.size
        size = content['height'] + content['width']

        # --
        #search = self.browser.find_element(*WhatsAppElements.search)
        #search.send_keys("Silla" + Keys.ENTER)

        time.sleep(2)

        # 663243
        # 38432
        # 48432
        # 28415
        # 18415
        # 2600
        # 2600
        # 15600
        # 1300 CM
        for i in range(0, 1300):
            self.browser.execute_script(
                "document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_3OvU8"):  # replace for _1V5O7
                if i.find("div", class_="_3vPI2"):
                    if i.find("div", class_="zoWT4"):
                        # if i.find("span", class_="_3q9s6"):
                        # username = i.find("span", class_="_ccCW").
                        username = i.find(
                            "span", class_="ggj6brxn")

                        if(i.find("span", class_="matched-text")):
                            username = i.find("span", class_="matched-text")

                        if(username):
                            usernames.append(username.text)

            initial += 10
        # Remove duplicates
        usernames = list(set(usernames))
        return usernames

    def get_last_message_for(self, name):
        # ----
        #remove = self.browser.find_element(*WhatsAppElements.remove)
        # remove.click()

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
        aux = ""

        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        dom = etree.HTML(str(soup))

        # TODO: Elementos obtenibles de selected span number account
        if(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/div/span/span')):
            print("/*1")
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/div/span/span')

        elif(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[3]/div[1]/div[2]/span')):
            print("/*2")
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[3]/div[1]/div[2]/span')

        elif(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[6]/div[3]/div/div/span/span')):
            print("/*3")
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[6]/div[3]/div/div/span/span')

        elif(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[7]/div[2]/div/div/span/span')):
            print("/*4")
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[7]/div[2]/div/div/span/span')

        elif(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/h2/span')):
            print("/*5")
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/h2/span')

        elif(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[8]/div[3]/div/div/span/span')):
            print("/*6")
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[8]/div[3]/div/div/span/span')

        elif(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[6]/div[2]/div/div/span/span')):
            aux = dom.xpath(
                '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[6]/div[2]/div/div/span/span')

        if(aux):
            # print(name)
            # print(aux[0])
            # print(aux[0].getText())`
            # print(aux[0].text)
            # print("")

            temp = aux[0].text
            print("temp")
            print(temp)
            if(temp):
                if(temp[0:3] == "+51"):
                    message = aux[0].text
                else:
                    if(dom.xpath('//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/h2/span') is nan):
                        aux2 = dom.xpath(
                            '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[2]/h2/span')
                        if(aux2):
                            message = aux2[0].text
                        else:
                            message = ""

        print("message {}".format(message))
        return message


"""
        for i in soup.find_all("div", class_="KPJpj"):
            print(name);
            row = row + 1
            # Persona Natural
            if i.select("#app > div > div > div._3ArsE > div.ldL67._1bLj8 > span > div > span > div > div > section > div._1is6W.ZIBLv.g0rxnol2.tvf2evcx.oq44ahr5.lb5m6g5c.brac1wpa.lkjmyc96.b8cdf3jl.bcymb0na.myel2vfb.e8k79tju > div.p357zi0d.ktfrpxia.nu7pwgvd.fhf7t426.f8m0rgwh.gndfcl4n"):
                # if(temp is None):
                print("1~")
                phone = i.find("div", class_='qt60bha0')
                i.find()
`
            # elif i.select("#app > div > div > div._3ArsE > div.ldL67._1bLj8 > span > div > span > div > div > section > div:nth-child(7) > div.gx1rr48f.Wt3HP > div"):
            elif i.select("#app > div > div > div._3ArsE > div.ldL67._1bLj8 > span > div > span > div > div > section` > div:nth-child(6) > div.gx1rr48f.Wt3HP > div"):
                print("2~")
                phone = i.find("div", class_='ggj6brxn')

            elif i.select("#app > div > div > div._3ArsE > div.ldL67._1bLj8 > span > div > span > div > div > section > div._1is6W.ZIBLv.g0rxnol2.tvf2evcx.oq44ahr5.lb5m6g5c.brac1wpa.lkjmyc96.i4pc7asj.bcymb0na.przvwfww.e8k79tju > div.gx1rr48f.Wt3HP > div"):
                print("3~")
                phone = i.find("div", class_='m0h2a7mj')

            print("")
            print("phone")
            print(phone)

            if phone:
                message = phone.find(
                    "span", class_='selectable-text').getText()

            # if aux:
            #   message = aux.find("span", class_='_1lF7t').getText()

                # temp = i.find("h2", class_='qfejxiq4')
                # _other_ = temp.find(
                #     "span", class_='selectable-text').getText()
                # if(_other_[0:3] == "+51"):
                #     print(_other_[0:3])
                #     message = _other_
                # messages = list(filter(None, messages))
        """
