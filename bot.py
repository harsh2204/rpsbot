import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import sys
from driver import Bot

hmap = {
        1:'rock',
        2:'paper',
        3:'scissors'
    }

botboy = Bot('bot2.py')

def call(d, x:int):
    buttons = d.find_elements(By.XPATH, f"//div[@class='action']/input[@id='{hmap[x]}']")
    d.execute_script('arguments[0].click()', buttons[0])
    time.sleep(10)

def play(num):
    
    now = datetime.now()
    timestamp = f'{now.day}.{now.month}.{now.year}_to{num}'

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    d = webdriver.Chrome(chrome_options=options)

    d.get("https://rockpaperprizes.com/")
    time.sleep(1)#Page 1

    d.find_element_by_xpath("//select[@name='province']/option[text()='Ontario']").click()
    d.find_element_by_xpath("//button[@class='button submit']").click()
    time.sleep(3)#Page 2


    d.find_element_by_xpath("//input[@name='phone']").send_keys(num)
    d.find_element_by_xpath("//button[contains(@class, 'button')]").click()


    time.sleep(10)#Page 3..6    
    while True:        
        res = d.find_element_by_tag_name('h1').text
        if 'PRIZES' in res:
            break

        roll = random.randint(1, 3)
        
        
        print(f"Rolled {hmap[roll]}")
        time.sleep(1)
        
        try:
            call(d, roll)
        except:
            print("Couldn't roll", roll)
            break                   

    d.save_screenshot(f'{timestamp}.png')
    print("Done playing!")
    time.sleep(5)
    d.close()

if __name__ == "__main__":
    if(len(sys.argv[-1])):
        play(str(sys.argv[-1]))
  
