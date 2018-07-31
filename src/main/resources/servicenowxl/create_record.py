from servicenowxl.client.ServiceNowClient import ServiceNowClient
from servicenowxl.helper.helper import assert_not_null
import json

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(shortDescription, "ShortDescription is mandatory")
assert_not_null(comments, "Comments is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
data = sn_client.create_record(tableName, json.dumps({'short_description': shortDescription, 'comments': comments}))
sysId = data["sys_id"]
ticket = data["number"]
print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(ticket, sysId)
print sn_client.format_record(data)
