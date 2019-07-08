#! /usr/bin/python3.7
import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pritam/Documents/Sewa/')
from Sewa.myapp import app as application
