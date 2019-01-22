# import com.xhaus.jyson.JysonCodec as json
#
# from servicenow.client.ServiceNowClient import ServiceNowClient
# from servicenow.helper.helper import assert_not_null
#
# assert_not_null(servicenowServer, "Server is mandatory")
# assert_not_null(tableName, "TableName is mandatory")
# assert_not_null(sysId, "SysId is mandatory")
# assert_not_null(content, "Content is mandatory")
#
# sn_client = ServiceNowClient.create_client(servicenowServer, username, password)
#
# # Get Ticket Number from SysID
# record = sn_client.find_record(table_name=tableName, query="sys_id={}".format(sysId))[0]
# ticket = record["number"]
#
# # Update Record using ticket number
# updated_record = sn_client.update_record(table_name=tableName, ticket=ticket, content=json.loads(content))
#
# # Find updated record and show on UI
# data = sn_client.find_record(table_name=tableName, query="sys_id={}".format(sysId))[0]
# print sn_client.format_record(data)

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

    def set_from_task_vars(self, source_name, target_object, target_name=None):
        if source_name in self.task_vars.keys() and self.task_vars[source_name]:
            if target_name is None:
                target_name = source_name
            target_object[target_name] = self.task_vars[source_name]

    def get_record_for_sys_id(self, sys_id):
        # Get Ticket Number from SysID
        record = self.sn_client.find_record(table_name=self.table_name, query="sys_id={}".format(sys_id))[0]
        return record

    def process_record(self):
        ticket = self.get_record_for_sys_id(self.task_vars['sysId'])['number']
        content = {}
        self.set_from_task_vars('shortDescription', content, 'short_description')
        self.set_from_task_vars('description', content)
        self.set_from_task_vars('ciSysId', content, 'cmdb_ci')
        if self.task_vars['state']:
            ref = self.query('sys_choice', 'table=%s^label=%s' % (self.table_name, self.task_vars['state']), True)
            content['state'] = ref['value']
        if self.task_vars['assignmentGroup']:
            ref = self.find_by_name(self.task_vars['assignmentGroup'], 'sys_user_group', True)
            content['assignment_group'] = ref['sys_id']
        self.set_from_task_vars('comments', content, 'comments')
        for k, v in self.task_vars['additionalFields'].items():
            content[k] = v
        response = self.sn_client.update_record(self.table_name, ticket, content)
        return response

    def print_links(self, sys_id, ticket, data):
        mdl.println("Update Ticket '{}' with sysId '{}' in Service Now. \n".format(ticket, sys_id))
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/%s.do?sys_id=%s' % (self.sn_client.service_now_url, self.table_name, sys_id)
        mdl.print_url("Record Form View", url)
        mdl.print_hr()
        mdl.print_hr()
        mdl.print_header3("__Details__")
        mdl.println(self.sn_client.format_record(data))

    def process(self):
        self.process_record()
        sys_id = self.task_vars['sysId']
        data = self.get_record_for_sys_id(sys_id)
        self.print_links(sys_id, data['number'], data)
        return data


data = ServiceNowUpdateRecordClient(locals()).process()

