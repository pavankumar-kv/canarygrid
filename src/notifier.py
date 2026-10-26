"""
Project CanaryGrid - SOC Incident Notifier & Audit Logger
Description: Formats Tier-1 security incident cards for the analyst console
             and writes structured JSON logs for SIEM ingestion.
"""
import datetime
import json
import os
class CanaryNotifier:
    """Formats and records deception alerts."""
    def __init__(self):
        # Automatically find the docs/ folder in our project
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_file = os.path.join(project_root, "docs", "incident_audit.jsonl")
    def log_to_audit_file(self, alert_payload: dict):
        """Saves the alert as a structured JSON record for SIEM ingestion."""
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(alert_payload) + "\n")
        except Exception as e:
            print(f"[!] Error writing to audit log: {e}")
    def display_console_alert(self, alert_payload: dict):
        """Prints a high-visibility SOC Incident Card in the terminal."""
        banner = "=" * 70
        print("\n" + banner)
        print(" [!] CRITICAL SECURITY ALERT - CANARY DECEPTION TRIGGERED [!]")
        print(" Severity: CRITICAL | Confidence: 100% (Zero False-Positive Trap)")
        print(banner)
        print(f" Timestamp    : {alert_payload.get('timestamp')}")
        print(f" Trap Type    : {alert_payload.get('trap_type')}")
        print(f" Asset Name   : {alert_payload.get('asset_name')}")
        print(f" Attacker IP  : {alert_payload.get('attacker_ip')} ({alert_payload.get('ip_classification')})")
        print(f" Location     : {alert_payload.get('location')}")
        print(f" Organization : {alert_payload.get('organization')}")
        print(f" User-Agent   : {alert_payload.get('user_agent')}")
        print(f" Details      : {alert_payload.get('description')}")
        print("-" * 70)
        print(" RECOMMENDED SOC TIER-1 ACTION:")
        print(f" -> {alert_payload.get('recommended_action')}")
        print(banner + "\n")
    def dispatch(
        self,
        trap_type: str,
        asset_name: str,
        attacker_ip: str,
        user_agent: str,
        ip_details: dict,
        description: str,
        recommended_action: str = "Isolate target workstation immediately.",
    ):
        """Combines the alert data, prints the card, and logs to file."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        location = f"{ip_details.get('city', 'Unknown')}, {ip_details.get('country', 'Unknown')}"
        organization = f"{ip_details.get('isp', 'Unknown')} ({ip_details.get('org', 'Unknown')})"
        payload = {
            "timestamp": timestamp,
            "trap_type": trap_type,
            "asset_name": asset_name,
            "attacker_ip": attacker_ip,
            "ip_classification": ip_details.get("classification", "Unknown"),
            "location": location,
            "organization": organization,
            "user_agent": user_agent,
            "description": description,
            "recommended_action": recommended_action,
        }
        # 1. Print the alert on screen
        self.display_console_alert(payload)
        # 2. Save it to our audit history file
        self.log_to_audit_file(payload)
        return payload
# Test to see the formatted card
if __name__ == "__main__":
    notifier = CanaryNotifier()
    mock_ip_info = {
        "city": "Frankfurt",
        "country": "Germany",
        "isp": "DigitalOcean Cloud",
        "org": "Hacker VPS",
        "classification": "Datacenter / Cloud VPS (High Suspicion)",
    }
    notifier.dispatch(
        trap_type="AWS Honey-Key Reconnaissance",
        asset_name="prod-backup-service-key (.aws/credentials)",
        attacker_ip="185.220.101.5",
        user_agent="aws-cli/2.15 Python/3.11",
        ip_details=mock_ip_info,
        description="Adversary attempted 'sts:GetCallerIdentity' using stolen decoy cloud keys.",
        recommended_action="Quarantine workstation and revoke compromised AWS credentials.",
    )