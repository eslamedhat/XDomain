from tools.Sublist3r import sublist3r
import os

def sublist3r_run(domain,subbrute):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    os.chdir(dir_path)
    subdomains = sublist3r.main(domain, 40, 'subdomains.txt', ports= None, silent=False, verbose= True, enable_bruteforce= subbrute, engines=None)
    with open('subdomains.txt') as subdomains:
        with open("targets.txt", "a") as t:
            for i in subdomains:
                t.write(i)

def main():
    sublist3r_run("example.com")      


if __name__ == "__main__":
    main()