# XDomain (Auto powerful subdomains scanner)
The best thing in life is automation.
I enjoy coding stuff and I was searching for something to collect subdomains, I found a lot of tools, but I didn't find the automation part. I made this tool based on different tools and my own code. 

## XDomain will do the following:

* Get subdomains from Amass.
* Get subdomains from Sublist3r.
* Get subdomains from Subbrute.
* Get subdomains from SecurityTrails API (You need to add the API key in the config file).
* Generate subdomains via altdns.
* Auto take the founded list of subdomains and find the live targets. (The quality of this function is better than httprobe).
* Find hidden subdomains in JavaScript files from all the founded subdomains.
* Remove all duplicates.
* Take a screenshot for every subdomain.
* Find the technology of every subdomain.
* Nmap scan against every subdomain.
* Generate a quick HTML report.

## Requirements:
* sudo apt-get update
* sudo apt install python3-pip
* sudo apt-get install nmap
* pip3 install builtwith
* pip3 install python-nmap
* pip3 install dnspython
* pip3 install BeautifulSoup4 (On some systems, you need to install this first "sudo apt-get install python-bs4")
* pip3 install selenium
* pip3 install eventlet
* sudo apt-get install firefox-esr (Only if not installed)

## Usage:
Note: Don't forget to give executable permissions to all the files in the tools directory.

```
cd XDomain
chmod -R +x tools/
python3 XDomain.py -d wikihak.com
```
## Screenshots:
![alt text](https://wikihak.com/wp-content/uploads/1.JPG)

![alt text](https://wikihak.com/wp-content/uploads/2.JPG)

![alt text](https://wikihak.com/wp-content/uploads/3.JPG)

All the founded domains will be in "targets.txt".
All the live hosts will be in "live.txt".
In the conf.py, you will be able to control the used tools and the Nmap ports. 

I was working on a bigger tool, but I didn't have time to continue it. I will try to add more stuff in the future. 

## Things that might be added in the future:
* Auto directory/file bruteforce.
* waybackurls.
* Auto crawler.
* Auto scanner for different type of vulnerabilities.

Please let me know your suggestions. Enjoy! :D 

## Credits:
* [Sublist3r](https://github.com/aboul3la/Sublist3r/) - Thanks to my friend aboul3la :).
* [Amass](https://github.com/OWASP/Amass) - Thanks to OWASP.
* [Subbrute](https://github.com/TheRook/subbrute) - Thanks to TheRook.


