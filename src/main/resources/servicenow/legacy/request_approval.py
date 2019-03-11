#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import sys, traceback, time
import com.xhaus.jyson.JysonCodec as json
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null


assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(content, "No content provided.")
assert_not_null(shortDescription, "No shortDescription provided.")
assert_not_null(description, "No description provided.")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
content_json = content % (shortDescription, description)
sysId = None

try:
    # create a new record in service now using queue table
    record_data = sn_client.create_record(tableName, json.loads(content_json), getCurrentTask().getId())
    sysId = record_data["target_sys_id"]
    ticket = record_data["target_record_number"]

    # find record using ticker number and show on UI
    data = sn_client.find_record(table_name=tableName, query="number={}".format(ticket))[0]
    print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(ticket, sysId)
except Exception as e:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print sn_client.print_error(e)
    print "Failed to create record in Service Now"
    sys.exit(1)


is_clear = False
while not is_clear:
    try:
        data = sn_client.get_record(tableName, sysId)
        status = data["approval"]
        print "Found %s in Service Now as %s" % (data['number'], status)
        if "approved" == status.lower():
            is_clear = True
            print "ServiceNow approval received."
        elif "rejected" == status.lower():
            print "Failed to get approval from ServiceNow"
            sys.exit(1)
        else:
            time.sleep(5)
    except Exception as e:
        print sn_client.print_error(e)
        print "Error finding status for {}".format(sysId)
