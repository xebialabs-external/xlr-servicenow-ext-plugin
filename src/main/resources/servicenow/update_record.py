import com.xhaus.jyson.JysonCodec as json

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(sysId, "SysId is mandatory")
assert_not_null(content, "Content is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
xlr_task_id = task.getId()

# Get Ticket Number from SysID
record = sn_client.find_record(table_name=tableName, query="sys_id={}".format(sysId))[0]
ticket = record["number"]

# Update Record using ticket number
updated_record = sn_client.update_record(table_name=tableName, ticket=ticket, content=json.loads(content), xlr_task_id=xlr_task_id)

# Find updated record and show on UI
data = sn_client.find_record(table_name=tableName, query="sys_id={}".format(sysId))[0]
print sn_client.format_record(data)
