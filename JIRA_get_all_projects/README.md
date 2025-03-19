# Jira Project Fetcher

This Python script retrieves all projects visible to the authenticated user from a Jira Cloud instance using the Jira REST API.

## 📌 Features
- Fetches all projects from Jira using the REST API.
- Uses **environment variables** to securely store authentication credentials.
- Handles API errors and exceptions gracefully.
- Prints project details in a readable format.

## Set Environment Variables
- $env:JIRA_EMAIL="your-email@example.com"
- $env:JIRA_API_TOKEN="your-api-token"