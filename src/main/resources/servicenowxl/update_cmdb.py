import sys, string, time
import json
from servicenowxl.client.ServiceNowClient import ServiceNowClient
from servicenowxl.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
request = {'used_for': environment, 'name': applicationName, 'company': company,
           'u_config_admin_group': configAdminGroup, 'version': version, 'u_vm': virtualMachine, 'u_tomcat': tomcat,
           'u_mysql': mysql, 'u_space': cfSpace}
print "Sending content %s" % json.dumps(request)
data = sn_client.create_record(tableName, json.dumps(request))
sysId = data["sys_id"]
print "#Created %s in Service Now.#\n" % (sysId)
print sn_client.format_record(data)