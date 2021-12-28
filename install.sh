#!/bin/bash

# --------------------------------
# Install script for Mensaplan
#
# (c) by Felix Bruening
# --------------------------------

RUN_SCRIPT="/usr/local/bin/mensa.sh"
EXECUTABLE="/usr/local/bin/mensa"

echo "################################"
echo "Please install"
echo "-> python3"
echo "-> pip"
echo "################################"

if ! pip list | grep -F bs4
then
    echo "Installing 'bs4' ..."
    pip install bs4
fi

sudo touch RUN_SCRIPT
sudo echo "#!/bin/bash" >> RUN_SCRIPT
sudo echo "python3 $PWD/mensaplan.py | less" >> RUN_SCRIPT
sudo chmod +x RUN_SCRIPT
sudo ln -s RUN_SCRIPT EXECUTABLE
