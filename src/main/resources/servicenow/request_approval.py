import sys, traceback
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

print "Sending content {}".format(content_json)

try:
    # create a new record in service now using queue table
    record_data = sn_client.create_record(tableName, json.loads(content_json))
    print "Returned DATA = {}".format(record_data)
    print json.dumps(record_data, indent=4, sort_keys=True)
    sysId = record_data["target_sys_id"]
    ticket = record_data["target_record_number"]

    # find record using ticker number and show on UI
    data = sn_client.find_record(table_name=tableName, query="number={}".format(ticket))[0]
    print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(ticket, sysId)
except Exception, e:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    print e
    print sn_client.print_error(e)
    print "Failed to create record in Service Now"
    sys.exit(1)

sn_client.wait_for_approval(tableName, sysId)