import sys
import time
import traceback
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(sysId, "No sysId provided.")
assert_not_null(tableName, "No tableName provided.")
assert_not_null(pollInterval, "No pollInterval provided.")
assert_not_null(checkForStatus, "No check status provided.")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
data = ""

while True:
    try:
        data = sn_client.get_change_request(tableName, sysId)
        status = data[statusField]
        print "Found [{}] in Service Now with status: [{}] Looking for {}\n".format(data['number'], status, checkForStatus)
        if status == checkForStatus:
            status = data[statusField]
            ticket = data["number"]
            break
    except Exception, e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        print e
        print sn_client.print_error(e)
        print "Error finding status for %s" % statusField
    time.sleep(pollInterval)

print "\n"
print sn_client.format_record(data)
