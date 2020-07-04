class conf:
    ###################Choose the tool that you want to run "True or False"
    amass    =True # Get subdomains via Amass
    sublist3r=True # Get subdomains via Sublist3r
    sectrails=True  # Get subdomains from SecurityTrails API
    subbrute =True # Bruteforce subdomains via Subbrute   
    altdns   =True # Generate subdomains via altdns   
    live     =True  # Check the all the collected subdomains in "targets.txt" then add the live subdomains in "live.txt"
    JSFinder =True # Find subdomains in javascript files from all the live subdomains and append them with "live.txt"
    smartscan=True # Screenshot, Detect technology, Nmap scan, and generate a report
    #Add the ports for Nmap scan
    ports    = '20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,10000'
    
    ############################API keys......
    securitytrailsAPI=''
