"""
Unit tests for DualTrackBatchRunner (Track A 700/day Email Outreach & Track B Direct Site Playwright Automation).
"""

import pytest
from career_agent.dual_track_runner import DualTrackBatchRunner

def test_dual_track_runner_instantiation():
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    assert runner.daily_email_limit == 700
    assert runner.profile.name == "Sylvester Floyd Carter IV"

def test_track_a_batch_dispatch_mock():
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    res = runner.execute_track_a_smtp_dispatch(limit=5, live_send=False)
    assert res["track"] == "Track A (C-Suite Email Outreach)"
    assert res["limit"] == 5
    assert "dispatched" in res

def test_track_b_direct_site_mock():
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    res = runner.execute_track_b_direct_site_applications(limit=2, submit_live=False)
    assert res["track"] == "Track B (Direct Company Site Applications)"
    assert res["limit"] == 2
    assert "processed" in res
