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

echo "Checking required packages...."
echo "INSTALLED:"
if ! pip list | grep -F bs4
then
    echo "Installing 'bs4' ..."
    pip install bs4
fi

echo "Install scripts ..."
touch $RUN_SCRIPT
echo "#!/bin/bash" >> $RUN_SCRIPT
echo "python3 $PWD/mensaplan.py | less" >> $RUN_SCRIPT
chmod +x $RUN_SCRIPT
echo "Link executable...."
ln -s $RUN_SCRIPT $EXECUTABLE
