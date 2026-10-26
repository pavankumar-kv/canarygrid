# Threat Model: Project CanaryGrid

## 1. Executive Summary
Project CanaryGrid is an Active Defense and Cyber Deception Matrix engineered to detect unauthorized post-compromise activity inside an enterprise boundary. Rather than relying solely on signature-based detection (which produces high false-positive rates), CanaryGrid plants high-value decoy credentials and sensitive documents. 
Because legitimate users have zero business reason to interact with these decoy artifacts, **any interaction generates an alert with a 0% false-positive rate**.


## 2. MITRE ATT&CK Mapping
| Technique ID | Technique Name | CanaryGrid Decoy Asset | Deception Mechanism |
| :--- | :--- | :--- | :--- |
| **T1083** | File & Directory Discovery | Decoy Sensitive Document (`Executive_Compensation_Q4_Confidential.html`) | Invisible 1x1 image beacon triggered upon document open |
| **T1552.001** | Credentials in Files | Decoy `.aws/credentials` (`aws_credentials_decoy`) | Fake AWS key triggering automated cloud reconnaissance alerts |
| **T1078.004** | Cloud Accounts | Stolen Cloud IAM Credentials | Alerts upon `sts:GetCallerIdentity` probe |


## 3. Defense Guarantees
1. **Zero False Positives:** Decoys are never accessed by regular staff. Any trigger is high-confidence malicious activity.
2. **Early Kill-Chain Interception:** Catches the adversary during early discovery, long before data exfiltration or ransomware deployment.

  