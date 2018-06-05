import requests
import sys
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

    raw_html = requests.get(URL).text #GET response object and convert to text
    return BeautifulSoup(raw_html, "lxml")

def get_name(soup):

    return soup.find(id="productTitle").text.strip()

def get_price(soup):

    return float(soup.find(id="priceblock_ourprice").text[1:])

################################################################################

if __name__ == "__main__":
    if "-f" in sys.argv:
        filename = sys.argv[sys.argv.index("-f") + 1]
        main_dico = parse_file(filename)

        for component in main_dico:
            soup = get_soup(main_dico[component])
            print(get_name(soup) + ": £" + str(get_price(soup)))




    else:
        print("Please specify a file by using -f followed by the filename.")
