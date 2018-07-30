import sys
from servicenowxl.client.ServiceNowClient import ServiceNowClient
from servicenowxl.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(number, "No number provided.")

snClient = ServiceNowClient.create_client(servicenowServer, username, password)
change_request = snClient.get_change_request_with_fields(tableName, number, ['state', 'approval', 'number'])
print change_request
status = change_request["approval"]
print "Found {} in Service Now as {}".format(change_request['number'], status)

if "approved" == status:
    approval = False
    isClear = True
    print "ServiceNow approval received."
elif "rejected" == status:
    print "Failed to get approval from ServiceNow"
    sys.exit(1)

if change_request['state'] not in expectedStatus:
    print "Change Request {} is in required state\n".format(number)
else:
    print "Change Request {} is NOT in required state\n".format(number)
    sys.exit(1)


print "\n"
print snClient.format_record(change_request)
