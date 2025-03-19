import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Jira API URL for listing projects
url = "https://jitdev.atlassian.net/rest/api/3/issue"

# Use environment variables for security
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN") 

# Authentication using Basic Auth
auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "fields": {
    "description": {
      "content": [
        {
          "content": [
            {
              "text": "My first bug report",
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    # story type issue
    "issuetype": {
      "id": "10009"
    },
    "project": {
      "key": "SAM"
    },
    "summary": "First JIRA Issue",
  },
  "update": {}
} )

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))