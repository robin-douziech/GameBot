#!/bin/bash

if [ -d venv ]
then
	echo "removing virtual environment"
	rm -r venv
fi

echo "creating new virtual environment"
python -m venv venv

echo "activating environment"
source venv/bin/activate


echo "installing dependencies"
pip install -r requirements.txt

echo "runing bot"
python src/run.py
