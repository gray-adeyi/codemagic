# Alsaheem codemagic base for Rapid Forms
_______________

**Rapid Forms** is a web based dynamic form generator. (simply said it emulates what google form does).
**CodeMagic** is the base on which **Rapid Forms** is built on. It is designed using Django Framework

## Development Setup
You'll need to have python3 & pipenv installed. In your teminal, do.
`bash
$ cd codemagic
$ pipenv install
$ pipenv shell
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver
`
You'll need to populate your Transmitter model in the admin,
so create a superuser
`bash
$ ./manage.py createsuperuser --email example@domain.com`

After creating a Transmitter model instance navigate to 
[http://localhost:8000/demo](http://localhost:8000/demo) in your browser

## Current Contributors
1. Alsaheem
2. Gbenga