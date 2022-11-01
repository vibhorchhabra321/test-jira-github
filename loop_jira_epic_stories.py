from operator import truediv
#from jira import JIRA
from atlassian import Jira
import os
import warnings
import functools
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

def rgetattr(obj, attr, *args):
    def __getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(__getattr, [obj] + attr.split('.'))

def get_field_data(field, name):
    return rgetattr(field, name, 'Not Populated')

def get_validation_fields(issue):
    migr_fields = issue["fields"]
    field_dict = {
        'migration_status':get_field_data(migr_fields, 'customfield_21600.value'),
        'QA_tester_email': get_field_data(migr_fields, 'customfield_12300.name'),
        'QA_tester_displayname': get_field_data(migr_fields, 'customfield_12300.displayName'),
        'migration_approver_email': get_field_data(migr_fields, 'customfield_17832.name'),
        'migration_approver_displayname': get_field_data(migr_fields, 'customfield_17832.displayName'),
        'migration_services_list': get_field_data(migr_fields, 'customfield_10038.value'),
        'scrutiny_tickets': get_field_data(migr_fields, 'customfield_22200')
    }
    valid_ticket = True
    jira_validation_results = {}
    for k, v in field_dict.items():
        if v is None:
            jira_validation_results[k] = 'Not Populated'
            valid_ticket = False
        # print(f'k: {k} v: {v}')
        fieldname = k
        attr = v
        if isinstance(attr, str):
            jira_validation_results[fieldname] = attr
        if isinstance(attr, list):
            count = 0
            keys = []
            for item in attr:
                fname = fieldname + '_' + str(count) + '_key'
                keys.append(item.key)
                jira_validation_results[fname] = item.key
                fname = fieldname + '_' + str(count) + '_url'
                jira_validation_results[fname] = item.self
                count = count + 1  
            jira_validation_results[fieldname] = ', '.join(keys)
    jira_validation_results['valid_ticket'] = valid_ticket
    return jira_validation_results


warnings.filterwarnings('ignore',message='Unverified HTTPS request')

jira_base_url = os.environ.get("JIRA_CLOUD_URL")
username = os.environ.get("JIRA_USER_LOCAL")
apikey = os.environ.get("JIRA_TOKEN_LOCAL")

jira = Jira(
    url='https://uneritx.atlassian.net',
    username='vibhor@uneritx.com',
    password='8ehgj5XOOUxKfzCaFf6U1AC8',
    cloud=True)
#jira = Jira(options={'url':'https://uneritx.atlassian.net', 'verify':False}, basic_auth=('vibhor@uneritx.com', '8ehgj5XOOUxKfzCaFf6U1AC8'))

epic_ticket = "ST-1"
epic_stories = []
epic_stories_tasks = [{}]


jql_request = '"Epic Link" = {}'.format(epic_ticket)
epic = jira.jql(jql_request)

print(len(epic["issues"]))
for epic_issue_count in range(0,len(epic["issues"])):
    epic_story_key=epic["issues"][epic_issue_count]["key"]
    epic_stories.append(epic_story_key)

print(epic_stories)

for story in epic_stories:
    migr_issue = jira.issue(story)
    #print(migr_issue["id"])
    print(migr_issue["fields"]["customfield_10038"])
    #validation_results = get_validation_fields(migr_issue)
    #pp.pprint(validation_results)

