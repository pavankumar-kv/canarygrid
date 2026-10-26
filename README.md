 CanaryGrid: Enterprise Active Defense & Cyber Deception Matrix
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE%20ATT%26CK-T1083%20%7C%20T1552.001%20%7C%20T1078.004-red.svg)](https://attack.mitre.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![False Positive Rate](https://img.shields.io/badge/False%20Positive%20Rate-0%25-brightgreen.svg)]()
[![Domain](https://img.shields.io/badge/Domain-SOC%20%2F%20Detection%20Engineering-orange.svg)]()
> **CanaryGrid** is an active defense deception framework designed to catch adversaries during post-exploitation internal reconnaissance. By planting realistic decoy cloud credentials and weaponized tracking documents, CanaryGrid detects unauthorized lateral movement with a **0% false-positive rate** and automatically enriches attacker telemetry using open-source threat intelligence.
---
## The Problem CanaryGrid Solves
Modern Security Operations Centers (SOCs) face severe alert fatigue from noisy heuristic EDR alerts. Meanwhile, adversaries bypass traditional antivirus by using "Living off the Land" techniques to harvest credentials stored in files (`.aws/credentials`, `passwords.txt`).
**The Solution:** Legitimate enterprise users have zero business reason to interact with decoy files. Any access is a guaranteed indicator of malicious activity, allowing SOC analysts to initiate containment procedures within minutes.
---
## Deception Capabilities
| Trap Type | Target Behavior | MITRE ATT&CK | Deception Mechanism |
| :--- | :--- | :--- | :--- |
| **AWS Cloud Honey-Key** | Credential Harvesting & Cloud Recon | **T1552.001**, **T1078.004** | Decoy IAM Access Key; alerts upon `sts:GetCallerIdentity` |
| **Decoy Executive Document** | Sensitive File Discovery | **T1083** | Embedded 1x1 transparent tracking beacon triggers HTTP callback upon opening |
---
## Project Structure
```text
canarygrid/
├── README.md                  # Portfolio documentation
├── .gitignore                 # Secret protection rules
├── docs/
│   ├── THREAT_MODEL.md        # MITRE ATT&CK mappings
│   ├── INCIDENT_PLAYBOOK.md   # Step-by-step SOC Tier-1 triage procedures
│   └── incident_audit.jsonl   # Structured SIEM-compatible JSON Lines alert history
├── src/
│   ├── alert_router.py        # Central HTTP beacon listener & webhook dispatcher
│   ├── ip_enrichment.py       # Threat intelligence engine (GeoIP, Tor/VPN detection)
│   └── notifier.py            # Formatter for SOC console cards and audit logs
├── decoys/
│   ├── seed_decoys.py         # Staging script for decoy files
│   └── staged_assets/         # Staged honey-files
└── tests/
    └── simulate_recon.py      # Automated red-team simulation script testing all traps