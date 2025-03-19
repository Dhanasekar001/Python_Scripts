import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Jira API URL for listing projects
url = "https://jitdev.atlassian.net/rest/api/3/project"

# Use environment variables for security
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Ensure environment variables are set
if not EMAIL or not API_TOKEN:
    raise ValueError("JIRA_EMAIL and JIRA_API_TOKEN must be set as environment variables.")

# Authentication using Basic Auth
auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
    "Accept": "application/json"
}

try:
    # Send GET request
    response = requests.get(url, headers=headers, auth=auth)
    
    # Check for HTTP errors
    response.raise_for_status()

    # Parse JSON response
    output = response.json()

    # Debugging: Print the full response to verify structure
    print(json.dumps(output, indent=4, sort_keys=True))

    # Ensure the response is a list and has at least one project
    if isinstance(output, list) and output:
        for project in output:
            name = project.get("name", "Unknown")
            key = project.get("key", "Unknown")
            print(f"Project Name: {name}, Project Key: {key}")
    else:
        print("No projects found.")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
