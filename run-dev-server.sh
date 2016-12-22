#!/bin/bash

PORT=5042

/home/santa/.virtualenvs/piriti/bin/uwsgi  --http 0.0.0.0:$PORT --http-websockets --virtualenv /home/santa/.virtualenvs/piriti --master --processes 1 --wsgi piriti.app:app --python-autoreload 1 --gevent 100 --enable-threads  
