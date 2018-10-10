import logging
logging.getLogger().setLevel(logging.INFO)
import sys
import base64
import hashlib
import os

from flask import Flask, abort, make_response, jsonify, url_for, request, json, send_from_directory, send_file
from avatar.model import AvatarModel
from flask_jsontools import jsonapi
from dateutil import parser
import datetime

from rest_utils import register_encoder
from avatar.model import obtener_session

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']


from warden.sdk.warden import Warden
warden_url = os.environ['WARDEN_API_URL']
warden = Warden(OIDC_URL, warden_url, client_id, client_secret, verify=VERIFY_SSL)

API_BASE=os.environ['API_BASE']

app = Flask(__name__)
app.debug = True
register_encoder(app)

DEBUGGING = bool(int(os.environ.get('VSC_DEBUGGING',0)))
def configurar_debugger():
    """
    para debuggear con visual studio code
    """
    if DEBUGGING:
        print('Iniciando Debugger PTVSD')
        import ptvsd
        #secret = os.environ.get('VSC_DEBUG_KEY',None)
        port = int(os.environ.get('VSC_DEBUGGING_PORT', 5678))
        ptvsd.enable_attach(address=('0.0.0.0',port))

configurar_debugger()


# @app.route(API_BASE + '/avatar/', methods=['GET'], defaults={'hash':None})
@app.route(API_BASE + '/avatar/<hash>', methods=['GET'])
def obtener_avatar_binario(hash):

    with obtener_session() as s:
        avatar = AvatarModel.obtener_avatar(session=s, hash=hash)
    b64 = bool(request.args.get('b64',False))

    if not b64:
        r = make_response()
        r.status_code = 200
        r.data = base64.b64decode(avatar.data)
        r.headers['Content-Type'] = avatar.content_type
        return r
    else:
        return avatar.data

@app.route(API_BASE + '/avatar/<hash>', methods=['PUT','POST'])
@jsonapi
def agregar_actualizar_avatar(hash):
    data = request.get_json()
    avatar = data['avatar']
    ''' agrego el avatar en la base en base64 '''
    return ({status:200}, 200)

"""

@app.route(API_BASE + '/avatar/<hash>', methods=['PUT','POST'])
@warden.require_valid_token
@jsonapi
def agregar_avatar(hash, token=None):
    f = request.files['file']
    contenido = base64.b64encode(f.read()).decode('utf-8')
    UsersModel.actualizar_avatar(hash, contenido)
    return {'status':'OK','status_code':200}, 200

@app.route(API_BASE + '/usuarios/<uid>/avatar/', methods=['PUT','POST'])
@warden.require_valid_token
@jsonapi
def agregar_avatar_por_usuario(uid, token=None):
    h = hashlib.md5(uid.encode()).hexdigest()
    return agregar_avatar(h)

@app.route(API_BASE + '/usuarios/<uid>/avatar/.json', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_avatar_por_usuario(uid, token=None):
    h = hashlib.md5(uid.encode()).hexdigest()
    return obtener_avatar(h)

@app.route(API_BASE + '/usuarios/<uid>/avatar/', methods=['GET'])
def obtener_avatar_binario_por_usuario(uid, token=None):
    h = hashlib.md5(uid.encode()).hexdigest()
    return obtener_avatar_binario(h)

"""



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET','POST','PUT','PATCH'])
def catch_all(path):
    return ('no permitido', 401)

if DEBUGGING:
    @app.before_request
    def br():
        logging.info(request)

@app.route(API_BASE + '*', methods=['OPTIONS'])
def options():
    if request.method == 'OPTIONS':
        return 204
    return 204

def cors_after_request(response):
    if not response.headers.get('Access-Control-Allow-Origin',None):
        response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.after_request
def add_header(r):
    r = cors_after_request(r)
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


'''
@app.route('/rutas', methods=['GET'])
@jsonapi
def rutas():
    links = []
    for rule in app.url_map.iter_rules():
        url = url_for(rule.endpoint, **(rule.defaults or {}))
        links.append(url)
    return links
'''

def main():
    app.run(host='0.0.0.0', port=10102, debug=False)

if __name__ == '__main__':
    main()
