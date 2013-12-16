#!/bin/bash
uwsgi --socket :8001 --wsgi-file wsgi.py -d log.log