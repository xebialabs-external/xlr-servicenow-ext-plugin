#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import com.xhaus.jyson.JysonCodec as json

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

# create record in service now using queue table
record_data = sn_client.create_record(tableName, json.loads(content), getCurrentTask().getId())
sysId = record_data["target_sys_id"]
Ticket = record_data["target_record_number"]

# find record using ticker number and show on UI
data = sn_client.find_record(table_name=tableName, query="number={}".format(Ticket))[0]
print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(Ticket, sysId)
print sn_client.format_record(data)
