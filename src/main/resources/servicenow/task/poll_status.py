#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import sys
import time
import traceback

from servicenow import get_deep_link_url, add_code_compliance_record
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null


class ServiceNowPollStatusClient(object):

    def __init__(self, task_vars, task_reporting_api, task):
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
        self.task_reporting_api = task_reporting_api
        self.task = task
        assert_not_null(task_vars['servicenowServer'], "No server provided.")
        assert_not_null(task_vars['sysId'], "No sysId provided.")
        assert_not_null(task_vars['tableName'], "No tableName provided.")
        #assert_not_null(task_vars['pollInterval'], "No pollInterval provided.")
        assert_not_null(task_vars['checkForStatus'], "No check status provided.")
        self.sn_client = ServiceNowClient.create_client(task_vars['servicenowServer'], task_vars['username'], task_vars['password'])


    def process_poll(self):
        sleepTime = 300
        data = ""
        i = 1
        while i < 550:
            try:
                data = self.sn_client.get_record(self.task_vars['tableName'], self.task_vars['sysId'])
                status = data[self.task_vars['statusField']]
                print "Found ", data['number'], " in Service Now with field value:", status, " Looking for:", self.task_vars['checkForStatus']
                if status == self.task_vars['checkForStatus']:
                    status = data[self.task_vars['statusField']]
                    ticket = data["number"]
                    break
            except Exception, e:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                print e
                print self.sn_client.print_error(e)
                print "Error finding status for %s" % statusField
            if i == 97:
                sleepTime = 600
            if i == 199:
                sleepTime = 1200
            if i == 298:
                sleepTime = 1800
            if i > 400:
                sleepTime = sleepTime + i - 200
            time.sleep(sleepTime)
            i += 1
        if i == 549 and status != self.task_vars['checkForStatus']:
            raise Exception("Timeout has been reached, more than 50 days have passed.")
        print "\n"
        return data, status

    def process(self):
        data, status = self.process_poll()
        ticket = data['number']

        add_code_compliance_record(table_name=self.table_name,
                                  task_reporting_api=self.task_reporting_api,
                                  task=self.task,
                                  service_now_server=self.task_vars['servicenowServer'],
                                  service_now_user=self.task_vars['username'],
                                  data=data,
                                  url=get_deep_link_url(self.sn_client.service_now_url, self.table_name, data['sys_id']))

        return status, ticket, data

status, ticket, data = ServiceNowPollStatusClient(locals(), task_reporting_api=taskReportingApi, task=task).process()
