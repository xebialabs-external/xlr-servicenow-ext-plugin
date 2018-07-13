
import sys
import urllib
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest

SUCCESS_STATUS_CODE     = 200

class ServiceNowClient(object):
    def __init__(self, httpConnection, username=None, password=None): 
        self.headers        = {}
        self.accessToken    = None
        self.refreshToken   = None
        self.httpConnection = httpConnection
        self.useOAuth = httpConnection['useOAuth']
        if username:
           self.httpConnection['username'] = username
        if password:
           self.httpConnection['password'] = password
        self.httpRequest = HttpRequest(self.httpConnection, username, password)
        self.sysparms = 'sysparm_display_value=%s&sysparm_input_display_value=%s' % (self.httpConnection['sysparmDisplayValue'], self.httpConnection['sysparmInputDisplayValue'])

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return ServiceNowClient(httpConnection, username, password)

    def throw_error(self, response):
        print "Error from ServiceNow, HTTP Return: %s\n" % (response.getStatus())
        print "Detailed error: %s\n" % response.response
        if self.useOAuth :self.revoke_token()
        sys.exit(1)

    def EmptyToNone(self,value):
        if value is None or value.strip() == '':
           return None
        else:
            return value

    def issue_token(self):
        print "Issuing a new token"
        tokenData = self.create_token(self.httpConnection)
        self.accessToken  = tokenData['access_token']
        self.refreshToken = tokenData['refresh_token']
        self.headers['Authorization'] = "Bearer %s" % (self.accessToken)

    def create_token(self, httpConnection):
        servicenow_oauth_url     = "/oauth_token.do"
        content                  = {'grant_type': 'password', 'client_id':httpConnection['clientId'] , 'client_secret':httpConnection['clientSecret'],
                                    'username':httpConnection['oauthUsername'], 'password':httpConnection['oauthPassword']}
        httpRequest              = HttpRequest(httpConnection, None, None)
        response                 = httpRequest.post(servicenow_oauth_url, body=urllib.urlencode(content), contentType='application/x-www-form-urlencoded')
        if response.getStatus() == SUCCESS_STATUS_CODE:
            data = json.loads(response.getResponse())
            return data
        print 'Could not get access token'
        self.throw_error(response)

    def get_change_request_states(self):
        if self.useOAuth : self.issue_token()
        servicenow_api_url = '/api/now/v1/table/%s?element=state&name=task&sysparm_fields=%s&%s' % ('sys_choice', 'value,label', self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()
        if response.getStatus() == SUCCESS_STATUS_CODE:
            data = json.loads(response.getResponse())
            return data['result']
        self.throw_error(response)
