import time, os
import multiprocessing
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def clear_url(x):
    x = x.replace("http://","")
    x = x.replace("https://","")
    x=x.replace("/","")
    return x
def screenshot(subdomain,domain):

    options = Options()
    options.headless = True
    #options.add_argument( executable_path='tools/geckodriver' )
    try:
        driver = webdriver.Firefox(options=options, executable_path='tools/geckodriver')
    except:
        try:
            driver = webdriver.Firefox(options=options, executable_path='tools/geckodriver64')
        except:
            print("Couldn't start webdriver, please make sure that geckodriver has executable permissions")
    
    try:

        driver.set_page_load_timeout(50)
        #driver = webdriver.Firefox( firefox_options=options )
        driver.get(subdomain)
        driver.save_screenshot('Loot/'+domain+'/screenshots/'+clear_url(subdomain)+'.png')
            #print('Loot/'+domain+'/screenshots/'+subdomain+'.png')
            #print (driver.title)
            #print (driver.current_url)
        driver.quit()
        #os.system("pkill firefox-esr")
        #os.system("pkill geckodriver")
    except:
            try:

                driver.set_page_load_timeout(50)
                #driver = webdriver.Firefox( firefox_options=options )
                driver.get(subdomain)
                driver.save_screenshot('Loot/'+domain+'/screenshots/'+clear_url(subdomain)+'.png')
                    #print('Loot/'+domain+'/screenshots/'+subdomain+'.png')
                    #print (driver.title)
                    #print (driver.current_url)
                driver.quit()
                #os.system("pkill firefox-esr")
                #os.system("pkill geckodriver")
            except:
                print("Couldn't take screenshot for: "+str(subdomain))
        
def take_all_screenshots(domain):
    #print(domain)
    #print("**********************************")
    with open('live.txt') as t:
        lines = [line.rstrip() for line in t]
        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        numberOfThreads = 4
        jobs = []
        for i in lines:
        #print("takeng sc shot......................................")
            p = multiprocessing.Process(target=screenshot, args=(i,domain,))
            jobs.append(p)
            #live_targets(target)
        for i in chunks(jobs,numberOfThreads):
            for j in i:
                j.start()
            for j in i:
                j.join()
        #screenshot(i,domain)
        #time.sleep(10)
#take_all_screenshots("c2m.net")       

