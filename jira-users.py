#from operator import truediv
from jira import JIRA
import os
import warnings
import sys

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json


#jira_id = sys.argv[1]
jira_base_url = os.environ.get("JIRA_CLOUD_URL")
username = os.environ.get("JIRA_USER_LOCAL")
apikey = os.environ.get("JIRA_TOKEN_LOCAL")



url = jira_base_url

auth = HTTPBasicAuth(username, apikey)

headers = {
   "Accept": "application/json"
}

query = {
   'query': 'query'
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))



#jira = JIRA(options = {'server':jira_base_url, 'verify':False}, basic_auth = (username, apikey))

#users = jira.search_users('Vibhor') 
#print(users)

#for user in jira.group_members("administrators"):        
#    info = jira.user(user)        
#    print(info)
