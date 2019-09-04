#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow import get_deep_link_url, add_code_compliance_record
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl

assert_not_null(parent, "Parent is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

query = "change_request=%s" % (parent)
if shortDescription:
    query = query + "^short_descriptionSTARTSWITH%s" % (shortDescription)

data = sn_client.query(tableName, query, True)
sysId = data["sys_id"]
ticket = data["number"]
url = get_deep_link_url(service_now_url=sn_client.service_now_url,
                        table_name=tableName,
                        sys_id=sysId)

mdl.println("Found '{}' with sysId '{}' in Service Now. \n".format(ticket, sysId))
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
