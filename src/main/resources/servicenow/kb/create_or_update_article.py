#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

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
        content = {"kb_knowledge_base": self.task_vars['knowledgeBase'], "kb_category": self.task_vars['articleCategory'],"short_description": self.task_vars['shortDescription'],
                   "text": self.task_vars['articleText']}
        response = self.sn_client.create_record('kb_knowledge', content, getCurrentTask().getId())
        return response["target_sys_id"]

    def process(self):
        sys_id = self.publish_article()
        self.print_links(sys_id)

PublishArticleClient(locals()).process()