#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl

assert_not_null(parent, "Parent is mandatory")

sn_client = ServiceNowClient.create_client(servicenowServer, username, password)

query = "change_request=%s" % (parent)
if shortDescription:
    query = query+ "^short_descriptionSTARTSWITH%s" % (shortDescription)

data = sn_client.query(tableName, query)
sysId = data["sys_id"]
ticket = data["number"]
mdl.println("Found '{}' with sysId '{}' in Service Now. \n".format(ticket, sysId))
mdl.print_hr()
mdl.print_header3("__Links__")
url = '%s/%s.do?sys_id=%s' % (sn_client.service_now_url, tableName, sysId)
mdl.print_url("Record Form View", url)
