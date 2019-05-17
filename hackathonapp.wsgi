import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/python/python-hackathon-webapp/")

from hackathon import app as application
