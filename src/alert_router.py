"""
Project CanaryGrid - Central Alert Router & Beacon Listener
Description: A lightweight HTTP server that catches tripwire signals from
             decoy documents, AWS honey-keys, and canary tokens.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os
import sys
from urllib.parse import urlparse
# Ensure Python can see our other files in the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ip_enrichment import IPEnrichment
from notifier import CanaryNotifier
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AlertRouter")
# A 1x1 invisible transparent image (GIF format in raw computer bytes)
TRANSPARENT_PIXEL = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04"
    b"\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
)
notifier = CanaryNotifier()
class CanaryRequestHandler(BaseHTTPRequestHandler):
    """Handles incoming tripwires and webhooks."""
    def _get_client_ip(self) -> str:
        """Extracts the true IP address of the caller."""
        forwarded_for = self.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return self.client_address[0]
    def _send_json_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
    # When someone opens a document or visits a URL (GET request)
    def do_GET(self):
        parsed_url = urlparse(self.path)
        client_ip = self._get_client_ip()
        user_agent = self.headers.get("User-Agent", "Unknown-Agent")
        # 1. Health check (to verify our server is alive)
        if parsed_url.path == "/health":
            self._send_json_response(200, {"status": "ONLINE", "system": "CanaryGrid"})
            return
        # 2. Tripwire Beacon! (When someone opens a decoy document)
        if parsed_url.path.startswith("/beacon/"):
            token_id = parsed_url.path.replace("/beacon/", "")
            logger.warning(f"[!] TRIPWIRE TRIGGERED: Token [{token_id}] accessed from {client_ip}")
            # Send the IP to our Detective
            ip_info = IPEnrichment.lookup(client_ip)
            # Send the data to our Notifier to sound the alarm!
            notifier.dispatch(
                trap_type="Decoy Document Web Beacon Triggered",
                asset_name=f"Document Token [{token_id}]",
                attacker_ip=client_ip,
                user_agent=user_agent,
                ip_details=ip_info,
                description=f"Decoy document was opened. Web beacon callback received for ID '{token_id}'.",
                recommended_action="Inspect the compromised workstation. Check running processes for Word/Chrome.",
            )
            # Return the invisible 1x1 image so the intruder's screen doesn't show any error
            self.send_response(200)
            self.send_header("Content-Type", "image/gif")
            self.send_header("Content-Length", str(len(TRANSPARENT_PIXEL)))
            self.end_headers()
            self.wfile.write(TRANSPARENT_PIXEL)
            return
        self._send_json_response(404, {"error": "Endpoint not found"})
    # When an external service sends us an alert webhook (POST request)
    def do_POST(self):
        parsed_url = urlparse(self.path)
        client_ip = self._get_client_ip()
        user_agent = self.headers.get("User-Agent", "Unknown-Agent")
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}
        # If an AWS Honey-Key was abused
        if parsed_url.path == "/webhook/aws":
            asset_name = payload.get("access_key_id", "Decoy-AWS-Key")
            event_name = payload.get("event_name", "sts:GetCallerIdentity")
            target_ip = payload.get("source_ip", client_ip)
            ip_info = IPEnrichment.lookup(target_ip)
            notifier.dispatch(
                trap_type="AWS Honey-Key Reconnaissance Detected",
                asset_name=f"IAM Decoy Key: {asset_name}",
                attacker_ip=target_ip,
                user_agent=user_agent,
                ip_details=ip_info,
                description=f"Unauthorized cloud API probe '{event_name}' executed using decoy IAM credential.",
                recommended_action="Revoke active AWS sessions for key and check CloudTrail for lateral movement.",
            )
            self._send_json_response(200, {"status": "aws_alert_processed"})
            return
        self._send_json_response(404, {"error": "Invalid route"})
    def log_message(self, format, *args):
        # Keeps our terminal output clean and silent unless an alarm rings
        return
def start_server(port: int = 8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, CanaryRequestHandler)
    print("\n" + "=" * 70)
    print(f" [ONLINE] CanaryGrid Alert Router Active")
    print(f" [*] Listening on : http://localhost:{port}")
    print(f" [*] Health Check : http://localhost:{port}/health")
    print(f" [*] Tripwire URL : http://localhost:{port}/beacon/<token_id>")
    print("=" * 70)
    print(" [*] Server is waiting for intruders... (Press Ctrl+C to stop)\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down CanaryGrid Alert Router.")
        httpd.server_close()
if __name__ == "__main__":
    start_server(8080)