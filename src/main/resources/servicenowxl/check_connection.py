from servicenowxl.client.ServiceNowClient import ServiceNowClient
params = {
    'url': configuration.url, 'username': configuration.username
    , 'password': configuration.password, 'useOAuth': configuration.useOAuth
    , 'oauthUsername': configuration.oauthUsername, 'oauthPassword': configuration.oauthPassword
    , 'clientId': configuration.clientId, 'clientSecret': configuration.clientSecret
    , 'proxyHost': configuration.proxyHost, 'proxyPort': configuration.proxyPort
    , 'sysparmDisplayValue': configuration.sysparmDisplayValue
    , 'sysparmInputDisplayValue': configuration.sysparmInputDisplayValue
}

sn_client = ServiceNowClient.create_client(params)
content = None

data = sn_client.get_change_request_states()
