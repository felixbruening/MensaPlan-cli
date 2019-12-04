#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib.request  as urllib2 

URL="https://www.stw-bremen.de/de/mensa/uni-mensa"
PARSER='html.parser'
FOOD_CATEGORIES = ['Essen 1', 'Essen 2', 'Vegetarische Theke', 'Pfanne, Wok & Co.', 'Aufläufe & Gratin',
                    'Suppen', 'Veganes Wochenangebot, pro 100g Selbstbedienung', 'Pasta & Co.', 'Beilagen']


# Meal Class
class Meal:
    name = ""
    category=""
    description=""
    price=""

    def __init__(self, name, cat, descr, price):
        self.name=str(name)
        self.category=str(cat)
        self.description=str(descr)
        self.price=str(price)

    def printObj(self):
        string=str(self.name) + ": \n=================\n"
        string+="\n" + str(self.description) + "\n Preis:" + str(self.price)
        print(str(string))


# Function that parses the website and prits the meals of a day
def parse_and_print():
    allFoods = []

    html = urllib2.urlopen(URL)
    soup = BeautifulSoup(html, PARSER)


    foods = soup.findAll('table', class_='food-category')

    for i in range(0,9):
        category=FOOD_CATEGORIES[i]
        food_type=foods[i].find('td', class_="field field-name-field-food-types").text
        food_descr=foods[i].find('td', class_="field field-name-field-description").text
        price_stud=foods[i].find('td', class_="field field-name-field-price-students").text
        allFoods.append(Meal(category, food_type, food_descr, price_stud))

    print("############################################")
    print("###### Mensa plan University of Bremen #####")
    print("############################################\n\n")

    for fd in allFoods:
        Meal.printObj(fd)
        print("\n")


parse_and_print()