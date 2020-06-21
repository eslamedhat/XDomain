#apt-get update
#pip3 install python-nmap
#apt install sqlmap
#apt install python3-pip
#apt install golang-go
#pip3 install python-owasp-zap-v2.4
#pip3 install builtwith
#pip3 install dnspython
#sudo apt-get install gobuster
#sudo apt install default-jdk
from builtwith import *
import nmap, socket
import requests, os, shutil, glob, sys, time, csv
from urllib.parse import urlparse
import urllib.request
from conf import conf
dir_path = os.path.dirname(os.path.realpath(__file__))

import sublist3r,JSFinder, screenshot, reportgen
from multiprocessing import Process
CRED = '\033[91m'
CYELLOW = '\33[33m'
CEND = '\033[0m'

def banner():
    print("""
            __  ______                        _       
            \ \/ /  _ \  ___  _ __ ___   __ _(_)_ __  
             \  /| | | |/ _ \| '_ ` _ \ / _` | | '_ \ 
             /  \| |_| | (_) | | | | | | (_| | | | | |
            /_/\_\____/ \___/|_| |_| |_|\__,_|_|_| |_|
                  By Eslam Medhat - wikihak.com
    """)

banner()
if len(sys.argv) == 1:
    print("usage: python3 XDomain.py example.com")
    exit()
domain = sys.argv[1:]
domain = domain[0]
os.system("mkdir Loot")
os.system("mkdir Loot/" + str(domain))
os.system("mkdir Loot/"+domain+"/screenshots")

alldata=[]



def gen_csv(x):
    with open('out.csv','a') as f:
        for sublist in x:
            print(sublist)
            f.write(str(sublist) + ',')
        f.write('\n')

def check_scheme(target):
        target= target.strip()
        target = "http://"+target
        return target    
def rem_dup2():
    print(CRED+"Removing dupliactes....."+CEND)
    with open("live.txt") as result:
        uniqlines = set(result.readlines())
        with open('live.txt', 'w') as uniqtargets:
            uniqtargets.writelines(set(uniqlines))
            
def rem_dup1():
    print(os.getcwd())
    print("Removing dupliactes.....")
    with open("targets.txt") as result:
        uniqlines = set(result.readlines())
        with open('targets.txt', 'w') as uniqtargets:
            uniqtargets.writelines(set(uniqlines))
            
def live_targets():
    
    #global dir_path
    #os.chdir(dir_path)
    from requests.packages.urllib3.exceptions import InsecureRequestWarning

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
    
    rem_dup1()
    with open('targets.txt') as t:
        lines = [line.rstrip() for line in t]
        print(CRED+"checking live targets.... (default ports only 80 - 443)"+CEND)
        raw = open("live.txt", "w")
        for target in lines:
            target=check_scheme(target)
            try:
                r = requests.get(target, verify=False, timeout=5)
                print(r.url)
                with open("live.txt", "a") as live:
                    parsed_uri = urlparse(r.url)
                    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                    if domain in result:
                        live.write(result + "\n")
                    else:
                        print(target+" redirect to "+result+" it will not be added to live.txt ")
            except:
                print(str(target) + " is down!")
    rem_dup2()


def detect_tech(target):
    tech=builtwith(target)
    if "404" in tech:
        print("Couldn't detect technology with BuiltWith!")
        return "Not detected!"
    else:
        return tech

def clear_url(x):# to make a folder with the domain name
    x = x.replace("http://","")
    x = x.replace("https://","")
    x=x.replace("/","")
    return x



def amass_scan():
    #global dir_path
    #os.chdir(dir_path)
    print(CRED+"Getting subdomains with Amass..."+CEND)
    os.system("./tools/amass enum -passive -d "+domain+" -o targets.txt")


def smart_scan():
    global alldata
    global domain
    #all_subs=[]
    #with open("live.txt") as f:
       # all_subs = f.read().splitlines()

    #os.chdir(dir_path)
    reportgen.gen_html1(domain)

    #screenshot.screenshot(all_subs,domain)
    print(CYELLOW+"Taking screenshots for all subdomains... "+CEND)
    #screenshot.take_all_screenshots(domain)
    p = Process(target=screenshot.take_all_screenshots, args=(domain,))
    p.start()
    #screenshot.take_all_screenshots(domain)
    with open('live.txt') as t:
        lines = [line.rstrip() for line in t]

    for i in lines:
        #print (detect_protocol(i))

        alldata.append("Loot/"+domain+"/screenshots/"+clear_url(i)+".png")
        alldata.append(i)
        try:
            alldata.append(socket.gethostbyname(clear_url(i)))
        except:
            alldata.append("")
        print(CYELLOW+"Detecting technologies for: "+CEND+ i)
        technology= detect_tech(i)
        parsed_tech=""
        for k, v in technology.items():
            #print(k,v)
            parsed_tech=parsed_tech + " " +str(k) + str(v)+"<br>"
            parsed_tech=parsed_tech.replace("'","")
            #parsed_tech=parsed_tech.replace(": ","")
            #parsed_tech=parsed_tech.replace("]","")
        alldata.append(parsed_tech)
        
        
        print(CYELLOW+"Nmap scan for: "+CEND+ i)
        nm = nmap.PortScanner()

        port_range=conf.ports
        subdomain = clear_url(i)
        try:
            nm.scan(subdomain,port_range)
        except:
            print("Error happened while scanning: "+subdomain)
        
        open_ports=""
        for host in nm.all_hosts():
             for proto in nm[host].all_protocols():
         
                 lport = nm[host][proto].keys()
                 #lport.sort()
                 for port in lport:
                     if nm[host][proto][port]['state'] == "open":
                         open_ports=open_ports+ "  "+str(port)+" | "+ nm[host][proto][port]['name'] +" | " +nm[host][proto][port]['product']+": "+nm[host][proto][port]['cpe']+"<br>"
        alldata.append(open_ports)
        
        reportgen.gen_html2(domain,alldata)
        alldata.clear()
    print(CRED+"Generating the report..."+CEND)
    reportgen.gen_html3(domain)


def main():

    if conf.amass     == True:
        amass_scan()
    if conf.sublist3r == True:
        print(CRED+"Getting subdomains with Sublist3r..."+CEND)
        sublist3r.sublist3r_run(domain,conf.subbrute)
    if conf.live      == True:       
        live_targets()
    if conf.JSFinder  == True:
        print(CRED+"Getting subdomains from javascript files from all the live subdomains..."+CEND)
        JSFinder.Js_subdomains()
    if conf.smartscan == True:
        smart_scan()

    
    
    
if __name__ == "__main__":
    main()

