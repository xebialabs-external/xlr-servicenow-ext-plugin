from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(story, "Parent is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

data = sn_client.query(tableName, "sysparm_query=story=%s^short_descriptionSTARTSWITH%s" % (story,shortDescription))
sysId = data["sys_id"]
print "Found scrum task in Service Now with sys_id = %s.\n" % (sysId)
