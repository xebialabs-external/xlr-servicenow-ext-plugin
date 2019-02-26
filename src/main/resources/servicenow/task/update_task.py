#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class ServiceNowUpdateRecordClient(object):

    def __init__(self, task_vars):
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'],
                                                        task_vars['password'])
    
    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    def process_record(self):
        content = {'short_description': self.task_vars['shortDescription']}
        self.set_from_task_vars('description', content)
        self.set_from_task_vars('assignedTo', content, 'assigned_to')
        self.set_from_task_vars('priority', content, 'priority')
        self.set_from_task_vars('state', content, 'state')
        self.set_from_task_vars('ciSysId', content, 'cmdb_ci')
        self.set_from_task_vars('assignmentGroup', content, 'assignment_group')
        self.set_from_task_vars('comments', content, 'comments')
        for k, v in self.task_vars['additionalFields'].items():
            content[k] = v
        response = self.sn_client.update_record(self.table_name, self.task_vars['sysId'], content, getCurrentTask().getId())
        return response

    def print_links(self, sys_id, ticket, data):
        mdl.println("Updated task '{}' with number '{}' in Service Now. \n".format(ticket, data['number']))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/%s.do?sys_id=%s' % (self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)

    def process(self):
        self.process_record()
        data = self.sn_client.get_record(self.task_vars['tableName'],self.task_vars['sysId'])
        self.print_links(self.task_vars['sysId'], data['number'], data)
        return data, data['number']

data, number = ServiceNowUpdateRecordClient(locals()).process()