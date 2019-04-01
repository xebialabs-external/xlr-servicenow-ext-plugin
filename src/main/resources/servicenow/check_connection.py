#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow.client.ServiceNowClient import ServiceNowClient

params = {
    'url': configuration.url,
    'username': configuration.username,
    'password': configuration.password,
    'useServicenowApp': configuration.useServicenowApp,
    'useOAuth': configuration.useOAuth,
    'oauthUsername': configuration.oauthUsername,
    'oauthPassword': configuration.oauthPassword,
    'clientId': configuration.clientId,
    'clientSecret': configuration.clientSecret,
    'proxyHost': configuration.proxyHost,
    'proxyPort': configuration.proxyPort,
    'proxyUsername': configuration.proxyUsername,
    'proxyPassword': configuration.proxyPassword,
    'sysparmDisplayValue': configuration.sysparmDisplayValue,
    'sysparmInputDisplayValue': configuration.sysparmInputDisplayValue
}

sn_client = ServiceNowClient.create_client(params)
content = sn_client.check_connection()
