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

# Define the URL for getting the list of documents
url = "http://xxx:6405/biprws/v1/cmsquery"
query = "SELECT si_name,si_id FROM CI_INFOOBJECTS WHERE si_kind='CrystalReport'"

# Define the headers for the request
headers = {
    "Accept": "application/json",
    "X-SAP-LogonToken": session_token
}

# Define the query parameters for the request
params = {
    "query": query,
    "limit": "-1" # -1 returns all results
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

# Check if the response contains the expected key
if "entries" not in response_json:
    print("Error: Response does not contain 'entries' key")
    print("Response content:", response.content)
    exit()

# Get the list of reports
reports = [(e["content"]["values"][0], e["content"]["values"][1]) for e in response_json["entries"]]

# Print the list of reports
print(f"Done. {len(reports)} reports found in the system.")
for report in reports:
    print(f"{report[0]} - {report[1]}")
