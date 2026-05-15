
# Serverless Student / Business Dashboard 

This project is a serverless backend for a Student or Business Dashboard application. It is built entirely on AWS using three services — Lambda, API Gateway, and DynamoDB. There are no servers to set up or maintain. Everything is deployed through the AWS Console and runs within the AWS Free Tier.

![AWS Architecture Diagram](architecture.png)

---

## What This Project Does

When a user or a frontend application sends an HTTP request to the API, it first reaches API Gateway. API Gateway then triggers the correct Python Lambda function depending on whether the request is creating, reading, updating, or deleting a record. The Lambda function processes the request and reads or writes data in DynamoDB. Finally, it sends a JSON response back to the caller. The whole flow happens in milliseconds and you never have to think about a server.

---

## Prerequisites

Before you start, you need an AWS account. You can create one for free at https://aws.amazon.com/free. Everything in this project fits within the AWS Free Tier. Lambda gives you one million free requests every month, API Gateway gives you one million free API calls per month for the first twelve months, and DynamoDB gives you twenty-five gigabytes of free storage plus free read and write capacity forever.

---

## Step 1 — Create the DynamoDB Table

Log in to the AWS Console and type DynamoDB in the search bar at the top of the page. Click on it to open the service. Once inside, click the Create table button. Set the table name to ItemsTable and set the partition key to id with the type set to String. Leave everything else on the page at its default value and click Create table at the bottom. Wait about thirty seconds until the table status shows Active. The table name must be exactly ItemsTable with that exact spelling and capitalisation because the Lambda functions refer to it by that exact name.

---

## Step 2 — Create an IAM Role for Lambda

Lambda functions need permission to read and write to DynamoDB. You grant this permission through an IAM Role. Go to the AWS Console search bar and type IAM, then open it. Click Roles in the left sidebar and then click Create role. Under Trusted entity type, select AWS service. Under Use case, choose Lambda and click Next. On the permissions page, search for AmazonDynamoDBFullAccess and tick it, then search for AWSLambdaBasicExecutionRole and tick that too. Click Next, give the role the name LambdaDynamoDBRole, and click Create role.

---

## Step 3 — Zip the Lambda Functions

Download the lambdas folder from this repository. Each Python file needs to be zipped individually before you can upload it to AWS. Open a terminal inside the lambdas folder and run the following commands one by one.

```
zip create_item.zip create_item.py
zip get_items.zip get_items.py
zip get_item.zip get_item.py
zip update_item.zip update_item.py
zip delete_item.zip delete_item.py
```

If you are on Windows and do not have a terminal, you can right-click each Python file, choose Send to, then Compressed zipped folder, and rename the resulting zip file to match the names above. You should end up with five zip files ready to upload.

---

## Step 4 — Deploy the Lambda Functions

You need to create five Lambda functions in AWS, one for each operation. The process is the same for all five — just use a different name and zip file each time. The five functions are CreateItem using create_item.zip with handler create_item.lambda_handler, GetItems using get_items.zip with handler get_items.lambda_handler, GetItem using get_item.zip with handler get_item.lambda_handler, UpdateItem using update_item.zip with handler update_item.lambda_handler, and DeleteItem using delete_item.zip with handler delete_item.lambda_handler.

For each one, go to Lambda in the AWS Console and click Create function. Choose Author from scratch. Enter the function name, set the runtime to Python 3.12, then expand the section called Change default execution role, select Use an existing role, and pick LambdaDynamoDBRole from the dropdown. Click Create function. Once the function is created, go to the Code tab, click Upload from and then select .zip file, upload the matching zip file, and click Save. Scroll down to Runtime settings, click Edit, type in the handler value from the list above, and click Save.

Repeat this five times until all five functions are deployed. To confirm everything is working, open the GetItems function, click the Test tab, create a test event with any name and leave the body as an empty set of curly braces, then click Test. You should see a green success box showing an empty list of items.

---

## Step 5 — Create the API Gateway

Go to API Gateway in the AWS Console and click Create API. Choose REST API and click Build. Select New API, name it DashboardAPI, set the endpoint type to Regional, and click Create API.

Once inside the API, you will see a resource tree on the left with just a forward slash representing the root. Click on the root, then click Create resource. Name it items, tick the CORS checkbox, and click Create resource. With the items resource selected, click Create method and add a GET method that points to the GetItems Lambda function with Lambda proxy integration turned on. Then add a POST method the same way pointing to CreateItem.

Next, click on the items resource in the tree and click Create resource again. Name this one with just the text id wrapped in curly braces like this: {id}. Tick CORS and click Create resource. On this new resource add a GET method pointing to GetItem, a PUT method pointing to UpdateItem, and a DELETE method pointing to DeleteItem. Make sure Lambda proxy integration is turned on for all three.

When you are done adding all the methods, click Deploy API. Choose New stage, name the stage dev, and click Deploy. You will see an Invoke URL appear at the top of the page. It looks something like https://abc123.execute-api.us-east-1.amazonaws.com/dev. Copy this URL and save it because you will use it to call your API.

---

## Step 6 — Test the API

Replace YOUR_API_URL in the examples below with the Invoke URL you copied in the previous step.

To create a new record, send a POST request like this:

```
curl -X POST https://YOUR_API_URL/dev/items -H "Content-Type: application/json" -d '{"name": "Student A", "description": "Year 2, Computer Science", "status": "active"}'
```

To get all records, send a GET request like this:

```
curl https://YOUR_API_URL/dev/items
```

To get a single record, take the id value from the response above and send this request replacing ITEM_ID with that value:

```
curl https://YOUR_API_URL/dev/items/ITEM_ID
```

To update a record:

```
curl -X PUT https://YOUR_API_URL/dev/items/ITEM_ID -H "Content-Type: application/json" -d '{"name": "Student A", "status": "graduated"}'
```

To delete a record:

```
curl -X DELETE https://YOUR_API_URL/dev/items/ITEM_ID
```

If you prefer not to use the terminal, you can download Postman from https://www.postman.com/downloads which gives you a visual interface to send these requests.

---

## Troubleshooting

If you get a 500 Internal Server Error, open the Lambda function in the console, click the Monitor tab, and click View CloudWatch logs. The logs will show you the exact error message from the Python code.

If you get an AccessDeniedException, the IAM role is missing permissions. Go to IAM, open the LambdaDynamoDBRole, and confirm that AmazonDynamoDBFullAccess is attached to it.

If you get a ResourceNotFoundException saying the table was not found, make sure the DynamoDB table is named exactly ItemsTable and that it is in the same AWS region as your Lambda functions.

If the Lambda test passes but API Gateway returns an error, check that Lambda proxy integration is enabled on every method. Any time you make a change to API Gateway, you must redeploy it to the dev stage for the changes to take effect.

---

## Cleaning Up

When you are done with the project and want to make sure you are not charged for anything, delete the resources in this order. First delete the API in API Gateway by selecting DashboardAPI and choosing delete. Then delete all five Lambda functions. Then go to DynamoDB and delete the ItemsTable. Finally go to IAM, open Roles, and delete LambdaDynamoDBRole.

---

## License

MIT
