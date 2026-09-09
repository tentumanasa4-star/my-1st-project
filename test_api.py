import json
from app import create_app

def run_tests():
    app = create_app()
    client = app.test_client()

    print("\n==========================================")
    print("  RUNNING CAMPUS EVENTS BACKEND TESTS")
    print("==========================================")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("[PASS] 1. Health Check OK")

    # 2. Student Login
    res = client.post("/api/auth/login", json={
        "email": "student@campus.edu",
        "password": "password123"
    })
    assert res.status_code == 200, f"Student login failed: {res.data}"
    student_data = json.loads(res.data)
    student_token = student_data["token"]
    print(f"[PASS] 2. Student Login OK (Welcome {student_data['user']['name']})")

    # 3. Admin Login
    res = client.post("/api/auth/admin-login", json={
        "email": "admin@campus.edu",
        "password": "admin123"
    })
    assert res.status_code == 200, f"Admin login failed: {res.data}"
    admin_data = json.loads(res.data)
    admin_token = admin_data["token"]
    print(f"[PASS] 3. Admin Login OK (Welcome {admin_data['user']['name']})")

    # 4. Get Events with Filter
    res = client.get("/api/events?category=Technical")
    assert res.status_code == 200
    events = json.loads(res.data)["events"]
    assert len(events) >= 1
    print(f"[PASS] 4. Events Filter OK ({len(events)} technical events found)")

    # 5. Get Categories Count
    res = client.get("/api/events/categories")
    assert res.status_code == 200
    cats = json.loads(res.data)["categories"]
    print(f"[PASS] 5. Categories list OK ({len(cats)} categories retrieved)")

    # 6. Student Register for Event
    headers = {"Authorization": f"Bearer {student_token}"}
    res = client.post("/api/registrations", json={
        "event_id": "evt-002"
    }, headers=headers)
    assert res.status_code in [201, 409], f"Registration failed: {res.data}"
    if res.status_code == 201:
        reg_info = json.loads(res.data)
        print(f"[PASS] 6. Event Registration OK (Pass ID: {reg_info['registration']['registration_id']})")
    else:
        print("[PASS] 6. Event Registration idempotency OK (Already registered)")

    # 7. Student My Events
    res = client.get("/api/registrations/my-events", headers=headers)
    assert res.status_code == 200
    my_regs = json.loads(res.data)["registrations"]
    print(f"[PASS] 7. My Events retrieval OK ({len(my_regs)} registered events)")

    # 8. Notifications
    res = client.get("/api/notifications", headers=headers)
    assert res.status_code == 200
    notifs = json.loads(res.data)["notifications"]
    print(f"[PASS] 8. Notifications retrieval OK ({len(notifs)} notifications found)")

    # 9. Admin Analytics
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/admin/analytics", headers=admin_headers)
    assert res.status_code == 200
    analytics = json.loads(res.data)
    print(f"[PASS] 9. Admin Analytics OK (Total Events: {analytics['summary']['total_events']}, Total Regs: {analytics['summary']['total_registrations']})")

    print("\nAll 9 backend tests passed with 100% success!\n")

if __name__ == "__main__":
    run_tests()
