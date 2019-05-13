#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

from servicenow import add_code_compliance_facet
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null
from servicenow.markdown.markdown_logger import MarkdownLogger as mdl


class PublishArticleClient(object):

    def __init__(self, task_vars, facet_api, task):
        self.task_vars = task_vars
        self.facet_api = facet_api
        self.task = task
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        assert_not_null(task_vars['knowledgeBase'], "No knowledge base provided.")
        assert_not_null(task_vars['shortDescription'], "No description provided.")
        assert_not_null(task_vars['articleText'], "No text provided.")
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
        content = {"kb_knowledge_base": self.task_vars['knowledgeBase'], "kb_category": self.task_vars['articleCategory'],"short_description": self.task_vars['shortDescription'],
                   "text": self.task_vars['articleText']}

        #Also sending release info.
        content['x_xlbv_xl_release_identifier'] = str(release.id)
        content['x_xlbv_xl_release_state'] = str(release.status)

        response = self.sn_client.create_record('kb_knowledge', content, getCurrentTask().getId())
        return response["target_sys_id"]

    def process(self):
        sys_id = self.publish_article()
        data = self.sn_client.get_record('kb_knowledge', sys_id)
        self.print_links(sys_id)

        add_code_compliance_facet(table_name='kb_knowledge',
                                  facet_api=self.facet_api,
                                  task=self.task,
                                  service_now_server=self.task_vars['servicenowServer'],
                                  service_now_user=self.task_vars['username'],
                                  data=data,
                                  url='%s/kb_view.do?sys_kb_id=%s' % (self.sn_client.service_now_url, sys_id))
        return data

data = PublishArticleClient(locals(), facet_api=facetApi, task=task).process()
