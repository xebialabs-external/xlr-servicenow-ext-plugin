#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(number, "Ticket is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

data = sn_client.find_record(tableName, "number=%s" % (number))
numRecords = len(data)
print "Found %s records for %s" % (numRecords, number)
data = data[0]
sysId = data["sys_id"]
print "Found %s in Service Now with sysId = %s.\n" % (number, sysId)
print sn_client.format_record(data)
