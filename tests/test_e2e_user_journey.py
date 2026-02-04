import os
import time
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")


def wait_until_up(timeout_sec: int = 10) -> None:
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            r = requests.get(f"{BASE_URL}/", timeout=1)
            if r.status_code == 200:
                return
        except requests.RequestException:
            pass
        time.sleep(0.5)
    raise RuntimeError("Server not ready")


def test_user_journey_create_list_delete():
    wait_until_up()

    # Create
    create_resp = requests.post(
        f"{BASE_URL}/api/notes",
        json={"title": "E2E Title", "body": "E2E Body"},
        timeout=5,
    )
    assert create_resp.status_code == 201, create_resp.text
    created = create_resp.json()
    note_id = created["id"]

    # List and verify
    list_resp = requests.get(f"{BASE_URL}/api/notes", timeout=5)
    assert list_resp.status_code == 200, list_resp.text
    notes = list_resp.json()
    assert any(n.get("id") == note_id for n in notes)

    # Delete
    del_resp = requests.delete(f"{BASE_URL}/api/notes/{note_id}", timeout=5)
    assert del_resp.status_code == 204, del_resp.text

    # Verify deleted
    list_resp2 = requests.get(f"{BASE_URL}/api/notes", timeout=5)
    assert list_resp2.status_code == 200, list_resp2.text
    notes2 = list_resp2.json()
    assert all(n.get("id") != note_id for n in notes2)

