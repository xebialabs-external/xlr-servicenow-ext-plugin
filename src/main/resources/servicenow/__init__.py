#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#
import sys


def get_deep_link_url(service_now_url, table_name, sys_id):
    return '%s/%s.do?sys_id=%s' % (service_now_url, table_name, sys_id)


def add_code_compliance_record(table_name, task_reporting_api, task, service_now_server=None, service_now_user=None, data=None, url=None):
    if table_name not in ['rm_story', 'rm_scrum_task', 'rm_epic', 'rm_sprint']:
        try:
            record = task_reporting_api.newItsmRecord()
            record.targetId = task.id
            record.serverUrl = service_now_server['url'] if service_now_server else None
            record.serverUser = service_now_user or (service_now_server['username'] if service_now_server else None)
            record.record = data['number'] if data and 'number' in data else None
            record.title = data['short_description'] if data and 'short_description' in data else None
            record.status = data['state'] if data and 'state' in data else None
            record.priority = data['priority'] if data and 'priority' in data else None
            record.createdBy = data['sys_created_by'] if data and 'sys_created_by' in data else None
            record.record_url = url
            task_reporting_api.addRecord(record, True)
        except:
            exctype, value = sys.exc_info()[:2]
            print("{} occurred while creating `udm.ItsmRecord` - {}".format(exctype, value))
