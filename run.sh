#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:10000 'toolbox:create_app()'