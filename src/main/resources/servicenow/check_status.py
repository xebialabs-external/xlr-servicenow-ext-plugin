import sys
import com.xhaus.jyson.JysonCodec as json
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null


assert_not_null(servicenowServer, "No server provided.")
assert_not_null(statusField, "No statusField provided.")
assert_not_null(tableName, "No tableName provided.")
assert_not_null(sysId, "No sysId provided.")

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

try:
    data = snClient.get_change_request(tableName, sysId)
    status = data[statusField]
    ticket = data['number']
    print "Found {} in Service Now.".format(sysId)
    print json.dumps(data, indent=4, sort_keys=True)
except:
    print snClient.print_error(e)
    print "Error finding status for {}".format(statusField)
    sys.exit(1)

