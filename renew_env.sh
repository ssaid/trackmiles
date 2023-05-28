#!/bin/bash
dc down -v
dc build
dc exec server python3 manage.py migrate
dc exec server python3 manage.py createsuperuser
