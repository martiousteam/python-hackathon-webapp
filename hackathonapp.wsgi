import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/python/hackathon/")

from hackathonapp import app as application
