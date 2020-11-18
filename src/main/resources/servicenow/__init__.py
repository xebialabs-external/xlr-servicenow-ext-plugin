# Copyright 2020 DIGITAL.AI

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys

def get_deep_link_url(service_now_url, table_name, sys_id):
    return '%s/%s.do?sys_id=%s' % (service_now_url, table_name, sys_id)


def add_code_compliance_record(table_name, task_reporting_api, task, service_now_server=None, service_now_user=None, data=None, url=None):
    if table_name not in ['rm_story', 'rm_scrum_task', 'rm_epic', 'rm_sprint']:
        try:
            record = task_reporting_api.newItsmRecord()
            record.targetId = task.id
            record.serverUrl = service_now_server['url'] if service_now_server else "Not available"
            record.serverUser = service_now_user or (service_now_server['username'] if service_now_server else "Not available")
            record.record = data['number'] if data and 'number' in data else "Not available"
            record.title = data['short_description'] if data and 'short_description' in data else "Not available"
            record.status = data['state'] if data and 'state' in data else "Not available"
            record.priority = data['priority'] if data and 'priority' in data else "Not available"
            record.createdBy = data['sys_created_by'] if data and 'sys_created_by' in data else "Not available"
            record.record_url = url
            task_reporting_api.addRecord(record, True)
        except:
            exctype, value = sys.exc_info()[:2]
            print("{} occurred while creating `udm.ItsmRecord` - {}".format(exctype, value))
