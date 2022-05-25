from operator import truediv
from jira import JIRA
import os
import warnings
import sys


jira_id = sys.argv[1]
jira_base_url = os.environ.get("JIRA_CLOUD_URL")
username = os.environ.get("JIRA_USER_LOCAL")
apikey = os.environ.get("JIRA_TOKEN_LOCAL")

jira = JIRA(options = {'server':jira_base_url, 'verify':False}, basic_auth = (username, apikey))

singleIssue = jira.issue(jira_id)
print('{}: {}:{}'.format(singleIssue.key, singleIssue.fields.summary, singleIssue.fields.status, singleIssue.fields.reporter.displayName))
print(singleIssue)

if singleIssue.status in ["To Do", "Done"]:
  print('JIRA is in {} status therefore, cannot perform actions on it'.format(singleIssue.key)) && sys.exit(0)
elif singleIssue.status in ["In Progress"]:
  print("JIRA is in In-Progress Status")

