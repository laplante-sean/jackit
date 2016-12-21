#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***Create new venv***"; echo
    virtualenv --system-site-packages ./venv 
    source ./venv/bin/activate

    # Only upgrade on initial setup.
    pip3 install -r requirements.txt --upgrade
fi

python3 manage.py collectstatic

if [ ! -d "/home/protected/database" ];
then
    mkdir /home/protected/database
    chgrp web /home/protected/database
    chmod g+w /home/protected/database
fi

python3 manage.py migrate

if [ -f "/home/protected/database/db.sqlite3" ];
then
    chgrp web /home/protected/database/db.sqlite3
    chmod g+w /home/protected/database/db.sqlite3
else
    echo "ERROR: Could not modify permission on db file"
    exit 1
fi

exit 0