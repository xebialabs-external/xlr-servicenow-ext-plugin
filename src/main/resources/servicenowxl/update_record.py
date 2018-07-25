from servicenowxl.client.ServiceNowClient import ServiceNowClient
from servicenowxl.helper.helper import assert_not_null

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(sysId, "SysId is mandatory")
assert_not_null(content, "Content is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
data = sn_client.update_record(tableName, sysId, content)
print sn_client.format_record(data)
