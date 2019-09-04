#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import sys

from servicenow import get_deep_link_url, add_code_compliance_record
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(number, "No number provided.")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
change_request = sn_client.find_record(tableName, 'number=%s' % number)[0]
status = change_request["approval"]
print "Found {} in Service Now as {}".format(change_request['number'], status)

if "approved" == status.lower():
    approval = False
    isClear = True
    print "ServiceNow approval received."
elif "rejected" == status:
    print "Failed to get approval from ServiceNow"
    sys.exit(1)

if change_request['state'] in expectedStatus:
    print "Change Request {} is in required state\n".format(number)
else:
    print "Change Request {} is NOT in required state\n".format(number)
    sys.exit(1)

add_code_compliance_record(table_name=tableName,
                          task_reporting_api=taskReportingApi,
                          task=task,
                          service_now_server=servicenowServer,
                          service_now_user=username,
                          data=change_request,
                          url=get_deep_link_url(sn_client.service_now_url, tableName, change_request['sys_id']))
data = change_request
