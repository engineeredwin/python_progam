import requests
import json

# Authenticate the user and create a session object
session = requests.Session()

auth_url = "http://xxx:6405/biprws/logon/long"

username = "xxxx" 
password = "xxxxx"

headers = {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

body = f"""<?xml version="1.0" encoding="UTF-8"?>
<attrs xmlns="http://www.sap.com/rws/bip">
     <attr name="userName" type="string">{username}</attr>
     <attr name="password" type="string">{password}</attr>
</attrs>
"""

response = session.post(auth_url, headers=headers, data=body)

if response.status_code != 200:
    print("Authentication failed")
    exit()

# Get the session token from the response headers
if "X-SAP-LogonToken" not in response.headers:
    print("Error: Session token not found in response headers")
    exit()

session_token = response.headers["X-SAP-LogonToken"]

# Define the URL for getting the content usage data
url = "http://xxx:6405/biprws/audit/reports"

# Define the headers for the request
headers = {
    "Accept": "application/json",
    "X-SAP-LogonToken": session_token
}

# Define the query parameters for the request
params = {
    "dateFrom": "2021-01-01T00:00:00Z",  # Replace with the desired start date and time
    "dateTo": "2021-12-31T23:59:59Z",  # Replace with the desired end date and time
    "format": "json"
}

# Send the GET request to the server using the authenticated session
response = session.get(url, headers=headers, params=params)

# Convert the response to JSON
try:
    response_json = response.json()
except ValueError as e:
    print("Error: Could not parse JSON response:", e)
    print("Response content:", response.content)
    exit()

# Write the response to a JSON file
with open("content_usage.json", "w") as f:
    json.dump(response_json, f)

print(f"Done. Content usage written to content_usage.json.")
