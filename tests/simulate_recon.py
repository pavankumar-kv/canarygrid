"""
Project CanaryGrid - Adversary Reconnaissance Simulator
Description: Emulates a real attacker performing internal discovery
             and interacting with CanaryGrid decoys.
"""
import os
import re
import sys
import time
import requests
ROUTER_URL = "http://localhost:8080"
def check_if_server_is_online() -> bool:
    """Verifies that our Alert Router is running before attacking."""
    try:
        resp = requests.get(f"{ROUTER_URL}/health", timeout=3)
        return resp.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
def attack_scenario_1_open_document():
    """Scenario 1: Attacker finds and opens the confidential document (MITRE T1083)."""
    print("\n" + "-" * 65)
    print(" [*] ATTACK SCENARIO 1: Attacker Discovers & Opens Sensitive Document")
    print("     MITRE ATT&CK: T1083 (File and Directory Discovery)")
    print("-" * 65)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc_path = os.path.join(project_root, "decoys", "staged_assets", "Executive_Compensation_Q4_Confidential.html")
    if not os.path.exists(doc_path):
        print(f" [!] Error: Decoy file '{doc_path}' not found. Run seed_decoys.py first.")
        return
    # Attacker reads the file
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    # The browser automatically parses the hidden beacon image
    match = re.search(r'<img src="([^"]+)"', content)
    if not match:
        print(" [!] No beacon found in document.")
        return
    beacon_url = match.group(1)
    print(f" [+] Attacker opened: {doc_path}")
    print(f" [+] Browser secretly requests tripwire pixel: {beacon_url}")
    # Send the request just like a browser does
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
    }
    resp = requests.get(beacon_url, headers=headers, timeout=5)
    if resp.status_code == 200:
        print(" [SUCCESS] Document tripwire sprang! (1x1 transparent image returned)")
def attack_scenario_2_cloud_key_probe():
    """Scenario 2: Attacker abuses stolen AWS honey-key (MITRE T1552 & T1078)."""
    print("\n" + "-" * 65)
    print(" [*] ATTACK SCENARIO 2: Attacker Probes Stolen AWS Honey-Key")
    print("     MITRE ATT&CK: T1552.001 (Credentials in Files) & T1078 (Cloud Accounts)")
    print("-" * 65)
    # Simulating an attacker using the AWS CLI from a foreign IP address
    payload = {
        "access_key_id": "AKIAIOSFODNN7EXAMPLE",
        "event_name": "sts:GetCallerIdentity",
        "source_ip": "185.220.101.5",  # Simulated Tor Exit Node in Germany
        "useragent": "aws-cli/2.15.15 Python/3.11.6 Linux/5.15",
    }
    print(f" [+] Attacker found key: {payload['access_key_id']}")
    print(f" [+] Attacker executes: 'aws sts get-caller-identity' from IP: {payload['source_ip']}")
    resp = requests.post(f"{ROUTER_URL}/webhook/aws", json=payload, timeout=5)
    if resp.status_code == 200:
        print(" [SUCCESS] Cloud Honey-Key alert dispatched to Alert Router!")
def run_full_attack():
    print("\n" + "=" * 65)
    print("   PROJECT CANARYGRID: AUTOMATED ADVERSARY ATTACK SIMULATION")
    print("=" * 65)
    if not check_if_server_is_online():
        print(f"\n[!] ERROR: Alert Router is not running at {ROUTER_URL}")
        print("    You must start 'python src/alert_router.py' first in another window!\n")
        sys.exit(1)
    print("\n[+] Alert Router is ONLINE. Commencing simulated attack in 2 seconds...")
    time.sleep(2)
    attack_scenario_1_open_document()
    time.sleep(3)
    attack_scenario_2_cloud_key_probe()
    print("\n" + "=" * 65)
    print(" [SUCCESS] Attack Complete! Look at your Alert Router window.")
    print("=" * 65 + "\n")
if __name__ == "__main__":
    run_full_attack()

  