#!/bin/bash
uwsgi --socket :8002 --wsgi-file wsgi.py -d log.log