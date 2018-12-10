import com.xhaus.jyson.JysonCodec as json

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
xlr_task_id = task.getId()

request = {'used_for': environment, 'name': applicationName, 'company': company,
           'u_config_admin_group': configAdminGroup, 'version': version, 'u_vm': virtualMachine, 'u_tomcat': tomcat,
           'u_mysql': mysql, 'u_space': cfSpace}
print "Sending content %s" % json.dumps(request)
data = sn_client.create_record(tableName, request, xlr_task_id)
sysId = data["target_sys_id"]

# Find updated record and show on UI
data = sn_client.find_record(table_name=tableName, query="sys_id={}".format(sysId))[0]

print "#Created %s in Service Now.#\n" % (sysId)
print sn_client.format_record(data)
