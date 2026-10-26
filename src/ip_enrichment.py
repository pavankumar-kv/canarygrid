"""
Project CanaryGrid - Threat Intelligence & IP Enrichment Engine
Description: Enriches an attacker's IP address with Geolocation, ISP, 
             and flags whether they are using a VPN, Cloud VPS, or Tor.
"""


import ipaddress
import logging
import requests
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("IPEnrichment")
class IPEnrichment:
    """Enriches IP addresses using OSINT data sources."""
    @staticmethod
    def is_private_ip(ip_str: str) -> bool:
        """Checks if the IP belongs to a private local network (like 192.168.x.x or 127.0.0.1)."""
        try:
            ip_obj = ipaddress.ip_address(ip_str.strip())
            return ip_obj.is_private or ip_obj.is_loopback
        except ValueError:
            return False
    @classmethod
    def lookup(cls, ip_str: str) -> dict:
        """Looks up location and threat classification for an IP address."""
        ip_clean = ip_str.strip()
        # 1. If it's a private internal IP (inside your office/home network)
        if cls.is_private_ip(ip_clean):
            return {
                "ip": ip_clean,
                "type": "Internal Private Network",
                "country": "Local Office / Lab",
                "city": "Intranet",
                "isp": "Private Enterprise Subnet",
                "org": "Internal Workstation",
                "classification": "Internal Reconnaissance Candidate (Insider Threat)",
            }
        # 2. If it's a public internet IP, ask the OSINT database (ip-api)
        try:
            url = f"http://ip-api.com/json/{ip_clean}?fields=status,country,city,regionName,isp,org,as,hosting,proxy"
            response = requests.get(url, timeout=4)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    is_hosting = data.get("hosting", False)
                    is_proxy = data.get("proxy", False)
                    # Classify the threat level
                    classification = "Residential / Corporate Internet"
                    if is_hosting:
                        classification = "Datacenter / Cloud VPS (High Suspicion)"
                    elif is_proxy:
                        classification = "VPN / Tor / Proxy (High Suspicion)"
                    return {
                        "ip": ip_clean,
                        "type": "Public Internet",
                        "country": data.get("country", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "region": data.get("regionName", "Unknown"),
                        "isp": data.get("isp", "Unknown"),
                        "org": data.get("org", "Unknown"),
                        "classification": classification,
                    }
        except Exception as e:
            logger.warning(f"Lookup failed for {ip_clean}: {e}")
        # Fallback if internet is disconnected
        return {
            "ip": ip_clean,
            "type": "Public Internet",
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Offline / Unavailable",
            "org": "Offline / Unavailable",
            "classification": "Unverified Public Endpoint",
        }
    
# Quick test when running this file directly
if __name__ == "__main__":
    print("\n--- Test 1: Checking a Local/Internal IP ---")
    local_result = IPEnrichment.lookup("192.168.1.50")
    print(f"IP: {local_result['ip']}")
    print(f"Classification: {local_result['classification']}")
    print("\n--- Test 2: Checking a Public IP (Cloudflare 1.1.1.1) ---")
    public_result = IPEnrichment.lookup("8.8.8.8")
    print(f"IP: {public_result['ip']}")
    print(f"Country: {public_result['country']}, {public_result['city']}")
    print(f"ISP: {public_result['isp']}")
    print(f"Classification: {public_result['classification']}\n")