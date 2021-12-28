# MensaPlan Python3 Script
This python-script prints the todays meals of the Uni-Bremen Mensa or of the Cafe Unique on the central campus.

Following options are available:

    -h, --help      show this help message and exit 
    -q, --quiet     shows only main meals 
    -m, --mensa     prints meals of mensa uni bremen 
    -u, --unique    prints meals of cafe unique 
    -a, --show-all  prints meals of cafe unique and uni-mensa 



# Required python3-libraries
$ pip3 install `BeautifulSoup` 

$ pip3 install `bs4`

# Usage
$ python3 `mensaplan.py` [options]

*It is recommended to pipe the output to `less` or `more` because the program output may be a bit long.*
