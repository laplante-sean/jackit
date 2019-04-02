#!/bin/bash

if [ -d "venv" ];
then
    echo; echo "***Activate existing venv***"; echo
    source ./venv/bin/activate
else
    echo; echo "***Create new venv***"; echo
    python3 -m venv ./venv
    source ./venv/bin/activate

    # Get the latest pip
    python -m pip install --upgrade pip

    # Only upgrade on initial setup.
    pip install -r requirements.txt
fi

python manage.py migrate
python manage.py runserver

exit 0