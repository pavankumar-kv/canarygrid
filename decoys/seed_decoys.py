"""
Project CanaryGrid - Decoy Asset Seeder
Description: Automatically generates and places realistic honey-files (bait)
             to catch adversaries performing internal reconnaissance.
"""
import os
# 1. The fake confidential document with the hidden tripwire image
DECOY_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>CONFIDENTIAL: Executive Compensation & Bonus Allocations Q4</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }}
        .header {{ border-bottom: 2px solid #b30000; padding-bottom: 10px; color: #b30000; }}
        .warning {{ background-color: #ffe6e6; border: 1px solid #cc0000; padding: 10px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>CONFIDENTIAL - FOR BOARD OF DIRECTORS ONLY</h2>
    </div>
    <div class="warning">
        <strong>RESTRICTED ACCESS:</strong> Unauthorized access to compensation records is strictly prohibited.
    </div>
    <p>Document Tracking Reference: DOC-REF-2026-X99</p>
    <!-- Invisible Tripwire Beacon (1x1 transparent image) -->
    <img src="{beacon_url}" width="1" height="1" alt="" style="display:none;" />
</body>
</html>
"""
# 2. The fake AWS cloud credentials file
DECOY_AWS_TEMPLATE = """# AWS Production Automated Deployment & Backup Profile
# Managed by Terraform - DO NOT EDIT MANUALLY
# Last Rotated: 2026-09-14T08:12:00Z
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-east-1
output = json
[prod-db-backup-svc]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-west-2
"""
# 3. The fake database configuration
DECOY_ENV_TEMPLATE = """# Enterprise Database Staging Secrets
DB_HOST=staging-db.internal-enterprise.corp
DB_PORT=5432
DB_USER=svc_analytics_admin
DB_PASS=Sup3rS3cur3P@ssw0rd!2026
"""
def plant_all_decoys():
    """Generates and plants the bait files."""
    # Find our project root folder
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(project_root, "decoys", "staged_assets")
    os.makedirs(target_dir, exist_ok=True)
    print("\n[*] Seeding CanaryGrid Deception Assets into 'decoys/staged_assets'...\n")
    # 1. Plant Decoy AWS Credentials
    aws_path = os.path.join(target_dir, "aws_credentials_decoy")
    with open(aws_path, "w", encoding="utf-8") as f:
        f.write(DECOY_AWS_TEMPLATE)
    print(f" [+] Decoy AWS credentials staged at : {aws_path}")
    # 2. Plant Decoy Confidential Document
    doc_path = os.path.join(target_dir, "Executive_Compensation_Q4_Confidential.html")
    beacon_url = "http://localhost:8080/beacon/payroll_board_doc_01"
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(DECOY_HTML_TEMPLATE.format(beacon_url=beacon_url))
    print(f" [+] Decoy Document seeded           : {doc_path}")
    # 3. Plant Decoy Database Secrets
    env_path = os.path.join(target_dir, "database_staging_secrets.env")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(DECOY_ENV_TEMPLATE)
    print(f" [+] Decoy Database secrets seeded   : {env_path}")
    print("\n[SUCCESS] All deception assets successfully planted!")
if __name__ == "__main__":
    plant_all_decoys()