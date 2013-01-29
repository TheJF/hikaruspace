import bottle
from bottle import request, static_file, abort, response, jinja2_template as template
from pymongo import Connection
from beaker.middleware import SessionMiddleware
import requests
import json
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

echo_host = config.get('Hikaru-Echo', 'host')
echo_port = config.get('Hikaru-Echo', 'port')

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
except:
    print 'Mongo connection failure! Could not connect. Is Mongo running?'
    exit(0)

### ROUTES ###


@bottle.route('/')
def index():
    return template('views/index.tpl', login_bar=get_login_bar())


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
    return template('scripts/' + filename, login_name=get_login_name())


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


@bottle.route('/debug/gatekeeper')
def debug_gatekeeper():
    json_to_post = {'test': 'Okay, this seems to work.'}
    r = requests.post('http://' + host + ':' + str(port) + '/module/gatekeeper', data=json_to_post)
    return r.text


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


def speak(sentence):
    """ Send a sentence to the speech server """
    speech_url = 'http://' + echo_host + ':' + str(echo_port) + '/speak/' + sentence
    requests.get(speech_url)
    return speech_url

### RUN THE SERVER ###
bottle.run(server='paste', app=app, host=host, port=port)
