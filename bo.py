import requests

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
