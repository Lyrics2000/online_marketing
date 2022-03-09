import scrapy
import yaml
from pathlib import Path
from selenium.webdriver.common.by import By
import os
import glob

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time


class FbspiderSpider(scrapy.Spider):
    name = 'FbSpider'
   

    def start_requests(self):
        url = "https://wwww.facebook.com"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.headless = False
       
        chrome = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        chrome.get(url)
        time.sleep(5)
        self.login_to_facebook(chrome)
        self.post_on_page(chrome)



        return super().start_requests()

    def parse(self, response):
        pass

    def login_to_facebook(self,driver):
        script_location = Path(__file__).absolute().parent
        file_location = script_location / 'credentials/facebook.yml'
        f = file_location.open()
      
        data  =  yaml.load(f,Loader=yaml.FullLoader)
        
        
        username_box = driver.find_element_by_id('email')
        username_box.send_keys(data['username'])
        print("entering email")
        time.sleep(1)

        password_box = driver.find_element_by_id('pass')
        password_box.send_keys(data['password'])
        print ("Password entered")

        login_box = driver.find_element_by_name('login')
        login_box.click()
        time.sleep(5)

    def post_on_page(self,driver):
        time.sleep(5)
        print("going to gheko profile")
        driver.get("https://www.facebook.com/profile.php?id=100078353754869")
        time.sleep(5)
        print("clicking on upload post div")
        xpath =  driver.find_element_by_xpath("//*[@class='m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b']")
        xpath.click()
        time.sleep(5)

        print("sending post message")
        upload_img = driver.find_elements(by = By.XPATH,value="//*[@class='bp9cbjyn j83agx80 taijpn5t l9j0dhe7 datstx6m k4urcfbm']")
        upload_img[1].click()

        time.sleep(3)
        div_writer =  driver.find_element_by_xpath("//*[@data-contents='true']")
        div_writer.send_keys("hello im lyrics")
        time.sleep(2)
        post_writer =  driver.find_element_by_xpath("//*[@class='s45kfl79 emlxlaya bkmhp75w spb7xbtv bp9cbjyn rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv pq6dq46d taijpn5t l9j0dhe7 tdjehn4e qypqp5cg q676j6op']")
        # post_writer.click()
        time.sleep(2)
        path = Path(__file__).absolute().parent
        
        facebook_images_path =  path / "facebook_images"
        print(facebook_images_path)

        list_endings = ['.jpg','.png']
        all_files = []

        for i in list_endings:
            oo = glob.glob(f"{str(facebook_images_path)}/*{i}")
            for k in oo:
                all_files.append(k)


        print(all_files)

    
        # post_writer.send_keys(all_files[0])

