# Copyright 2020 DIGITAL.AI

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from servicenow import get_deep_link_url, add_code_compliance_record
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl

from java.text import SimpleDateFormat

import logging
import logging.handlers
import os

LOG_FILENAME = 'log/snow-ext-plugin.log'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=2)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


logger.debug('logger has been configured')

class ServiceNowRecordClient(object):

    def __init__(self, task_vars, task_reporting_api, task):
        logger.info('record client init : begin')
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
        self.task_reporting_api = task_reporting_api
        self.task = task
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        assert_not_null(task_vars['assignment_group'], "Assignment group is required.")
        assert_not_null(task_vars['short_description'], "Short description is required when creating a task.")
        assert_not_null(task_vars['description'], "Description is required.")
        logger.info('record client init : creating client')
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'], task_vars['password'])
        logger.info('record client init : end')


    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]


    def process_record(self):
        content = {}
        self.set_from_task_vars('u_request', content)
        self.set_from_task_vars('u_application_name', content)
        self.set_from_task_vars('cmdb_ci', content)
        self.set_from_task_vars('priority', content)
        self.set_from_task_vars('state', content)
        self.set_from_task_vars('assignment_group', content)
        self.set_from_task_vars('assigned_to', content)
        self.set_from_task_vars('due_date', content)
        self.set_from_task_vars('short_description', content)
        self.set_from_task_vars('description', content)

        # Dates need to be converted
        sdf = SimpleDateFormat("MM-dd-yyyy HH:mm:ss");
        content['due_date'] = sdf.format(self.task_vars['due_date'])

        # Also sending release info.
        content['x_xlbv_xl_release_identifier'] = str(release.id)
        content['x_xlbv_xl_release_state'] = str(release.status)

        logger.debug('process_record : send create_record request...')
        logger.debug('process_record : table name: '+self.table_name)
        logger.debug('process_record : content... ')
        logger.debug(content)
        response = self.sn_client.create_record(self.table_name, content, getCurrentTask().getId())
        logger.debug('process_record : response...')
        logger.debug(response)

        return response


    def print_links(self, sys_id, ticket, data):
        mdl.println("Created '{}' with sysId '{}' in Service Now. \n".format(ticket, sys_id))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = get_deep_link_url(self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)


    def process(self):
        response = self.process_record()
        sys_id = response['target_sys_id']
        data = self.sn_client.get_record(self.table_name, sys_id)
        self.print_links(sys_id, data['number'], data)

        logger.info('create rtask : add_code_compliance_record')
        add_code_compliance_record(table_name=self.table_name,
                                  task_reporting_api=self.task_reporting_api,
                                  task=self.task,
                                  service_now_server=self.task_vars['servicenowServer'],
                                  service_now_user=self.task_vars['username'],
                                  data=data,
                                  url=get_deep_link_url(self.sn_client.service_now_url, self.table_name, sys_id))

        return sys_id, data['number'], data


logger.info('create rtask : begin')
sysId, rtaskId, data = ServiceNowRecordClient(locals(), task_reporting_api=taskReportingApi, task=task).process()
logger.info('create rtask : end')
