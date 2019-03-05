#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(number, "No number provided.")
assert_not_null(fieldNames,"No field names provided.")


servicenow_client = ServiceNowClient.create_client(servicenowServer, username, password)
change_request = servicenow_client.get_record_with_fields(tableName, number, fieldNames)

rows = []
row = []
for field in fieldNames:
    row.append(change_request[field])
rows.append(row)
servicenow_client.print_table(fieldNames, rows)
