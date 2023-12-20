#url information given url

import socket
import urllib.parse
import requests
import ssl

def get_ip_info(ip_address):
    try:
        url = f"http://ipinfo.io/{ip_address}/json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to retrieve information for {ip_address}"}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_ssl_info(url):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((url, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                cert = ssock.getpeercert()
                return cert

    except (ssl.CertificateError, ssl.SSLError, socket.gaierror) as e:
        return {"error": str(e)}

def get_url_info(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        ip_address = socket.gethostbyname(domain)
        ip_info = get_ip_info(ip_address)
        ssl_info = get_ssl_info(domain)

        return {
            "Protocol": parsed_url.scheme,
            "Domain": domain,
            "Subdomain": domain.split(".", 1)[0] if "." in domain else None,
            "Top-Level Domain (TLD)": domain.split(".")[-1] if "." in domain else None,
            "Path": parsed_url.path,
            "Query Parameters": parsed_url.query,
            "Fragment Identifier": parsed_url.fragment,
            "IP Version": "IPv4" if "." in ip_address else "IPv6",
            "IP Address": ip_address,
            "Network Routing": ip_info.get("org"),
            "ASN (Autonomous System Number)": ip_info.get("asn"),
            "Reverse DNS": ip_info.get("hostname"),
            "Abuse Reports": ip_info.get("abuse"),
            "Domain Ownership": None,  # Requires WHOIS lookup
            "SSL Certificate": ssl_info,
            "Redirects": None,  # Requires following redirects
            "Parameters and Query Strings": None,  # Parsing HTML content
            "URL Structure": None,  # Parsing HTML content
            "Web Application Framework": None,  # Parsing HTML content
        }
    except socket.gaierror:
        return {"error": f"Failed to resolve IP address for {url}"}

def main():
    url = input("Enter a URL: ")
    url_info = get_url_info(url)

    if "error" in url_info:
        print(url_info["error"])
    else:
        for key, value in url_info.items():
            if key == "SSL Certificate":
                print(f"{key}:\n{value}")
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()
