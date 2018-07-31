import sys, traceback
import com.xhaus.jyson.JysonCodec as json
from servicenowxl.client.ServiceNowClient import ServiceNowClient
from servicenowxl.helper.helper import assert_not_null


assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(content, "No content provided.")
assert_not_null(shortDescription, "No shortDescription provided.")
assert_not_null(description, "No description provided.")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
content_json = content % (shortDescription, description)
sysId = None

print "Sending content {}".format(content_json)

try:
    data = sn_client.create_record(tableName, content_json)
    print "Returned DATA = {}".format(data)
    print json.dumps(data, indent=4, sort_keys=True)
    sysId = data["sys_id"]
    ticket = data["number"]
    print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(ticket, sysId)
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print e
    print sn_client.print_error(e)
    print "Failed to create record in Service Now"
    sys.exit(1)

sn_client.wait_for_approval(tableName, sysId)