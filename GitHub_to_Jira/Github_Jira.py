from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Define the Jira API URL
JIRA_URL = "https://jitdev.atlassian.net/rest/api/3/issue"

# Use environment variables for security
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN") 

print("JIRA Email:", EMAIL)
print("JIRA API Token:", API_TOKEN)

auth = HTTPBasicAuth(EMAIL, API_TOKEN)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

app = Flask(__name__)

@app.route('/createJira', methods=['POST'])
def create_jira():
    """Handles GitHub webhook and creates a Jira issue if commit message contains '/createJiraIssue'."""
    
    # ✅ Fix: Use Flask's request.get_json(), not requests.get_json()
    data = request.get_json()

    if not data or "comment" not in data:
        return jsonify({"error": "No comment found"}), 400

    commit_message = data["comment"]["body"]

    # ✅ Fix: `any()` requires an iterable, but you're checking a single string
    if "/createJiraIssue" in commit_message:
        payload = json.dumps({
            "fields": {
                "summary": "First JIRA Issue",
                "description": {
                    "content": [
                        {
                            "content": [
                                {"text": "My first bug report", "type": "text"}
                            ],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                "issuetype": {"id": "10009"},  # Verify the correct issue type ID
                "project": {"key": "SAM"}
            }
        })

        # Send the request to Jira API
        response = requests.post(JIRA_URL, data=payload, headers=headers, auth=auth)

        if response.status_code == 201:
            return jsonify({"message": "JIRA issue created successfully"}), 200
        else:
            return jsonify({"error": "Failed to create JIRA issue", "details": response.json()}), response.status_code

    return jsonify({"message": "No Jira issue created. Commit message did not contain '/createJiraIssue'"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
