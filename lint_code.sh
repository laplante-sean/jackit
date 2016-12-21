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

echo; echo "***Pip install pylint***"; echo
pip3 install -I pylint

echo; echo "***Pylinting***"; echo
pylint --rcfile=./.pylintrc ./jackitio ./jackit
err=$?

if [ $err -ne 0 ];
then
    echo; echo "***Linting failed with exit code: $err***"; echo
    exit $err
else
    echo; echo "***Linting passed***"; echo
fi

exit 0