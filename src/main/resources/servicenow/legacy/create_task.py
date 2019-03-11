#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import com.xhaus.jyson.JysonCodec as json
import sys

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(tableName, "No tableName provided.")
assert_not_null(content, "No content provided.")

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

print "Sending content {}".format(content)

try:
    # create record in service now using queue table
    record_data = snClient.create_record(tableName, json.loads(content), getCurrentTask().getId())
    taskId = record_data["target_sys_id"]
    Task = record_data["target_record_number"]

    # find record using ticker number and show on UI
    data = snClient.find_record(table_name=tableName, query="number={}".format(Task))[0]
    print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(Task, taskId)
    print "\n"
    print snClient.format_record(data)
except Exception, e:
    print e
    print snClient.print_error(e)
    print "Failed to create record in Service Now"
    sys.exit(1)
