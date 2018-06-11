"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
"""
@author Amit Agarwal
"""
"""
This script triggers ReST queries to the DNA Center
"""
import requests, base64, json, sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_device_by_serial(serial_no):
    #read DNAC instance
    fh = open('dnac_instance.conf')
    lines = list(fh)
    fh.close()
    dnac_ip = lines[0].split("=")[1].strip()
    un = lines[1].split("=")[1].strip()
    pw = lines[2].split("=")[1].strip()
    #Do Auth
    encodedvalue = un+":"+pw
    b64Val = base64.b64encode(encodedvalue.encode('UTF-8')).decode('utf-8')
    DNAC_URL = 'https://'+dnac_ip+'/api/system/v1/auth/login'

    try:
        print("trying auth ...")
        r = requests.get(DNAC_URL, headers={"Authorization": "Basic %s" % b64Val,"Content-Type": "application/json"}, verify=False)
        r.raise_for_status()
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:",errt)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:",errc)
        sys.exit(1)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:",errh)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else",err)
        sys.exit(1)
    print(r.text)

    #getting the cookie value from the returned header to set authentication for the rest of the session
    a=r.headers['Set-Cookie'].split(";")
    b=a[0].split("=")
    c=b[1]
    cookie = {'X-JWT-ACCESS-TOKEN':c}

    #Fetch device by serial no.
    tg = 'https://'+dnac_ip+'/api/v1/network-device/serial-number/'+serial_no
    try:
        r = requests.get(tg, cookies=cookie, verify=False)
        r.raise_for_status()
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        sys.exit(1)
    except requests.exceptions.HTTPError as errh:
        print("Serial no. not found ",  serial_no)
        print("Http Error:", errh)
        return
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        sys.exit(1)
    response = json.loads(r.text)

    finalResp = {}
    finalResp['_id'] = response["response"]["serialNumber"]
    finalResp['class'] = response["response"]["series"]
    finalResp['ipAddr'] = response["response"]["managementIpAddress"]
    finalResp['mac'] = response["response"]["macAddress"]
    finalResp['type'] = response["response"]["family"]
    if response["response"]["collectionStatus"] == 'Managed':
        finalResp['health'] = 'status-green'
    else:
        finalResp['health'] = 'status-red'
    finalResp['hostname'] = response["response"]["hostname"]
    json_data = json.dumps(finalResp)
    print(json_data)
    return json_data
