#!/bin/bash
PATH_TO_FILE="/home/home/my/RepoCode/avito/parser/html/new.txt"

gedit $PATH_TO_FILE

if [ -s $PATH_TO_FILE ]; then
    echo "$PWD"

    cd /home/home/my/RepoCode/avito/parser

    echo "$PWD"
    pipenv install
    pipenv --venv
    pipenv run python3 avito.py avito

    # docker exec -it avito-service.backend-1 pipenv run python manage.py collectstatic --noinput

    read -p "Press enter to continue"
else
    echo "File is empty" 
    read -p "Press enter to continue"
fi