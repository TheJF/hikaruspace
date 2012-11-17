from bottle import route, get, post, request, run, static_file, jinja2_template as template
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
	return template('views/index.tpl')

@route('/images/<filename:re:.*\.png>')
def serve_image(filename):
	return static_file(filename, root='images', mimetype='image/png')

@route('/styles/<filename:path>')
def serve_styles(filename):
	return static_file(filename, root='styles')

@route('/js/<filename:path>')
def serve_js(filename):
	return static_file(filename, root='js')


### RUN THE SERVER ###
run(host=host, port=port)