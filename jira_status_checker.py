from operator import truediv
from jira import JIRA
import os
import warnings
import sys


jira_id = sys.argv[1]
jira_base_url = os.environ.get("JIRA_CLOUD_URL")
username = os.environ.get("JIRA_USER")
pwd = os.environ.get("JIRA_TOKEN")

jira = JIRA(options = jira_base_url,
			basic_auth = (username,
						pwd))

singleIssue = jira.issue(jira_id)
print('{}: {}:{}'.format(singleIssue.key,
						singleIssue.fields.summary,
                        singleIssue.fields.status,
						singleIssue.fields.reporter.displayName))
print(singleIssue)

def jira_status_checker():
  if singleIssue.status in ["To Do", "Done"]:
    return false
  elif singleIssue.status in ["In Progress"]:
    return true

jira_status_checker()
