from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(parent, "Parent is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

data = sn_client.query(tableName, "sysparm_query=change_request=%s^short_descriptionSTARTSWITH%s" % (parent,shortDescription))
sysId = data["sys_id"]
print "Found change task in Service Now with sysId = %s.\n" % (sysId)
