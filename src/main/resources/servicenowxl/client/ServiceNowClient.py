import sys
import urllib
import com.xhaus.jyson.JysonCodec as json
from xlrelease.HttpRequest import HttpRequest
import time
SUCCESS_STATUS_CODE = 200
RECORD_CREATED_STATUS = 201


class ServiceNowClient(object):
    def __init__(self, httpConnection, username=None, password=None):
        self.headers = {}
        self.accessToken = None
        self.refreshToken = None
        self.httpConnection = httpConnection
        self.useOAuth = httpConnection['useOAuth']
        if username:
            self.httpConnection['username'] = username
        if password:
            self.httpConnection['password'] = password
        self.httpRequest = HttpRequest(self.httpConnection, username, password)
        self.sysparms = 'sysparm_display_value=%s&sysparm_input_display_value=%s' % (
            self.httpConnection['sysparmDisplayValue'], self.httpConnection['sysparmInputDisplayValue'])

    @staticmethod
    def create_client(httpConnection, username=None, password=None):
        return ServiceNowClient(httpConnection, username, password)

    def issue_token(self):
        print "Issuing a new token"
        tokenData = self.create_token(self.httpConnection)
        self.accessToken = tokenData['access_token']
        self.refreshToken = tokenData['refresh_token']
        self.headers['Authorization'] = "Bearer %s" % (self.accessToken)

    def create_token(self, httpConnection):
        servicenow_oauth_url = "/oauth_token.do"
        content = {'grant_type': 'password', 'client_id': httpConnection['clientId'],
                   'client_secret': httpConnection['clientSecret'],
                   'username': httpConnection['oauthUsername'], 'password': httpConnection['oauthPassword']}
        httpRequest = HttpRequest(httpConnection, None, None)
        response = httpRequest.post(servicenow_oauth_url, body=urllib.urlencode(content),
                                    contentType='application/x-www-form-urlencoded')
        if response.getStatus() == SUCCESS_STATUS_CODE:
            data = json.loads(response.getResponse())
            return data
        print 'Could not get access token'
        self.throw_error(response)

    def revoke_token(self):
        print "Revoking token"
        httpRequest = HttpRequest(self.httpConnection, None, None)
        servicenowApiUrl = "/oauth_revoke_token.do?token=%s" % self.accessToken
        response = httpRequest.get(servicenowApiUrl)
        servicenowApiUrl = "/oauth_revoke_token.do?token=%s" % self.refreshToken
        response = httpRequest.get(servicenowApiUrl)

    def format_record(self, myObj, outStr="", prefix="", header=True):
        if header:
            outStr = "%s| Key | Value |\n" % (outStr)
            outStr = "%s| --- | --- |\n" % (outStr)
        if type(myObj) is dict:
            for key in myObj.iterkeys():
                value = myObj[key]
                if type(value) is dict or type(value) is list:
                    p = "%s%s." % (prefix, key)
                    outStr = "%s| %s%s |\n%s" % (outStr, prefix, key, self.format_record(value, "", p, False))
                else:
                    p = "%s%s" % (prefix, key)
                    outStr = "%s| %s%s |%s |\n" % (outStr, prefix, key, value)
        elif type(myObj) is list:
            for value in myObj:
                outStr = "%s| | %s\n" % (outStr, value)
        else:
            outStr = "%s%s" % (outStr, myObj)
        return outStr

    def print_table(self, headers, rows):
        print "\n|", "|".join(headers), "|"
        print "|", " ------ |" * len(headers)
        for r in rows:
            print "| ", "  |".join(r), " |"
        print "\n"

    def print_error(self, response):
        if type(response) is dict:
            outStr =   "| Status  | %s |\n" % ( response["status"] )
            outStr = "%s| Message | %s |\n" % ( outStr, response["error"]["message"] )
            outStr = "%s| Detail  | %s |\n" % ( outStr, response["error"]["detail"] )
            return outStr
        return response

    def get_change_request_states(self):
        servicenow_api_url = '/api/now/v1/table/%s?element=state&name=task&sysparm_fields=%s&%s' % (
        'sys_choice', 'value,label', self.sysparms)
        return self.request(method='GET', url=servicenow_api_url, headers=self.headers)

    def create_record(self, table_name, content):
        servicenow_api_url = '/api/now/v1/table/%s?%s' % (table_name, self.sysparms)
        return self.request(method='POST', url=servicenow_api_url, body=content, headers=self.headers)

    def find_record(self, table_name, query):
        servicenow_api_url = '/api/now/v1/table/%s?%s&%s' % (table_name, query, self.sysparms)
        return self.request(method='GET', url=servicenow_api_url, headers=self.headers)

    def update_record(self, table_name, sysId, content):
        servicenow_api_url = '/api/now/v1/table/%s/%s?%s' % (table_name, sysId, self.sysparms)
        return self.request(method='PUT', url=servicenow_api_url, body=content, headers=self.headers)

    def get_change_request(self, table_name, sys_id):
        servicenow_api_url = '/api/now/v1/table/{}/{}?{}'.format(table_name, sys_id, self.sysparms)
        return self.request(method='GET', url=servicenow_api_url, headers=self.headers)

    def get_change_request_with_fields(self, table_name, number, fields):
        servicenow_api_url = '/api/now/v1/table/%s?number=%s&sysparm_fields=%s&%s' % (table_name, number, ",".join(fields), self.sysparms)
        response = self.httpRequest.get(servicenow_api_url, contentType='application/json', headers = self.headers)
        if self.useOAuth :self.revoke_token()

        if response.getStatus() == SUCCESS_STATUS_CODE:
            data = json.loads(response.getResponse())
            if len(data['result']) == 1:
                return data['result'][0]
        self.throw_error(response)

    def wait_for_approval(self, table_name, sys_id):
        is_clear = False
        while not is_clear:
            try:
                data = self.get_change_request(table_name, sys_id)
                status = data["approval"]
                print "Found %s in Service Now as %s" % (data['number'], status)
                if "Approved" == status:
                    is_clear = True
                    print "ServiceNow approval received."
                elif "rejected" == status:
                    print "Failed to get approval from ServiceNow"
                    sys.exit(1)
                else:
                    time.sleep(5)
            except:
                print json.dumps(data, indent=4, sort_keys=True)
                print "Error finding status for {}".format(sys_id)

    def request(self, method, url, headers, content_type='application/json', body=None):
        print "Service Now URL = %s \n" % (url)
        if self.useOAuth: self.issue_token()
        if method == 'GET':
            response = self.httpRequest.get(url, contentType=content_type, headers=headers)
        elif method == 'PUT':
            response = self.httpRequest.put(url, body=body, contentType=content_type, headers=headers)
        else:
            response = self.httpRequest.post(url, body=body, contentType=content_type, headers=headers)
        if self.useOAuth: self.revoke_token()
        if response.getStatus() == SUCCESS_STATUS_CODE or response.getStatus() == RECORD_CREATED_STATUS:
            try:
                data = json.loads(response.getResponse())
                return data['result']
            except:
                print response.getResponse()
                raise RuntimeError("Cannot convert to json")
        else:
            print response.getResponse()
            self.throw_error(response)

    def throw_error(self, response):
        print "Error from ServiceNow, HTTP Return: %s\n" % (response.getStatus())
        print "Detailed error: %s\n" % response.response
        if self.useOAuth: self.revoke_token()
        sys.exit(1)

    def EmptyToNone(self, value):
        if value is None or value.strip() == '':
            return None
        else:
            return value
