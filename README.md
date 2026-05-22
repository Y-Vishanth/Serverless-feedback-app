---

# Serverless Feedback App

A beginner-friendly serverless web application built using AWS services like **Lambda**, **API Gateway**, and **DynamoDB**.

This project demonstrates how a frontend application can send data to a backend API without managing any servers.

---

# Project Architecture

```text
Frontend (HTML/CSS/JavaScript)
        ↓
API Gateway
        ↓
AWS Lambda
        ↓
DynamoDB
```

---

# How This Project Works

1. User enters:

   * Name
   * Feedback message

2. Frontend sends request using JavaScript Fetch API.

3. API Gateway receives the HTTP request.

4. API Gateway triggers AWS Lambda.

5. Lambda processes the request and stores data in DynamoDB.

6. User receives:

```text
Feedback stored successfully!
```

7. Submitted feedback can be viewed inside DynamoDB table items.

---

# Technologies Used

* HTML
* CSS
* JavaScript
* AWS Lambda
* API Gateway
* DynamoDB
* IAM
* Git & GitHub

---

# Project Structure

```text
serverless-feedback-app/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   └── lambda_function.py
│
├── screenshots/
│
├── README.md
```

---

# Step-by-Step Setup Guide

# 1. Clone Repository

```bash
git clone https://github.com/Y-Vishanth/Serverless-feedback-app.git

```

---

# 2. Frontend Setup

Go to:

```text
frontend/
```

Files included:

* `index.html`
* `style.css`
* `script.js`

Run the frontend using:

* VS Code Live Server

OR

Open:

```text
index.html
```

inside browser.

---

# 3. Create DynamoDB Table

Go to:

```text
AWS Console
→ DynamoDB
→ Create Table
```

Use:

| Setting       | Value          |
| ------------- | -------------- |
| Table Name    | Feedback-Table |
| Partition Key | id             |
| Type          | String         |

Keep:

* Default settings
* On-demand capacity

After creation:

* Open table
* Click:

  ```text
  Explore table items
  ```

---

# 4. Create Lambda Function

Go to:

```text
AWS Lambda
→ Create Function
```

Use:

* Runtime: Python 3.x

Function name:

```text
feedback-function
```

---

# 5. Add Backend Code

Go to:

```text
backend/lambda_function.py
```

Copy the code from:

```text
lambda_function.py
```

Paste it inside AWS Lambda code editor.

After pasting:

* Click:

  ```text
  Deploy
  ```

---

# 6. Add DynamoDB Permissions to Lambda

Go to:

```text
Lambda
→ Configuration
→ Permissions
→ Execution Role
```

Attach policy:

```text
AmazonDynamoDBFullAccess
```

This allows Lambda to:

* insert items
* access DynamoDB table

---

# 7. Create API Gateway

Go to:

```text
API Gateway
→ Create API
→ HTTP API
```

Create route:

```text
POST /submit
```

Attach Lambda integration:

```text
feedback-function
```

---

# 8. Configure CORS

Go to:

```text
API Gateway
→ CORS
```

Add:

| Setting       | Value         |
| ------------- | ------------- |
| Allow Origins | *             |
| Allow Headers | content-type  |
| Allow Methods | POST, OPTIONS |

---

# 9. Add OPTIONS Route

Create additional route:

```text
OPTIONS /submit
```

Attach same Lambda integration.

This handles browser preflight requests.

---

# 10. Deploy API

Go to:

```text
Stages
```

Use:

```text
dev
```

Copy:

```text
Invoke URL
```

---

# 11. Update Frontend API URL

Go to:

```text
frontend/script.js
```

Replace fetch URL with:

```text
YOUR_INVOKE_URL/dev/submit
```

Example:

```text
https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/submit
```

---

# 12. Test Application

Run frontend.

Enter:

* name
* feedback

Click:

```text
Submit
```

Expected response:

```text
Feedback stored successfully!
```

---

# 13. Verify Data in DynamoDB

Go to:

```text
DynamoDB
→ Explore table items
```

You should see:

* user name
* feedback message
* generated UUID

stored successfully.

---

# Real Errors Faced During Development

This project involved debugging multiple real-world cloud issues.

---

## 1. CORS Errors

### Problem

Browser blocked requests with:

```text
CORS Error
```

### Fix

Configured:

* CORS settings
* OPTIONS route
* Access-Control-Allow-Origin headers

---

## 2. 404 Preflight Error

### Problem

```text
OPTIONS /submit → 404
```

### Cause

OPTIONS route was missing.

### Fix

Created:

```text
OPTIONS /submit
```

inside API Gateway.

---

## 3. 500 Internal Server Error

### Problem

Lambda crashed during OPTIONS requests.

### Cause

Lambda expected:

```python
event['body']
```

even for OPTIONS requests.

### Fix

Handled:

```text
OPTIONS
```

requests separately.

---

## 4. requestContext KeyError

### Problem

```text
KeyError: requestContext
```

### Cause

Lambda test events differ from API Gateway events.

### Fix

Added safe checks for:

```python
requestContext
```

before accessing HTTP method.

---

# Learning Outcomes

This project helped understand:

* Serverless Architecture
* AWS Lambda
* API Gateway
* DynamoDB
* IAM Permissions
* Fetch API
* CORS Debugging
* HTTP Methods
* Preflight Requests
* Cloud Troubleshooting
* Frontend + Backend Integration

---

# Future Improvements

Possible enhancements:

* Host frontend on S3
* Add CloudFront CDN
* Add Terraform
* Add CI/CD using GitHub Actions
* Add Authentication
* Add CloudWatch Monitoring

---

# Screenshots

Add screenshots inside:

```text
screenshots/
```

Suggested screenshots:

* frontend UI
* Lambda success logs
* DynamoDB items
* API Gateway routes

---

# Author

Vishanth Yelamarthi

---

# Final Result

This project demonstrates a complete serverless workflow where:

```text
Frontend → API Gateway → Lambda → DynamoDB
```

works successfully without managing any servers.
