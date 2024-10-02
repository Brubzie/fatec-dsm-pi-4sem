# CafeTech | PI do 4º semestre de 2024 | DSM - Fatec Araras

A aplicação "CafeTech" é uma plataforma desenvolvida em Django com o objetivo de facilitar o processo de controle de pagamento para a manutenção contínua do clube do café.

## Participantes

<p align="center">
  <a href="https://github.com/marquesluana">
    <img src="https://avatars.githubusercontent.com/marquesluana" width="15%">
  </a>
  <a href="https://github.com/Brubzie">
    <img src="https://avatars.githubusercontent.com/Brubzie" width="15%">
  </a>
</p>

## Tecnologias utilizadas

<div>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg" width="50px">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-plain-wordmark.svg" width="50px">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original-wordmark.svg" width="50px">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-plain-wordmark.svg" width="50px">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original-wordmark.svg" width="50px">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original-wordmark.svg" width="50px">
</div>

## COMO RODAR ESSE PROJETO?

No ambiente Linux:

```console
git clone https://github.com/Brubzie/fatec-dsm-pi-4sem
cd CafeTech/
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
coverage run --source='.' manage.py test 
coverage html
python manage.py runserver
```

No ambiente Windows:

```console
git clone https://github.com/Brubzie/fatec-dsm-pi-4sem
cd CafeTech/
virtualenv venv
cd venv
cd scripts
activate.bat
cd ..
cd ..
pip install -r requirements.txt
python manage.py migrate
python manage.py test
coverage run --source='.' manage.py test 
coverage html
python manage.py runserver

```
