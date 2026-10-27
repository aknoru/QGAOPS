from software.dashboard.app import dashboard_payload


def test_dashboard_payload_is_explicitly_software_only():
    payload = dashboard_payload()
    assert payload["software_only"] is True
    assert "not integrated" in payload["hardware_status"]
