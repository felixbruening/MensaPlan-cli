#!/usr/bin/python
####################################
#
# Author        : Felix Bruening
# Date          : 2019
# Last changed  : 2021-10-12
# 
####################################

from bs4 import BeautifulSoup
import urllib.request  as urllib2 
import datetime
import re

URL = "https://www.stw-bremen.de/de/mensa/uni-mensa"
this_parser = 'html.parser'
food_categories = ['Ausgabe 1', 'Ausgabe 2', 'Vegetarische Theke', 'Cafe Central "to-go" Angebot 1', 'Cafe Central "to-go" Angebot 2']

# Meal Class
class Meal:
    name        = ""
    category    = ""
    description = ""
    stud_price  = ""
    emp_price   = ""

    def __init__(self, name, cat, descr, stud_price, emp_price):
        self.name = str(name)
        self.category = str(cat)
        self.description = str(descr)
        self.stud_price = str(stud_price)
        self.emp_price = str(emp_price)

    def printObj(self):
        string = str(self.name) + ": \n=================\n"
        string += "\n" + str(self.description) + "\n --> Preis (Studenten):   " + str(self.stud_price) 
        string += "\n --> Preis (Bedienstete): " + str(self.emp_price)
        print(str(string))

# remove a weird html-tag from html-table section
# no elegant solution but it works
def remove_sup_section(section):
    del section['class']
    section_str = str(section).replace('<sup>', '<').replace('</sup>', '>').replace('<td>', '').replace('</td>', '').replace('&amp;', 'und')
    return re.sub(r'<.+?>', '', section_str)

# Function that parses the website and prints the meals of a day
def parse_and_print():
    allFoods = []
    html = urllib2.urlopen(URL)
    soup = BeautifulSoup(html, this_parser)
    foods = soup.findAll('table', class_='food-category')

    for i in range(0, len(food_categories)):
        category   = food_categories[i]
        food_type  = foods[i].find('td', class_="field field-name-field-food-types").text
        food_descr_sec = foods[i].find('td', class_="field field-name-field-description")
        food_descr = remove_sup_section(food_descr_sec)
        price_stud = foods[i].find('td', class_="field field-name-field-price-students").text
        price_emp  = foods[i].find('td', class_="field field-name-field-price-employees").text
        allFoods.append(Meal(category, food_type, food_descr, price_stud, price_emp))

    print("########################################")
    print("## Mensa plan University of Bremen") 
    print("##")
    print("## Today's date: " + datetime.datetime.now().strftime("%A, den %d.%m.%Y"))
    print("##")
    print("########################################\n")

    for fd in allFoods:
        Meal.printObj(fd)
        print("\n")

parse_and_print()