from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class PublishArticleClient(object):

    def __init__(self, task_vars):
        self.task_vars = task_vars
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'],
                                                        task_vars['password'])

    def print_links(self, sys_id):
        mdl.print_hr()
        mdl.print_header3("__Links__")
        url = '%s/kb_view.do?sys_kb_id=%s' % (self.sn_client.service_now_url, sys_id)
        mdl.print_url("Article Form View", url)
        mdl.println("")
        url = '%s/sp?id=kb_article&sys_id=%s' % (self.sn_client.service_now_url, sys_id)
        mdl.print_url("Article Portal View", url)
        mdl.print_hr()

    def publish_article(self):
        kb_ci = self.sn_client.find_record("kb_knowledge_base", "name=%s" % self.task_vars['knowledgeBase'])[0]
        category_ci = self.sn_client.find_record("kb_category", "name=%s" % self.task_vars['articleCategory'])[0]

        content = {"kb_knowledge_base": kb_ci['sys_id'], "kb_category": category_ci['sys_id'],
                   "short_description": self.task_vars['shortDescription'],
                   "text": self.task_vars['articleText'], 'workflow_state': 'published'}
        response = self.sn_client.create_record('kb_knowledge', content)
        return response["target_sys_id"]

    def process(self):
        sys_id = self.publish_article()
        self.print_links(sys_id)


PublishArticleClient(locals()).process()

