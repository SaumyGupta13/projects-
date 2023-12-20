#ip information given url

import socket
import requests
import urllib.parse

def get_url_info(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc

        # Resolve the IP address of the host
        ip_address = socket.gethostbyname(host)

        # Retrieve additional information using the IP address
        url_info = get_ip_info(ip_address)
        url_info["Hostname"] = host
        url_info["URL"] = url

        return url_info

    except socket.gaierror:#error if hostname cannot be resolved to ip address
        return {"error": f"Failed to resolve IP address for {url}"}
    except requests.exceptions.RequestException as e:# if any exception occur in HTTP request
        return {"error": str(e)}

def get_ip_info(ip_address):
    try:
        url = f"http://ipinfo.io/{ip_address}/json"
        response = requests.get(url)

        if response.status_code == 200:
            ip_info = response.json()
            return ip_info
        else:
            return {"error": f"Failed to retrieve information for {ip_address}"}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    url = input("Enter a URL: ")
    url_info = get_url_info(url)

    if "error" in url_info:
        print(url_info["error"])
    else:
        for key, value in url_info.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
