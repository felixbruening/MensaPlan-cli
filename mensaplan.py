#!/usr/bin/python3
####################################
##
## Author        : Felix Bruening
## Date          : 2019
## Last changed  : 2021-10-12
## 
##
# --------------------------------------------------------------
from bs4 import BeautifulSoup
import urllib.request as urllib2 
from optparse import OptionParser
import datetime
import re

# --------------------------------------------------------------
# Global option variables
verbose = False
uni_mensa = False
cafe_unique = False
show_all = False

# --------------------------------------------------------------
# Parse Options
parser = OptionParser()
parser.add_option("-v", "--verbose",
                    help="shows only main meals",
                    action="store_true",
                    dest="verbose")
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

if options.verbose:
    verbose = True
if options.uni_mensa:
    uni_mensa = True
if options.cafe_unique:
    cafe_unique = True
    uni_mensa = False
if options.show_all:
    show_all = True

# --------------------------------------------------------------
# Uni Bremen Mensa
UNI_MENSA_URL = "https://www.stw-bremen.de/de/mensa/uni-mensa"
this_parser = 'html.parser'
mensa_food_categories = ['Ausgabe 1', 
                         'Ausgabe 2', 
                         'Vegetarische Theke', 
                         'Cafe Central "to-go" Angebot 1', 
                         'Cafe Central "to-go" Angebot 2']

# --------------------------------------------------------------
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
        if verbose and i >= 2:
            return
        food_descr_sec = foods[i].find('td', class_="field field-name-field-description")
        food_descr = remove_sup_section(food_descr_sec)
        price_stud = foods[i].find('td', class_="field field-name-field-price-students").text
        price_emp  = foods[i].find('td', class_="field field-name-field-price-employees").text
        string = mensa_food_categories[i] + ": \n===============================\n"
        string += "\n" + food_descr + "\n --> Preis (Studenten):   " + price_stud 
        string += "\n --> Preis (Bedienstete): " + price_emp 
        print(str(string))
        print("\n")

if show_all or uni_mensa:
    print_mensa_meal()

if show_all or cafe_unique:
    print("MEAL CAFE UNIQUE TEST")
