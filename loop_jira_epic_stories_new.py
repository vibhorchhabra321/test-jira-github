import functools
import pprint
from jira import JIRA
import os
import warnings
import pandas as pd

class issue_fields(dict):
 
  # __init__ function
  def __init__(self):
    self = dict()
 
  # Function to add key:value
  def add(self, key, value):
    self[key] = value
 
 
# Main Function
#svc_obj = service()

def rgetattr(obj, attr, *args):
    def __getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(__getattr, [obj] + attr.split('.'))

def get_field_data(field, name):
    return rgetattr(field, name, 'Not Populated')

def get_validation_fields(issue):
    migr_fields = issue.fields
    field_dict = {
        'services_list': get_field_data(migr_fields, 'customfield_10038'),
        'QA_Tester': get_field_data(migr_fields, 'customfield_10044.displayName')
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

jira = JIRA(options={'server':'https://uneritx.atlassian.net', 'verify':False}, basic_auth=('your-user-id', 'your-user-password'))

jira.search_issues('parentEpic=ST-1')
epic_stories=[]
for issue in jira.search_issues('parentEpic=ST-1'):
    epic_stories.append(issue.key)
    #print('{}: {}'.format(issue.key, issue.fields))
##print(epic_stories)
epic_stories_details=[]
for story in epic_stories:
    migr_issue = jira.issue(story)
    #print(migr_issue.id)
    story_default_details=issue_fields()
    story_default_details.add("JIRA ID",migr_issue.key)
    story_default_details.add("Summary",migr_issue.fields.summary)
    story_default_details.add("Status",migr_issue.fields.status)
    story_default_details.add("Assignee",migr_issue.fields.assignee)
    validation_results = get_validation_fields(migr_issue)
    validation_results.update(story_default_details)
    epic_stories_details.append(validation_results)
    #epic_stories_details.append(story_default_details)
    #pp.pprint(validation_results)

#print(epic_stories_details)
pd.DataFrame.from_dict(epic_stories_details)
