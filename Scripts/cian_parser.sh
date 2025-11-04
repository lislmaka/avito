#!/bin/bash
PATH_TO_FILE="/home/home/my/RepoCode/avito/parser/html/new.txt"
echo "Open file"
gedit $PATH_TO_FILE
echo "Close fiile"

echo "$PWD"

cd /home/home/my/RepoCode/avito/parser

echo "$PWD"
pipenv install
pipenv --venv
pipenv run python3 avito.py cian
# cd /home/home/my/RepoCode/avito/backend

docker exec -it avito-service.backend-1 pipenv run python manage.py collectstatic --noinput

read -p "Press enter to continue"