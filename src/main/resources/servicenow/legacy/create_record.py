from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(shortDescription, "ShortDescription is mandatory")
assert_not_null(comments, "Comments is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

# create record in service now using queue table
record_data = sn_client.create_record(tableName, {'short_description': shortDescription, 'comments': comments})
sysId = record_data["target_sys_id"]
Ticket = record_data["target_record_number"]

# find record using ticker number and show on UI
data = sn_client.find_record(table_name=tableName, query="number={}".format(Ticket))[0]
print "Created Ticket '{}' with sysId '{}' in Service Now. \n".format(Ticket, sysId)
print sn_client.format_record(data)
