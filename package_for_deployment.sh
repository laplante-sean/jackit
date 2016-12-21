#!/bin/sh

# Make sure they're in the directory with django manage.py
if [ ! -f "./jackitio/manage.py" ];
then
    echo; echo "You're in the wrong directory"; echo
    exit 1
fi

# Make sure the parent directory is for jackitio
if [ ! -d "../jackit" ];
then
    echo; echo "You're in the wrong directory"; echo
    exit 1
fi

staging="/tmp/jackitio_staging"
package_file="deploy_jackit.io.tar.gz"

if [ ! -d $staging ];
then
    #echo "mkdir $staging"
    mkdir $staging
fi

for f in `ls`;
do
    if [ -d $f ];
    then
        echo "cp -R $f $staging"
        #cp -R $f $staging
    fi

    if [ -f $f ];
    then
        echo "cp $f $staging"
        #cp $f $staging
    fi
done

# Tar up the staging directory
echo "tar -zcvf $package_file $staging"
#tar -zcvf $package_file $staging 

exit 0