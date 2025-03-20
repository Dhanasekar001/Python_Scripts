# 🚀 GitHub to Jira Issue Creator  

A **Flask-based webhook** that listens for GitHub commits and automatically creates a **Jira issue** when a commit message contains `/createJiraIssue`.

---

## 📌 Features
- ✅ Listens for GitHub commit **webhook events**  
- ✅ Creates **Jira issues** dynamically  
- ✅ Uses **Jira REST API v3**  
- ✅ Secured using **environment variables**  

## Set Environment Variables
- $env:JIRA_EMAIL="your-email@example.com"
- $env:JIRA_API_TOKEN="your-api-token"

## 🖥️ Running the Flask App
To start the Flask server, run:

```bash
python Github_Jira.py
```
The application will start on:
```bash
http://0.0.0.0:5000
```

## 🔗 Connecting to GitHub Webhook
- 1️⃣ Go to Your GitHub Repository
  Navigate to Settings > Webhooks > Add Webhook.
- 2️⃣ Configure the Webhook
    **Payload URL**: http://your-public-ngrok-url/createJira
    **Content type**: application/json
    **Events**: Select **Issue comments**.
    Click **Add webhook**.
- 3️⃣ Expose Localhost (If Running Locally)
    If you are running the Flask app on your local machine, use **ngrok** to expose it:
    ```bash
    ngrok http 5000
    ```
    Copy the **ngrok public URL** and use it as the **Payload URL** in GitHub.

## 📝 How It Works
- You push a commit containing **/createJiraIssue** in the commit message.
- GitHub sends a webhook event to the Flask app.
- The Flask app processes the event and checks if the commit message contains **/createJiraIssue**.
- If found, a Jira issue is created automatically! 🎉