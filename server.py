import bottle
from bottle import request, static_file, abort, response, jinja2_template as template
from bottle.ext.tornadosocket import TornadoWebSocketServer
import tornado.websocket
from pymongo import Connection
from beaker.middleware import SessionMiddleware
import requests
import json
import ConfigParser
import hashlib

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
mongo_username = config.get('Mongo', 'username')
mongo_password = config.get('Mongo', 'password')

echo_host = config.get('Hikaru-Echo', 'host')
echo_port = config.get('Hikaru-Echo', 'port')

# get metas
app_name = config.get('Meta', 'name')
observing = config.get('Meta', 'observing')

# and the secret key
secret_key = config.get('Crypto', 'secret_key')

# set session options
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)

# connect to Mongo
try:
    connection = Connection(mongo_host, mongo_port)
    db = connection[mongo_db]
    db.authenticate(mongo_username, mongo_password)
except:
    print 'Mongo connection failure! Could not connect. Is Mongo running?'
    exit(0)


### ROUTES ###

@bottle.route('/')
def index():
    return template('views/index.tpl', template_info=get_template_info())


@bottle.get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='')

@bottle.route('/images/<filename:re:.*\.png>')
def serve_image(filename):
    return static_file(filename, root='images', mimetype='image/png')


@bottle.route('/styles/<filename:path>')
def serve_styles(filename):
    return static_file(filename, root='styles')


@bottle.route('/libs/<filename:path>')
def serve_libs(filename):
    return static_file(filename, root='libs')


# Scripts are JavaScript that are run through the templating engine, allowing for integration of values and such
@bottle.route('/scripts/<filename:path>')
def scripts(filename):
    response.content_type = 'text/javascript, charset=utf8'
    return template('scripts/' + filename, template_info=get_template_info())


# Receive an NFC UID and return if this card ID has access
@bottle.get('/module/gatekeeper')
@bottle.post('/module/gatekeeper')
def gatekeeper():
    test = request.forms.get('test')
    speech = speak(test)
    # Check if it's a valid gatekeeper request
    # Then verify if it's coming from a verified IP address and device
    # Validate the card UID against the access privilege list
    # If all is good, grant access
    # If not, deny access
    return speech


@bottle.post('/auth/login')
def login():
    # Check if the request has an assertion
    if 'assertion' not in request.forms:
        abort(400)

    # Send the assertion to Mozilla's verifier service
    data = {'assertion': request.forms.get('assertion'), 'audience': 'http://%s:%s' % (host, port)}
    resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)

    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)

        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Get the session object from the environ
            session = bottle.request.environ.get('beaker.session')

            # Log the user in by setting a secure session cookie
            session['email'] = verification_data['email']
            session.save()
            return resp.content

        # Oops, something failed. Abort.
        abort(500)


@bottle.post('/auth/logout')
def logout():
    session = bottle.request.environ.get('beaker.session')
    session.delete()

@bottle.get('/validate_card')
def validate_card():
    reader_id = request.query.get('reader_id')
    card_uid = request.query.get('card_uid')
    status = request.query.get('status')
    timestamp = request.query.get('timestamp')

    print "Reader ID: " + str(reader_id)
    print "Card UID: " + str(card_uid) 
    print "Status: " + str(status)
    print "Timestamp: " + str(timestamp)
    
    member = find_member_by_card_uid(card_uid)
    if member:
        hashed_time = hashlib.sha224()
        hashed_time.update(str(secret_key) + str(timestamp))
        validation_response = json.dumps({"access": "granted", 
                               "hashed_time": hashed_time.hexdigest()})
        # Update the dashboard with the relevant info
        door_opened_time = timestamp
        r = requests.get('http://'+host+':'+port+'/update_dashboard?widget=2&label=Door last opened&value='+door_opened_time+'&status=grey') 
    else:
        validation_response = json.dumps({"access": "denied"})
    
    print "Response: " + validation_response
    

    return validation_response

@bottle.get('/update_dashboard')
def update_dashboard():
    widget_num = request.query.get('widget')
    label = request.query.get('label')
    value = request.query.get('value')
    status = request.query.get('status')

    widget = {'command_type': 'dashboard_update', 'widget_num': widget_num, 'label': label, 'value': value, 'status': status}
    dashboard = update_dashboard(widget)

    # JSON string it up
    widget = json.dumps(widget)
    InterfaceDataHandler.broadcast(widget)

    return widget

### WEBSOCKETRY ###

class InterfaceDataHandler(tornado.websocket.WebSocketHandler):
    connections = []

    def open(self):
        print 'Client connected'
        # Add the connection to the list for global broadcasting purposes
        self.connections.append(self)

    def on_message(self, message):
        # Update the interface
        if message == "update":
            self.write_message('test')

    def on_close(self):
        print 'Client connection closed'
        # Clean up dead connections
        self.connections.remove(self)

    @classmethod
    def broadcast(self, message):
        print 'Broadcasting to all...'
        print self.connections
        for connection in self.connections:
            connection.write_message(message)
            print message

tornado_handlers = [
            (r"/interface_data", InterfaceDataHandler)
        ]


### HELPER FUNCTIONS ###

def is_logged_in():
    session = bottle.request.environ.get('beaker.session')
    logged_in = 'email' in session
    return logged_in


def get_login_name():
    session = bottle.request.environ.get('beaker.session')
    if is_logged_in():
        return session['email']
    else:
        return 'undefined'


def get_login_bar():
    if is_logged_in():
        login_bar = '<span id="logged_in">Logged in as ' + get_login_name() + '. <a href="#" id="signout">Log out</a></span>'
    else:
        login_bar = '<span id="logged_out"><a href="#" id="signin" class="persona-button green"><span>Sign in with your E-mail</span></a></span>'

    return login_bar

def get_template_info():
    template_info = {'login_name': get_login_name(), 
                     'host': host, 
                     'port': port,
                     'login_bar': get_login_bar(),
                     'app_name': app_name,
                     'observing': observing}
    return template_info

def speak(sentence):
    """ Send a sentence to the speech server """
    speech_url = 'http://' + echo_host + ':' + str(echo_port) + '/speak/' + sentence
    requests.get(speech_url)
    return speech_url

### DATABASE FUNCTIONS ####

# TODO: Abstract this into a library
def find_member_by_card_uid(card_uid):
    member = db.members.find_one({"card_uid":card_uid})
    return member

def update_dashboard(widget):
    return 'Not yet done'

### RUN THE SERVER ###
bottle.run(server=TornadoWebSocketServer, handlers=tornado_handlers, reloader=True, app=app, host=host, port=port)
