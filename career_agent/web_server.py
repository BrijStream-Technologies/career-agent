"""
Web Server module for Sylvester's Autonomous Career Agent.
Provides a lightweight HTTP web server delivering the mobile iPhone UI dashboard and REST API.
Uses zero external dependencies (Python standard library http.server).
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket
import sys
from pathlib import Path
from career_agent.agent_orchestrator import CareerAgentOrchestrator

PORT = 8080

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class CareerAgentHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silent or concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def do_GET(self):
        if self.path == "/api/digest":
            self.send_json_response(self.get_digest_data())
        elif self.path in ["/", "/dashboard", "/index.html"]:
            self.send_html_dashboard()
        else:
            self.send_error(404, "Endpoint not found")

    def send_json_response(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html_dashboard(self):
        html_path = Path(__file__).parent / "mobile_dashboard.html"
        if html_path.exists():
            content = html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(500, "Dashboard HTML file missing")

    def get_digest_data(self) -> dict:
        sample_listings = [
            {
                "id": "job_001",
                "title": "Principal AI Product Manager",
                "company": "ElevenLabs",
                "location": "Remote - US",
                "is_remote": True,
                "base_salary_min": 240000,
                "base_salary_max": 290000,
                "estimated_tc": 360000,
                "description": "Lead AI voice orchestration, P&L management, AI prompt architecture, audio licensing, and rights registry.",
                "source_url": "https://elevenlabs.io/careers/principal-ai-pm"
            },
            {
                "id": "job_002",
                "title": "Forward Deployed AI Solutions Lead",
                "company": "Anthropic",
                "location": "Remote - US / Global",
                "is_remote": True,
                "base_salary_min": 250000,
                "base_salary_max": 320000,
                "estimated_tc": 480000,
                "description": "Forward deployed AI lead working with customers to build AI agents, system architecture, prompt engineering, Python, P&L strategy.",
                "source_url": "https://anthropic.com/careers/forward-deployed-lead"
            }
        ]
        
        orchestrator = CareerAgentOrchestrator()
        digest_md = orchestrator.run_daily_pipeline(sample_listings)

        return {
            "candidate": orchestrator.profile.name,
            "title": orchestrator.profile.title,
            "scanned_count": len(sample_listings),
            "digest_markdown": digest_md
        }

def start_server(port: int = PORT, run_forever: bool = True):
    local_ip = get_local_ip()
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, CareerAgentHTTPHandler)
    
    print("=" * 60)
    print(f"🚀 Career Agent Mobile Server is running!")
    print(f"📱 Access on your iPhone via local Wi-Fi: http://{local_ip}:{port}")
    print(f"💻 Access locally on Mac: http://localhost:{port}")
    print("=" * 60)
    
    if run_forever:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()
    return httpd

if __name__ == "__main__":
    port_arg = PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port_arg = int(sys.argv[1])
    start_server(port=port_arg, run_forever=True)
