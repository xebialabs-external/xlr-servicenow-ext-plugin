from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(parent, "Parent is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

data = sn_client.find_record(tableName, "change_request=%s&short_descriptionSTARTSWITH%s" % (parent,shortDescription))
numRecords = len(data)
print "Found %s records for the chosen serach criteria.\n" % (numRecords)
data = data[0]
sysId = data["sys_id"]
print "Found change task in Service Now with sysId = %s.\n" % (sysId)
print sn_client.format_record(data)
