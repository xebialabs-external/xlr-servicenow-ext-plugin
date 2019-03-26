#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#

import sys
import time
import traceback
from servicenow.client.ServiceNowClient import ServiceNowClient
from servicenow.helper.helper import assert_not_null


class ServiceNowPollStatusClient(object):

    def __init__(self, task_vars):
        self.table_name = task_vars['tableName']
        self.task_vars = task_vars
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
                print "Found [{}] in Service Now with field value: [{}] Looking for [{}]\n".format(data['number'], status, self.task_vars['checkForStatus'])
                if status == self.task_vars['checkForStatus']:
                    status = data[self.task_vars['statusField']]
                    ticket = data["number"]
                    break
            except Exception, e:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                print e
                print sn_client.print_error(e)
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
        return data

    def process(self):
        data = self.process_poll()
        return data

data = ServiceNowPollStatusClient(locals()).process()