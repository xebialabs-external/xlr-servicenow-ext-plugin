from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class ServiceNowRecordClient(object):

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
        #getting priority if valid
        if self.task_vars['priority']:
            ref = self.sn_client.find_value_of_list(self.task_vars['priority'], 'change_request', 'priority', True)
            content['priority'] = ref['value']
        #getting state if valid
        if self.task_vars['state']:
            ref = self.sn_client.find_value_of_list(self.task_vars['state'], 'change_request', 'state', True)
            content['state'] = ref['value']
        #getting the ci if valid
        if self.task_vars['ciSysId']:
            ref = self.sn_client.find_by_name(self.task_vars['ciSysId'], 'cmdb_ci', True)
            content['cmdb_ci'] = ref['sys_id']
        #getting the assignmentgroup if valid
        if self.task_vars['assignmentGroup']:
            ref = self.sn_client.find_by_name(self.task_vars['assignmentGroup'], 'sys_user_group', True)
            content['assignment_group'] = ref['sys_id']
        self.set_from_task_vars('comments', content, 'comments')
        for k, v in self.task_vars['additionalFields'].items():
            content[k] = v
        response = self.sn_client.create_record(self.table_name, content, getCurrentTask().getId())
        return response

    def print_links(self, sys_id, ticket, data):
        mdl.println("Created Ticket '{}' with sysId '{}' in Service Now. \n".format(ticket, sys_id))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/%s.do?sys_id=%s' % (self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)
        mdl.print_hr()
        mdl.print_hr()
        mdl.print_header3("__Details__")
        mdl.println(self.sn_client.format_record(data))

    def process(self):
        response = self.process_record()
        sys_id, number = response['target_sys_id'], response['target_record_number']
        data = self.sn_client.find_record(table_name=self.table_name, query="number={}".format(number))[0]
        self.print_links(sys_id, number, data)
        return sys_id, number, data

sysId, number, data = ServiceNowRecordClient(locals()).process()

