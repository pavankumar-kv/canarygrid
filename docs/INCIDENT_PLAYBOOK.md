# SOC Tier-1 Incident Response Playbook: CanaryGrid Alerts


## 1. Severity & Triage
* **Alert Severity:** `CRITICAL` (P1)
* **Detection Confidence:** `100%` (Zero False-Positive Active Defense Trap)
* **Assumption:** Host compromise or active insider reconnaissance in progress.

## 2. Immediate Containment Procedure (First 15 Minutes)
### Procedure A: Decoy Document Web Beacon Triggered
1. **Identify the Host:** Look at the `attacker_ip` and `user_agent` reported on the CanaryGrid alert card.
2. **Check Running Processes:** Verify which user opened the document:
   ```powershell
   Get-Process -Name chrome, msedge, WINWORD -ErrorAction SilentlyContinue
3. Isolate Host: If unauthorized, disconnect the computer from the network to prevent lateral movement.

Procedure B: AWS Honey-Key Reconnaissance Detected

1. Check the IP Origin: If the IP is flagged as Datacenter / Cloud VPS or Tor Exit Node, an external attacker has exfiltrated the credentials.
2. Deactivate the Key: Revoke active cloud sessions immediately.
3. Trace Compromise Point: Identify which workstation had the stolen key file.


## 3. Post-Incident Review & Root Cause Analysis
1. Determine how the attacker originally entered the machine (phishing, unpatched software, stolen credentials).
2. Review endpoint logs 4 hours prior to the canary trigger to scope lateral discovery.
3. Re-seed new, rotated canary credentials across the environment.
4.Update firewall rules to block the attacker's observed IP addresses.