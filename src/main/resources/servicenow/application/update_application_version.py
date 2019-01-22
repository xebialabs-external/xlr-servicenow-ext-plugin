from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl
import json

class ServiceNowApplicationClient(object):

    def __init__(self, task_vars):
        self.table_cmdb_ci_app = 'cmdb_ci_appl'
        self.ci_name = task_vars['ciName']
        self.task_vars = task_vars
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'],
                                                        task_vars['password'])

    # Path for default client.  It uses v1 of the api which throws a 404 not found when nothing matchs. v2 doesn't.
    def _find_record(self, table_name, query):
        servicenow_api_url = '/api/now/table/%s?%s&%s' % (table_name, query, self.sn_client.sysparms)
        return self.sn_client.request(method='GET', url=servicenow_api_url, headers=self.sn_client.headers)

    # This updates the cmdb record directly and not via the queue table
    def _update_cmdb_record(self, sys_id, content):
        servicenow_api_url = '/api/now/table/cmdb_ci_appl/%s' % sys_id
        return self.sn_client.request('PUT', servicenow_api_url, self.sn_client.headers, body=json.dumps(content))

    def query(self, table_name, query, fail_on_not_found=False):
        # check if application exists
        result = self._find_record(table_name, query)
        size = len(result)
        if size is 1:
            return result[0]
        elif size > 1:
            raise Exception("Expected to find only 1 entry with query '%s' but found %s" % (query, size))
        if fail_on_not_found:
            raise Exception("No resullts found for query '%s'." % query)
        return None

    def find_by_name(self, name, table_name, fail_on_not_found=False):
        # check if application exists
        query = "name=%s" % name
        return self.query(table_name, query, fail_on_not_found)

    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    def is_task_var_diff(self, source_name, target_value):
        return source_name in self.task_vars.keys() and self.task_vars[source_name] != target_value

    def process_application_ci(self, name):
        ci = self.find_by_name(name, self.table_cmdb_ci_app, fail_on_not_found=True)
        sys_id = ci['sys_id']
        if self.is_task_var_diff('version', ci['version']):
            content = {'sys_id': sys_id}
            self.set_from_task_vars('environment', content)
            self.set_from_task_vars('version', content)
            self._update_cmdb_record(sys_id, content)
        return sys_id

    def print_links(self, sys_id):
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/cmdb_ci_appl.do?sys_id=%s' % (self.sn_client.service_now_url, sys_id)
        mdl.print_url("Application Form View", url)
        mdl.print_hr()

    def process(self):
        sys_id = self.process_application_ci(self.ci_name)
        self.print_links(sys_id)


ServiceNowApplicationClient(locals()).process()

