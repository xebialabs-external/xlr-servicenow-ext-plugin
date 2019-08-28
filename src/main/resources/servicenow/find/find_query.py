#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow import add_code_compliance_record
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl

assert_not_null(servicenowServer, "Server is mandatory")
assert_not_null(tableName, "TableName is mandatory")
assert_not_null(query, "Query is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

result = sn_client.find_record(tableName, query)
size = len(result)
numberFound = size
if not provideCount:
    if size == 1:
        data = result[0]
        sysId = data["sys_id"]
        url = '%s/%s.do?sys_id=%s' % (sn_client.service_now_url, tableName, sysId)

        mdl.println("Found a record with sysId '{}' in Service Now. \n".format(sysId))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        mdl.print_url("Record Form View", url)

        add_code_compliance_record(table_name=tableName,
                                  task_reporting_api=taskReportingApi,
                                  task=task,
                                  service_now_server=servicenowServer,
                                  service_now_user=username,
                                  data=data,
                                  url=url)
    elif failOnNotFound:
        raise Exception("%s results found for query '%s', while 1 expected." % (size, query))
else:
    mdl.println("Found '{}' number of record in Service Now.".format(size))
