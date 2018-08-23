import sys
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

assert_not_null(servicenowServer, "No server provided.")
assert_not_null(tableName, "No tableName provided.")
assert_not_null(content, "No content provided.")

snClient = ServiceNowClient.create_client(servicenowServer, username, password)

print "Sending content {}".format(content)

try:
    data = snClient.create_record(tableName, content)
    taskId = data["sys_id"]
    Task = data["number"]
    print "Created {} in Service Now.".format(taskId)
    print "Created {} in Service Now.".format(Task)
    print "\n"
    print snClient.format_record(data)
except Exception, e:
    print e
    print snClient.print_error(e)
    print "Failed to create record in Service Now"
    sys.exit(1)
