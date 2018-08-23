from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
data = sn_client.create_record(tableName, content)
sysId = data["sys_id"]
Ticket = data["number"]
print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(Ticket, sysId)
print sn_client.format_record(data)