#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#
import com.xhaus.jyson.JysonCodec as json

from servicenow import get_deep_link_url, add_code_compliance_facet
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class ServiceNowUpdateRecordClient(object):

    def __init__(self, task_vars, facet_api, task):
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
        self.facet_api = facet_api
        self.task = task
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        assert_not_null(task_vars['sysId'], "Sys_id is mandatory when updating a task.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'],
                                                        task_vars['password'])

    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    def process_record(self):
        contentx = {}

        # First old stuff so the newer fields will overwrite.
        if 'content' in self.task_vars.keys():
            if content:
                oldStuff = {}
                oldStuff = json.loads(content)
                for m, y in oldStuff.items():
                    contentx[m] = y

        self.set_from_task_vars('shortDescription', contentx, 'short_description')
        self.set_from_task_vars('description', contentx)
        self.set_from_task_vars('assignmentGroup', contentx, 'assignment_group')
        self.set_from_task_vars('assignedTo', contentx, 'assigned_to')
        self.set_from_task_vars('priority', contentx)
        self.set_from_task_vars('state', contentx)
        self.set_from_task_vars('ciSysId', contentx, 'cmdb_ci')
        self.set_from_task_vars('comments', contentx)

        self.set_from_task_vars('changeRequest', contentx, 'change_request')
        self.set_from_task_vars('workNotes', contentx, 'work_notes')
        self.set_from_task_vars('storyPoints', contentx, 'story_points')
        self.set_from_task_vars('epic', contentx)
        self.set_from_task_vars('product', contentx)
        self.set_from_task_vars('sprint', contentx)
        self.set_from_task_vars('acceptanceCriteria', contentx, 'acceptance_criteria')
        self.set_from_task_vars('taskType', contentx, 'type')
        self.set_from_task_vars('plannedHours', contentx, 'planned_hours')
        self.set_from_task_vars('story', contentx)
        self.set_from_task_vars('impact', contentx)
        self.set_from_task_vars('urgency', contentx)
        self.set_from_task_vars('closeCode', contentx, 'close_code')
        self.set_from_task_vars('closeNotes', contentx, 'close_notes')

        # Also sending release info.
        contentx['x_xlbv_xl_release_identifier'] = str(release.id)
        contentx['x_xlbv_xl_release_state'] = str(release.status)

        for k, v in self.task_vars['additionalFields'].items():
            contentx[k] = v

        response = self.sn_client.update_record(self.table_name, self.task_vars['sysId'], contentx,
                                                getCurrentTask().getId())
        return response

    def print_links(self, sys_id, ticket, data):
        mdl.println("Updated task with number '{}' in Service Now. \n".format(data['number']))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = get_deep_link_url(self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)

    def process(self):
        self.process_record()
        data = self.sn_client.get_record(self.table_name, self.task_vars['sysId'])
        self.print_links(self.task_vars['sysId'], data['number'], data)

        add_code_compliance_facet(table_name=self.table_name,
                                  facet_api=self.facet_api,
                                  task=self.task,
                                  service_now_server=self.task_vars['servicenowServer'],
                                  service_now_user=self.task_vars['username'],
                                  data=data,
                                  url=get_deep_link_url(self.sn_client.service_now_url, self.table_name,
                                                        self.task_vars['sysId']))

        return data, data['number']


data, ticket = ServiceNowUpdateRecordClient(locals(), facet_api=facetApi, task=task).process()
