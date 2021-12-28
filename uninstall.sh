#!/bin/bash

# --------------------------------
# Uninstall script for Mensaplan
#
# (c) by Felix Bruening
# --------------------------------

RUN_SCRIPT="/usr/local/bin/mensa.sh"
EXECUTABLE="/usr/local/bin/mensa"

sudo unlink EXECUTABLE
sudo rm -rf RUN_SCRIPT
