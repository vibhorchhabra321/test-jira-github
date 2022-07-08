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
#print('{}: {}:{}'.format(singleIssue.key, singleIssue.fields.summary, singleIssue.fields.status, singleIssue.fields.reporter.displayName))
jira_status = str(singleIssue.fields.status)
#print(singleIssue)
#print(jira_status)

for user in jira.group_members("jira-administrators"):        
    info = jira.user(user)        
    print(info.name, info.emailAddress)

if jira_status not in ["To Do", "Done"]:
  sys.exit(0)
else:
  sys.exit(1)

