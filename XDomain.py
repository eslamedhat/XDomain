#apt-get update
#pip3 install python-nmap
#apt install python3-pip
#pip3 install builtwith
#pip3 install dnspython
from builtwith import *
import nmap, socket
import requests, os, shutil, glob, sys, time, csv, resource, argparse
from urllib.parse import urlparse
import urllib.request
from conf import conf
dir_path = os.path.dirname(os.path.realpath(__file__))

from tools import altdns
import sublist3r,JSFinder, screenshot, reportgen
from multiprocessing import Process
import multiprocessing
import eventlet
import subprocess

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
'''
if len(sys.argv) == 1:
    print("usage: python3 XDomain.py example.com")
    exit()
'''
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="The target domain", required=True)
args = parser.parse_args()

domain = args.domain    
#domain = sys.argv[1:]
#domain = domain[0]
os.system("mkdir Loot")
os.system("mkdir Loot/" + str(domain))
os.system("mkdir Loot/"+domain+"/screenshots")

alldata=[]


'''
def gen_csv(x):
    with open('out.csv','a') as f:
        for sublist in x:
            print(sublist)
            f.write(str(sublist) + ',')
        f.write('\n')
'''
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
    os.chdir(dir_path)
    print(os.getcwd())
    print("Removing dupliactes.....")
    with open("targets.txt") as result:
        uniqlines = set(result.readlines())
        with open('targets.txt', 'w') as uniqtargets:
            uniqtargets.writelines(set(uniqlines))
            
def live_targets(target,x):
    #domain= "seek.com.au"
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
    try:
        eventlet.monkey_patch()
        with eventlet.Timeout(10):
            httpstarget="https://"+target
            r = requests.get(httpstarget, verify=False, timeout=15)
            print(str(x)+" "+httpstarget + CYELLOW+" is up :)"+CEND)
            with open("live.txt", "a") as live:
                parsed_uri = urlparse(httpstarget)
                result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                live.write(result + "\n")
                
    except:
            try:
                eventlet.monkey_patch()
                with eventlet.Timeout(10):
                    target="http://"+target
                    r = requests.get(target, verify=False, timeout=15)
                    print(str(x)+" "+target + CYELLOW+" is up :)"+CEND)
                    with open("live.txt", "a") as live:
                        parsed_uri = urlparse(target)
                        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                        live.write(result + "\n")
            except:
                print(str(x)+" "+str(target) + " is down!")

    
def get_live():
    rem_dup1()
    os.chdir(dir_path)

    resource.setrlimit(resource.RLIMIT_NOFILE, (131072, 131072))
    #print(resource.getrlimit(RLIMIT_MSGQUEUE))
    time.sleep(3)
    x=0
    with open('targets.txt') as t:
        lines = [line.rstrip() for line in t]
        print(CRED+"checking live targets.... (default ports only 80 - 443)"+CEND)
        raw = open("live.txt", "w")
        def chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        numberOfThreads = 150
        jobs = []
        for target in lines:
            x =x+1
            #target=check_scheme(target)
            p = multiprocessing.Process(target=live_targets, args=(target,x,))
            jobs.append(p)
            #live_targets(target)
        for i in chunks(jobs,numberOfThreads):
            for j in i:
                j.start()
            for j in i:
                j.join()
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
    global dir_path
    os.chdir(dir_path)
    print(CRED+"Getting subdomains with Amass..."+CEND)
    os.system("./tools/amass enum -passive -d "+domain+" -o targets.txt")


def securitytrails(domain):
    print(CRED+"Getting subdomains from SecurityTrails..."+CEND)
    url = "https://api.securitytrails.com/v1/domain/"+domain+"/subdomains"

    querystring = {"children_only":"false"}
    
    headers = {'accept': 'application/json', 'apikey': conf.securitytrailsAPI}

    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.text)
    json_data = response.json() if response and response.status_code == 200 else None
    if json_data and 'subdomains' in json_data:
        for sub in json_data['subdomains']:
            print(sub+"."+domain)
            with open("targets.txt", "a") as t:
                t.write(sub+"."+domain+ "\n")
            #print(sub+"."+domain)
    else:
        print("Please make sure that you added the api key for SecurityTrails")
        time.sleep(2)


def altdns_generate():
    print(CRED+"Generating subdomains via altdns..."+CEND)
    altdns.main()
    os.chdir(dir_path)
    with open('altdns.txt') as subdomains:
        with open("targets.txt", "a") as t:
            for i in subdomains:
                t.write(i)
    os.system("rm altdns.txt")
    
def smart_scan():
    os.chdir(dir_path)
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
    if conf.sectrails == True:
        securitytrails(domain)
    if conf.altdns    == True:
        altdns_generate()
    if conf.live      == True:       
        get_live()
    if conf.JSFinder  == True:
        print(CRED+"Getting subdomains from javascript files from all the live subdomains..."+CEND)
        JSFinder.Js_subdomains()
    if conf.smartscan == True:
        smart_scan()

    
    
    
if __name__ == "__main__":
    #altdns.main()
    main()



