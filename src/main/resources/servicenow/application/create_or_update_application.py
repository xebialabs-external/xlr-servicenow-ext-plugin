from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class ServiceNowApplicationClient(object):

    def __init__(self, task_vars):
        self.table_cmdb_ci_app = 'cmdb_ci_appl'
        self.table_cmdb_ci_app_server = 'cmdb_ci_app_server'
        self.ci_name = task_vars['ciName']
        self.depends_on_rel_typ_sys_id = '1a9cb166f1571100a92eb60da2bce5c5'
        self.runs_on_rel_typ_sys_id = '60bc4e22c0a8010e01f074cbe6bd73c3'
        self.task_vars = task_vars
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'],
                                                        task_vars['password'])

    # Path for default client.  It uses v1 of the api which throws a 404 not found when nothing matchs. v2 doesn't.
    def _find_record(self, table_name, query):
        servicenow_api_url = '/api/now/table/%s?%s&%s' % (table_name, query, self.sn_client.sysparms)
        return self.sn_client.request(method='GET', url=servicenow_api_url, headers=self.sn_client.headers)

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

    def find_relationship(self, parent_sys_id, child_sys_id, fail_on_not_found=False):
        query = "parent.sys_id=%s^child.sys_id=%s" % (parent_sys_id, child_sys_id)
        return self.query('cmdb_rel_ci', query, fail_on_not_found)

    def create_ci(self, table_name, content):
        record_data = self.sn_client.create_record(table_name, content)
        return record_data["target_sys_id"]

    def update_ci(self, table_name, content, ticket):
        self.sn_client.update_record(table_name, ticket, content)

    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    def get_optional_task_var(self, name):
        if name in self.task_vars.keys():
            return self.task_vars[name]
        return None

    def process_application_ci(self, name):
        ci = self.find_by_name(name, self.table_cmdb_ci_app)
        if ci is None:
            content = {'name': name}
            self.set_from_task_vars('environment', content)
            self.set_from_task_vars('version', content)
            sys_id = self.create_ci(self.table_cmdb_ci_app, content)
        else:
            sys_id = ci['sys_id']
        return sys_id

    def process_app_server_ci(self, name):
        ci = self.find_by_name(name, self.table_cmdb_ci_app_server)
        if ci is None:
            content = {'name': name}
            self.set_from_task_vars('version', content)
            sys_id = self.create_ci(self.table_cmdb_ci_app_server, content)
        else:
            sys_id = ci['sys_id']
        return sys_id

    def process_depends_on_relationship(self, parent_sys_id, child_sys_id):
        rel_ci = self.find_relationship(parent_sys_id, child_sys_id)
        if rel_ci is None:
            content = {'child': child_sys_id, 'parent': parent_sys_id, 'type': self.depends_on_rel_typ_sys_id}
            self.create_ci('cmdb_rel_ci', content)

    def process_runs_on_relationship(self, parent_sys_id, child_sys_id):
        rel_ci = self.find_relationship(parent_sys_id, child_sys_id)
        if rel_ci is None:
            content = {'child': child_sys_id, 'parent': parent_sys_id, 'type': self.runs_on_rel_typ_sys_id}
            self.create_ci('cmdb_rel_ci', content)

    def process_depends_on_relationships(self, parent_sys_id):
        depends_on = self.get_optional_task_var("dependsOn")
        if not depends_on:
            return
        for app_name in depends_on:
            child_sys_id = self.process_application_ci(app_name)
            self.process_depends_on_relationship(parent_sys_id, child_sys_id)

    def process_used_by_relationships(self, child_sys_id):
        used_by = self.get_optional_task_var("usedBy")
        if not used_by:
            return
        for app_name in used_by:
            parent_sys_id = self.process_application_ci(app_name)
            self.process_depends_on_relationship(parent_sys_id, child_sys_id)

    def process_runs_on_relationships(self, parent_sys_id):
        runs_on = self.get_optional_task_var("runsOn")
        if not runs_on:
            return
        for app_name in runs_on:
            child_sys_id = self.process_app_server_ci(app_name)
            self.process_runs_on_relationship(parent_sys_id, child_sys_id)

    def print_links(self, sys_id):
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/$ngbsm.do?id=%s' % (self.sn_client.service_now_url, sys_id)
        mdl.print_url("Application Dependency View", url)
        mdl.print_hr()

    def process(self):
        sys_id = self.process_application_ci(self.ci_name)
        self.process_depends_on_relationships(sys_id)
        self.process_used_by_relationships(sys_id)
        self.process_runs_on_relationships(sys_id)
        self.print_links(sys_id)
        return sys_id


sysId = ServiceNowApplicationClient(locals()).process()


