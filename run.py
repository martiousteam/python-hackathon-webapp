import sys
import logging
logging.basicConfig(stream=sys.stderr)

# sys.path.insert(0,"/var/www/python/python-hackathon-webapp/")

# If you get error hackathon cannot be found, enable the commented path statement above. change path to the folder in which you have this file.
from hackathon import app as application

application.run(host='0.0.0.0', port='5000', debug=True)
