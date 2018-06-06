import requests
import sys
import os
import tkinter
import time

from bs4 import BeautifulSoup

#################################PARSE_FILE#####################################

def parse_file(filename):

    dico = {}

    with open(filename) as inputfile:
        for line in inputfile:
            if line[0] == "#":
                continue
            else:
                sp = line.split(",")
                dico[sp[0]] = sp[1].strip()

    return dico

##################################GET_PRICE/NAME###############################

def get_soup(URL):

    if len(URL) == 0:
        return 0

    if URL[:25] != "https://www.amazon.co.uk/":
        raise ValueError("URL must begin with https://www.amazon.co.uk \nYour input was " + URL)

    stat_code = -1

    while stat_code != 200:

        get_response = requests.get(URL)
        stat_code = get_response.status_code
        raw_html = get_response.text                    #GET response object and convert to text

    return BeautifulSoup(raw_html, "lxml")

def get_name(soup):

    return soup.find(id="productTitle").text.strip()

def get_price(soup):

    return float(soup.find(id="priceblock_ourprice").text[1:])

################################################################################

def write_file(name, price):
    with open(name, "a") as outputfile:

        if os.stat(name).st_size == 0:
            outputfile.write("# date, time, price\n")

        curr_time = time.strftime("%d/%m/%Y, %H:%M", time.gmtime())
        outputfile.write(curr_time + ", " + str(price) + "\n")


################################################################################

if __name__ == "__main__":

    print("----------Amazon-Price-Tracker----------\n")

    if "-f" in sys.argv:
        filename = sys.argv[sys.argv.index("-f") + 1]
        main_dico = parse_file(filename)

    if "-t" in sys.argv:
        wait_time = int(sys.argv[sys.argv.index("-t") + 1])
    else:
        wait_time = 60

    print("Wait time: " + str(wait_time))

    while True:

        for component in main_dico:
            soup = get_soup(main_dico[component])
            name = get_name(soup)
            price = get_price(soup)
            print(name)
            print("£" + str(price) + "\n")

            write_file(component, price)
        print("----------------------------------------")
        time.sleep(wait_time)

    else:
        print("Please specify a file by using -f followed by the filename.")
        print("To specify a time between price checks, use -t followed by the desired time in seconds.")
