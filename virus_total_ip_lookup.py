#!/usr/bin/python3
# Script Name: virus_total_ip_lookup.py
# Purpose: Use to lookup Virus Total Stats for an IP address
# Written By: Will Armijo
# Created on: 01/11/2025

'''
Please note that this script is not compliant with security as the API key is statically assigned. 
This can be updated to retrieve the API key from a protected file, user input, or user environment variable. 
'''

import requests
import json
import pandas as pd
from pandas import json_normalize

ip_addr = input("Please Enter an IP Address: ")
api_key = "<Replace with your own API Key>"
url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_addr}"

# Set up the headers
header = {
    'X-Apikey': f'{api_key}',
    'Content-Type': 'application/json'
}

response = requests.get(url, headers=header)
print("Retreiving ", {url})

if response.status_code == 200:
    vt_data = response.text
    
    df = pd.read_json(vt_data)

    ioc_total = df['data']
    ioc_country = ioc_total['attributes']['country']
    ioc_ip = df['data']['id']
    ioc_atrb = df['data']['attributes']
    network = ioc_atrb['network']
    ioc_rep = ioc_atrb['reputation']
    ioc_tags = ioc_atrb['tags']
    ioc_results = df['data']['attributes']['last_analysis_stats']

    print("")
    print("IoC Results for", ioc_ip)
    print("=====================================")
    print("")
    print("Target IP: ", ioc_ip)
    print("Target Network", network)
    print("IoC Country: ", ioc_country)
    print("")
    print("=====================================")
    print("Antimalware Scan Engines IoC Results: ")
    print("")
    print("Found to be Malicious ", ioc_results['malicious'], "times")
    print("Found to be Suspicious ", ioc_results['suspicious'], "times")
    print("Found to be Undetected ", ioc_results['undetected'], "times")
    print("Found to be Harmless ", ioc_results['harmless'], "times")
    print("")

else:
    print("Request failed with status", {response.status_code}, {response.text})
