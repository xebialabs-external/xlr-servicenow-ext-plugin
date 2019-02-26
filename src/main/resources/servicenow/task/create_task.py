#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class ServiceNowRecordClient(object):

    def __init__(self, task_vars):
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        assert_not_null(task_vars['shortDescription'], "Short description is mandatory when creating a task.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'],
                                                        task_vars['password'])

    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    def process_record(self):
        content = {}
        self.set_from_task_vars('shortDescription', content, 'short_description')
        self.set_from_task_vars('description', content)
        self.set_from_task_vars('assignmentGroup', content, 'assignment_group')
        self.set_from_task_vars('assignedTo', content, 'assigned_to')
        self.set_from_task_vars('priority', content, 'priority')
        self.set_from_task_vars('state', content, 'state')
        self.set_from_task_vars('ciSysId', content, 'cmdb_ci')
        self.set_from_task_vars('comments', content, 'comments')

        self.set_from_task_vars('changeRequest', content, 'change_request')
        self.set_from_task_vars('workNotes', content, 'work_notes')
        self.set_from_task_vars('storyPoints', content, 'story_points')
        self.set_from_task_vars('epic', content, 'epic')
        self.set_from_task_vars('product', content, 'product')
        self.set_from_task_vars('sprint', content, 'sprint')
        self.set_from_task_vars('taskType', content, 'type')
        self.set_from_task_vars('plannedHours', content, 'planned_hours')
        self.set_from_task_vars('story', content, 'story')

        for k, v in self.task_vars['additionalFields'].items():
            content[k] = v
        response = self.sn_client.create_record(self.table_name, content, getCurrentTask().getId())
        return response

    def print_links(self, sys_id, ticket, data):
        mdl.println("Created '{}' with sysId '{}' in Service Now. \n".format(ticket, sys_id))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/%s.do?sys_id=%s' % (self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)

    def process(self):
        response = self.process_record()
        sys_id = response['target_sys_id']
        data = self.sn_client.find_record(table_name=self.table_name, query="sys_id={}".format(sys_id))[0]
        self.print_links(sys_id, data['number'], data)
        return sys_id, data['number'], data

sysId, number, data = ServiceNowRecordClient(locals()).process()

