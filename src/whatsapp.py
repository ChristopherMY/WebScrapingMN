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
              "#side > div.SgIJV > div > label > div > div._2_1wd.copyable-text.selectable-text")
    aside = (By.CSS_SELECTOR, "#main > header > div._2uaUb")


class WhatsApp:
    browser = None
    size = 0
    timeout = 15  # The timeout is set for about ten seconds

    def __init__(self, wait, screenshot=None, session=None):
        if self.browser is None:
            self.browser = webdriver.Chrome(
            executable_path="chromedriver.exe")  # change path
                # to open the WhatsApp web
            self.browser.get("https://web.whatsapp.com/")

                # you need to scan the QR code in here (to eliminate this step, I will publish another blog
            try:
                WebDriverWait(self.browser, wait).until( 
                EC.presence_of_element_located(WhatsAppElements.content)) #wait till search element appears
            except Exception as e:
                print(e)

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
        for i in range(0, size):
            self.browser.execute_script("document.getElementById('pane-side').scrollTop={}".format(initial))
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            for i in soup.find_all("div", class_="_2Z4DV"): # replace for _1V5O7
                if i.find("div", class_="_2pkLM"):
                    username = i.find("div", class_="_3Dr46").text
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
        # time.sleep(1)      
        
        row = 0
        message = ""
        phone = ""
        phone2 = ""
        
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        for i in soup.find_all("div", class_="_2kOFZ"):      
            
            row = row + 1
            
            if i.select("#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > div._3QfZd.three > div.Akuo4 > div._1Flk2._3xysY > span > div._1sMV6 > span > div.OMoBQ._2W4mF._3wXwX.copyable-area > div > section > div:nth-child(4) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_10szZ')
                # message = "Ingreso 1° IF : {}".format(row)
                
            elif i.select("#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > div._3QfZd.three > div.Akuo4 > div._1Flk2._3xysY > span > div._1sMV6 > span > div.OMoBQ._2W4mF._3wXwX.copyable-area > div > section > div:nth-child(7) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_10szZ')
                # message = "Ingreso 1° ELSEIF : {}".format(row)
            
            elif i.select("#app > div._3h3LX._34ybp.app-wrapper-web.font-fix.os-win > div._3QfZd.three > div.Akuo4 > div._1Flk2._3xysY > span > div._1sMV6 > span > div.OMoBQ._2W4mF._3wXwX.copyable-area > div >  section > div:nth-child(6) > div:nth-child(3) > div"):
                phone = i.find("div", class_='_10szZ')
                # message = "Ingreso 1° ELSEIF : {}".format(row) 
            # else:
                # message = "No Ingreso 1° IF : {}".format(row)
                
            if phone:
                phone2 = phone.find("span", class_='selectable-text')
                # message = "Ingreso 2° IF : {}".format(row)
            # else:
                # message = "No Ingreso 2° IF : {}".format(row)
                
            if phone2:
                # message = "Ingreso 3° IF : {}".format(row)
                message = phone2.find("span", class_='_1Kn3o').text
            # else:
                # message = "No Ingreso 3° IF : {}".format(row)                        
            
        # messages = list(filter(None, messages))
        # messages = list(filter(None, messages))
       
        return message
