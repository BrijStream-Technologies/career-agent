"""
Unit tests for IMAP Bounce Reconciliation Module.
Tests MIME DSN parsing, fallback email extraction, and ledger updates.
"""

import pytest
import json
from pathlib import Path
from career_agent.imap_bounce_reconciler import IMAPBounceReconciler

def test_parse_bounce_email_body():
    reconciler = IMAPBounceReconciler()

    # DSN Sample Payload
    sample_raw_dsn = b"""From: mailer-daemon@mail.me.com
To: sylvesterfcarter@icloud.com
Subject: Undeliverable: Executive Candidate Brief
Content-Type: multipart/report; report-type=delivery-status; boundary="BOUNDARY"

--BOUNDARY
Content-Type: text/plain

This is an automatically generated Delivery Status Notification.
Delivery to the following recipients failed permanently:
  * executive_bounced@targetcorp.com

--BOUNDARY
Content-Type: message/delivery-status

Reporting-MTA: dns; mail.me.com
Final-Recipient: rfc822; executive_bounced@targetcorp.com
Action: failed
Status: 5.1.1
Diagnostic-Code: smtp; 550 5.1.1 User unknown

--BOUNDARY--
"""

    failed_email, reason = reconciler.parse_bounce_email_body(sample_raw_dsn)
    assert failed_email == "executive_bounced@targetcorp.com"
    assert "550" in reason or "User" in reason


def test_parse_microsoft_exchange_ndr():
    reconciler = IMAPBounceReconciler()

    exchange_ndr = b"""From: Mail Delivery Subsystem <mailer-daemon@googlemail.com>
To: sylvesterfcarter@icloud.com
Subject: Message blocked

Your message to robert.kyncl@wmg.com has been blocked. See technical details below for more information.
The response from the remote server was:
550 5.4.1 Recipient address rejected: Access denied. For more information see https://aka.ms/EXOSmtpErrors

Final-Recipient: rfc822; robert.kyncl@wmg.com
Action: failed
Status: 5.4.1
Remote-MTA: dns; wmg-com.mail.protection.outlook.com
Diagnostic-Code: smtp; 550 5.4.1 Recipient address rejected: Access denied.
"""

    failed_email, reason = reconciler.parse_bounce_email_body(exchange_ndr)
    assert failed_email == "robert.kyncl@wmg.com"
    assert "5.4.1" in reason or "Rejected" in reason or "Microsoft Exchange" in reason

def test_scan_and_reconcile_bounces_mock(tmp_path, monkeypatch):
    # Create temp ledgers
    mock_sent_ledger = tmp_path / "sent_outreach_ledger.json"
    mock_sent_ledger.write_text(json.dumps({
        "job_1": {
            "job_id": "job_1",
            "company": "Target Corp",
            "recipient_email": "bounced_exec@company.com",
            "status": "DISPATCHED"
        },
        "job_2": {
            "job_id": "job_2",
            "company": "Valid Corp",
            "recipient_email": "valid_exec@company.com",
            "status": "DISPATCHED"
        }
    }))

    mock_track_a_ledger = tmp_path / "track_a_290_executive_dispatch_ledger.json"
    mock_track_a_ledger.write_text(json.dumps([
        {
            "executive_name": "Bounced Exec",
            "executive_email": "bounced_exec@company.com",
            "status": "DISPATCHED"
        }
    ]))

    reconciler = IMAPBounceReconciler(
        sent_ledger_path=mock_sent_ledger,
        track_a_ledger_path=mock_track_a_ledger
    )

    # Mock connect_imap to return None (no live network during unit test)
    monkeypatch.setattr(reconciler, "connect_imap", lambda: None)

    # Set up mock bounced email manually
    reconciler.bounced_records = [
        {"email": "bounced_exec@company.com", "reason": "550 User Unknown", "timestamp": "2026-10-03T09:00:00"}
    ]

    results = reconciler.scan_and_reconcile_bounces()
    
    assert results["sent_ledger_updates"] == 1
    assert results["track_a_ledger_updates"] == 1

    # Verify ledger file updates
    sent_data = json.loads(mock_sent_ledger.read_text())
    assert sent_data["job_1"]["status"] == "BOUNCED_UNDELIVERABLE"
    assert sent_data["job_2"]["status"] == "DISPATCHED"

    track_a_data = json.loads(mock_track_a_ledger.read_text())
    assert track_a_data[0]["status"] == "BOUNCED_UNDELIVERABLE"

    report = reconciler.generate_reconciliation_report(results)
    assert "Executive IMAP Bounce & Delivery Reconciliation Brief" in report
    assert "bounced_exec@company.com" in report
