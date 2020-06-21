import time, os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
def clear_url(x):
    x = x.replace("http://","")
    x = x.replace("https://","")
    x=x.replace("/","")
    return x
def screenshot(subdomain,domain):

    options = Options()
    options.headless = True
    #options.add_argument( executable_path='tools/geckodriver' )
    driver = webdriver.Firefox(options=options, executable_path='tools/geckodriver')
    #driver = webdriver.Firefox( firefox_options=options )
    driver.get(subdomain)
    driver.save_screenshot('Loot/'+domain+'/screenshots/'+clear_url(subdomain)+'.png')
    #print('Loot/'+domain+'/screenshots/'+subdomain+'.png')
    #print (driver.title)
    #print (driver.current_url)
    driver.quit()
    os.system("pkill firefox-esr")
    os.system("pkill geckodriver")

def take_all_screenshots(domain):
    #print(domain)
    #print("**********************************")
    with open('live.txt') as t:
        lines = [line.rstrip() for line in t]

    for i in lines:
        #print("takeng sc shot......................................")
        screenshot(i,domain)
        #time.sleep(10)
#take_all_screenshots("c2m.net")       
