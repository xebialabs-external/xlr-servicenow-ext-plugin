#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import com.xhaus.jyson.JysonCodec as json
import sys

from servicenow import get_deep_link_url, add_code_compliance_record
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(statusField, "No statusField provided.")
assert_not_null(tableName, "No tableName provided.")
assert_not_null(sysId, "No sysId provided.")

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

try:
    data = snClient.get_record(tableName, sysId)
    status = data[statusField]
    ticket = data['number']
    print "Found {} in Service Now.".format(sysId)
    print json.dumps(data, indent=4, sort_keys=True)

    add_code_compliance_record(table_name=tableName,
                              task_reporting_api=taskReportingApi,
                              task=task,
                              service_now_server=servicenowServer,
                              service_now_user=username,
                              data=data,
                              url=get_deep_link_url(snClient.service_now_url, tableName, sysId))
except Exception as e:
    print snClient.print_error(e)
    print "Error finding status for {}".format(statusField)
    sys.exit(1)
