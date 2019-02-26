#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#


import urllib
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null

def get_row_data(item):
    row_map = {}
    for column in detailsViewColumns:
        if detailsViewColumns[column] and "." in detailsViewColumns[column]:
            json_col = detailsViewColumns[column].split('.')
            if item[json_col[0]]:
                row_map[column] = item[json_col[0]][json_col[1]]
        else:
            row_map[column] = item[column]
    row_map['link'] = sn_client.create_link(tableName, item['sys_id'])
    return row_map

assert_not_null(servicenowServer, "Server is mandatory")
sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
results = sn_client.find_record(tableName, "sysparm_query=%s&sysparm_limit=1000"% ('' if query == None else query))
rows= {}
for item in results:
    rows[item['number']] = get_row_data(item)
data = rows

