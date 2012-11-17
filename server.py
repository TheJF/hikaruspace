from bottle import route, get, post, request, run
from pymongo import Connection
import ConfigParser

### INITIALIZATION ###
# load configs
config = ConfigParser.ConfigParser()
config.read("server.cfg")

# set configs
host = config.get('Server', 'host')
port = config.getint('Server', 'port')
mongo_host = config.get('Mongo', 'host')
mongo_port = config.getint('Mongo', 'port')
mongo_db = config.get('Mongo', 'database')

# connect to Mongo
connection = Connection(mongo_host, mongo_port)
db = connection[mongo_db]

### ROUTES ###
@route('/')
def index():
	return 'Hikaruspace, under construction'


### RUN THE SERVER ###
run(host=host, port=port)