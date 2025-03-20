from flask import Flask, request , jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Define the Jira API URL
JIRA_URL = "https://your-jira-instance.atlassian.net/rest/api/3/issue"

# Use environment variables for security
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN") 
auth = HTTPBasicAuth(EMAIL, API_TOKEN)

app = Flask(__name__)

# Create a route that will accept POST requests and create a JIRA issue
@app.route('/createJira', methods=['POST'])
def github_webhook():
    """ Handles GitHub webhook and creates Jira issue if the commit message contains '/createJiraIssue'. """

    # Get JSON payload from GitHub
    data = request.get_json()

    # Check if it contains 'commits'
    if "commits" not in data:
        return jsonify({"error": "No commits found"}), 400

    # Extract commit messages
    commit_messages = [commit["message"] for commit in data["commits"]]

    # Debugging: Print commit messages
    print("Received commit messages:", commit_messages)

    # Check if any commit message contains "/createJiraIssue"
    if any("/createJiraIssue" in message for message in commit_messages):
        return create_jira_issue()

    return jsonify({"message": "No Jira issue created. Commit message did not contain '/createJiraIssue'"}), 200

def create_jira_issue():
    """ Creates a Jira issue when triggered. """

    payload = json.dumps({
        "fields": {
            "summary": "GitHub Commit Triggered Jira Issue",
            "description": {
                "content": [
                    {
                        "content": [
                            {
                                "text": "Automatically created from a GitHub commit.",
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            },
            "issuetype": {"id": "10009"},  # Issue Type ID (e.g., Story, Bug)
            "project": {"key": "SAM"}  # Jira Project Key
        }
    })

    try:
        # Send request to Jira API
        headers = {"Content-Type": "application/json"}  # Define headers with content type
        response = requests.post(JIRA_URL, headers=headers, auth=auth, data=payload)
        response_data = response.json()

        # Check for errors in Jira API response
        if response.status_code != 201:
            return jsonify({"error": "Failed to create Jira issue", "details": response_data}), response.status_code

        return jsonify({"message": "Jira issue created successfully", "jira_response": response_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)