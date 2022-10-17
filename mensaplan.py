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

(options, args) = parser.parse_args()

if options.quiet:
    quiet = True
if options.uni_mensa:
    uni_mensa = True

console = Console()

# --------------------------------------------------------------
# Uni Bremen Mensa
UNI_MENSA_URL = "https://www.stw-bremen.de/de/mensa/uni-mensa"
this_parser = 'html.parser'
mensa_food_categories = ['Ausgabe 1', 
                         'Ausgabe 2', 
                         'Ausgabe 3', 
                         'kombinierBar',
                         'kombinierBar (wöchentlich wechselnd)',
                         'Salatangebot'
                         ]

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

    for i in range(0, len(mensa_food_categories)):
        table = Table(show_header=True, show_lines=True)
        table.add_column(mensa_food_categories[i], width=50)
        table.add_column("Preis (Stud.)", justify="right")
        table.add_column("Preis (Bed.)", justify="right")

        if quiet and i >= 2:
            return
        
        all_foods_descr = foods[i].findAll('td', class_="field field-name-field-description")
        all_foods_price_stud = foods[i].findAll('td', class_="field field-name-field-price-students")
        all_foods_price_emp = foods[i].findAll('td', class_="field field-name-field-price-employees")

        all_foods_descr_text = []

        for idx in range(len(all_foods_descr)):
            if all_foods_descr[idx].text != 'Täglich wechselndes Saucen-Angebot':
                food_descr = remove_sup_section(all_foods_descr[idx])
                all_foods_descr_text.append(food_descr)

        for i in range(len(all_foods_descr_text)):
            if i >= len(all_foods_price_stud):
                the_student_price = ""    
            else:
                the_student_price = all_foods_price_stud[i].text

            if i >= len(all_foods_price_emp):
                the_employee_price = ""
            else:    
                the_employee_price = all_foods_price_emp[i].text

            table.add_row(all_foods_descr_text[i], the_student_price, the_employee_price)
            
        console.print(table)
# --------------------------------------------------------------

print_mensa_meal()
