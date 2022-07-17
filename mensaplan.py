#!/usr/bin/python3
####################################
##
## Author        : Felix Bruening
## Date          : 2019
## Last changed  : 2021-12-28
## 
##

# --------------------------------------------------------------
from bs4 import BeautifulSoup
import urllib.request as urllib2 
from optparse import OptionParser
import datetime
import re
from rich.console import Console
from rich.table import Table

# --------------------------------------------------------------
# Global option variables
quiet = False
uni_mensa = False
cafe_unique = False
show_all = False

# --------------------------------------------------------------
# Parse Options
parser = OptionParser()
parser.add_option("-q", "--quiet",
                    help="shows only main meals",
                    action="store_true",
                    dest="quiet")
parser.add_option("-m", "--mensa",
                    help="prints meals of mensa uni bremen",
                    action="store_true",
                    default=True,
                    dest="uni_mensa")
parser.add_option("-u", "--unique",
                    help="prints meals of cafe unique",
                    action="store_true",
                    default=False,
                    dest="cafe_unique")
parser.add_option("-a", "--show-all",
                    help="prints meals of cafe unique and uni-mensa",
                    action="store_true",
                    default=False,
                    dest="show_all")

(options, args) = parser.parse_args()

if options.quiet:
    quiet = True
if options.uni_mensa:
    uni_mensa = True
    cafe_unique = False
if options.cafe_unique:
    cafe_unique = True
    uni_mensa = False
if options.show_all:
    show_all = True

console = Console()

# --------------------------------------------------------------
# Uni Bremen Mensa
UNI_MENSA_URL = "https://www.stw-bremen.de/de/mensa/uni-mensa"
this_parser = 'html.parser'
mensa_food_categories = ['Ausgabe 1', 
                         'Ausgabe 2', 
                         'Vegetarische Theke', 
                         'Cafe Central "to-go" Angebot 1', 
                         'Cafe Central "to-go" Angebot 2']

# remove a weird html-tag from html-table section
# no elegant solution but it works
def remove_sup_section(section):
    del section['class']
    section_str = str(section).replace('<sup>', '<').replace('</sup>', '>').replace('<td>', '').replace('</td>', '').replace('&amp;', 'und')
    return re.sub(r'<.+?>', '', section_str)

# Function that parses the website and prints the meals of a day
def print_mensa_meal():
    html = urllib2.urlopen(UNI_MENSA_URL)
    soup = BeautifulSoup(html, this_parser)
    foods = soup.findAll('table', class_='food-category')

    print("##########################################")
    print("## Mensa plan University of Bremen") 
    print("##")
    print("## Today's date: " + datetime.datetime.now().strftime("%A, den %d.%m.%Y"))
    print("##")
    print("##########################################\n")


    for i in range(0, len(mensa_food_categories)):
        table = Table(show_header=True, show_lines=True)
        table.add_column(mensa_food_categories[i], width=50)
        table.add_column("Preis (Stud.)", justify="right")
        table.add_column("Preis (Bed.)", justify="right")

        if quiet and i >= 2:
            return
        food_descr_sec = foods[i].find('td', class_="field field-name-field-description")
        food_descr = remove_sup_section(food_descr_sec)
        price_stud = foods[i].find('td', class_="field field-name-field-price-students").text
        price_emp  = foods[i].find('td', class_="field field-name-field-price-employees").text

        table.add_row(food_descr, price_stud, price_emp)    
        console.print(table)
# --------------------------------------------------------------

# --------------------------------------------------------------
# Cafe Unique Bremen Campus
UNIQUE_MENU = "https://www.uni-bremen.de/speiseplaene"

def print_unique_meal():
    html_dump = urllib2.urlopen(UNIQUE_MENU)
    soup = BeautifulSoup(html_dump, this_parser)
    food_table = soup.findAll('tr', class_="tr-odd")
    content = food_table[0]
    sec_row = content.findAll(lambda item: item.name == 'td')    
    parts = sec_row[1].text.split("€")

    meals = []
    for s in parts:
        s = re.sub('[0-9,]', '', s)
        meals.append(s)
    
    meals = [x for x in meals if x and x != " "]

    # 'prices' is a list of orderes price-strings
    allPrices = sec_row[1].findAll(lambda item: item.name == 'strong')
    prices = []
    for var in allPrices:
        p2 = str(var)
        prices.append(p2.replace("<strong>", "").replace("</strong>", ""))

    if len(prices) != len(meals):
        print("[ERROR] Length of price-row and meal-row are different!")
        return

    print("##########################################")
    print("## Meal-plan Cafe Unique") 
    print("##")
    print("## Today's date: " + datetime.datetime.now().strftime("%A, den %d.%m.%Y"))
    print("##")
    print("##########################################\n")
    table = Table(show_header=True, show_lines=True)
    table.add_column("Gericht", width=50)
    table.add_column("Preis", justify="right")

    for i in range(0, len(meals)):
        table.add_row(meals[i], prices[i])
    
    console.print(table)

# --------------------------------------------------------------

if show_all or uni_mensa:
    print_mensa_meal()

if show_all or cafe_unique:
    print_unique_meal()
