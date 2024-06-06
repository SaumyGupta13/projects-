#get IP information using "ipinfo.io"

import requests  # to make HTTP request and interact with web services

def get_ip_info(ip_address):  #returns a dictionary
#for querying the ip address
    try:
        url = f"http://ipinfo.io/{ip_address}"  #constructs url for "ipinfo.io"
        response = requests.get(url)  #HTTP GET request to the constructed url

        if response.status_code == 200: #successful request
            ip_info = response.json()   #extract json information
            return ip_info
        else:  #unsuccessful request
            return f"Failed to retrieve information for {ip_address}"

    except requests.exceptions.Timeout:
        return f"Connection to {ip_address} timed out"
    except requests.exceptions.RequestException as e:
        return str(e)

# Replace "8.8.8.8" with the IP address you want to query
ip_address = "8.8.8.8"
result = get_ip_info(ip_address)

if isinstance(result, dict):#if fuction call returns dictionary
    print("IP Location: ", result.get("city"))
    print("IP Format: ", "IPv4" if "." in ip_address else "IPv6")
    print("Header Size: ", len(str(result)))
    print("Header Content: ")
    for key, value in result.items():
        print(f"{key}: {value}")
else:
    print(result)
