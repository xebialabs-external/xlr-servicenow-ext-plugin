#
# Copyright (c) 2019. All rights reserved.
#
# This software and all trademarks, trade names, and logos included herein are the property of XebiaLabs, Inc. and its affiliates, subsidiaries and licensors.
#
import sys


def get_deep_link_url(service_now_url, table_name, sys_id):
    return '%s/%s.do?sys_id=%s' % (service_now_url, table_name, sys_id)


def add_code_compliance_facet(table_name, facet_api, task, service_now_server=None, service_now_user=None, data=None, url=None):
    if table_name not in ['rm_story', 'rm_scrum_task', 'rm_epic', 'rm_sprint']:
        try:
            facet = facet_api.newFacet("udm.ItsmFacet")
            facet.targetId = task.id
            facet.serverUrl = service_now_server['url'] if service_now_server else None
            facet.serverUser = service_now_user or (service_now_server['username'] if service_now_server else None)
            facet.recordNumber = data['number'] if data and 'number' in data else None
            facet.title = data['short_description'] if data and 'short_description' in data else None
            facet.status = data['state'] if data and 'state' in data else None
            facet.priority = data['priority'] if data and 'priority' in data else None
            facet.createdBy = data['sys_created_by'] if data and 'sys_created_by' in data else None
            facet.recordUrl = url
            facet_api.createFacet(facet)
        except:
            exctype, value = sys.exc_info()[:2]
            print("{} occurred while creating `udm.ItsmFacet` - {}".format(exctype, value))
