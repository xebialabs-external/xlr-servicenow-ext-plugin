#!flask/bin/python
#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import os, io, json


app = Flask(__name__)
handler = RotatingFileHandler('/var/log/cherwell.log', maxBytes=1000000, backupCount=1)
logger_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
handler.setFormatter(logger_formatter)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

tokenList = ["THIS_IS_A_TOKEN_1", "THIS_IS_A_TOKEN_2", "THIS_IS_A_TOKEN_3", "THIS_IS_A_TOKEN_4", "THIS_IS_A_TOKEN_5"]
tokenIndexCounter = 0
pollingCounter = 0


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

def getFile( fileName ):
     filePath="/mockserver/responses/%s" % fileName
     F = open(filePath, "r")
     resp = make_response( F.read() )
     resp.headers['Content-Type'] = 'application/json'
     return resp

def requires_auth(f):
    """
    Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        global tokenList
        if token not in tokenList:
          raise AuthError({"code": "invalid_header", "description": "Unable to find appropriate key"}, 400)
        return f(*args, **kwargs)

    return decorated

def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description": "Authorization header is expected"}, 401)
    else:
        app.logger.info('Authorization from the header: %s' % auth)

    parts = auth.split()
    app.logger.info('parts[0]: %s' % parts[0])
    app.logger.info('parts[1]: %s' % parts[1])

    if parts[0] != "Bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with BEARER"}, 401)
    token = parts[1]
    return token


@app.route('/')
def index():
     logRequest(request)
     return "Hello, World!"


@app.route('/api/now/table/u_request_task', methods=['POST'])
@requires_auth
def save_business_object():
     logRequest(request)
     auth = request.headers.get("Authorization", None)
     content = request.json
     return getFile("createRTask.json")
     

@app.route('/token', methods=['POST'])
def get_access_token():
     logRequest(request)
     global tokenIndexCounter
     auth_mode = request.args.get("auth_mode")
     client_id = request.form.get("client_id")
     password =request.form.get("password")
     grant_type = request.form.get("grant_type")
     username =request.form.get("username")
     
     if username == "USERNAME" and password == "PASSWORD" and client_id == "API_KEY":
        app.logger.info("About to return the access token")
        app.logger.debug("Before Increment - tokenIndexCounter = %s" % str(tokenIndexCounter)) 
        app.logger.debug("About to return a token - %s" % (tokenList[tokenIndexCounter])) 
        resp = {'access_token': tokenList[tokenIndexCounter], 'expires_in': 60}
        if tokenIndexCounter >= (len(tokenList) -1):
             tokenIndexCounter = 0
        else:
             app.logger.debug("About to increment counter")
             tokenIndexCounter += 1

        return json.dumps(resp)
     else:
        app.logger.error("Credentials are invalid")  
        raise AuthError({"code": "credentials_invalid",
                        "description": "Credentials are invalid"}, 403)

def logRequest(request):
     app.logger.debug("**************** LOGGING REQUEST")
     app.logger.debug("request.url=%s" % request.url)
     app.logger.debug("request.headers=%s" % request.headers )
     if request.json:
          app.logger.debug("request.json=%s" % request.json)
     else:
          app.logger.debug("request.data=%s" % request.data)
     app.logger.debug("request.form=%s" % request.form)
     app.logger.debug("****************")


if __name__ == '__main__':
     app.run(debug=True)   
