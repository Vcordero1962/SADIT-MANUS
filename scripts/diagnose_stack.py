import socket
import requests
import sys
import os
import subprocess
import time


def check_port(host, port, service_name):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex((host, port))
            if result == 0:
                print(f"[OK] {service_name} Port {port} is OPEN.")
                return True
            else:
                print(
                    f"[ERR] {service_name} Port {port} is CLOSED or BLOCKED.")
                return False
    except Exception as e:
        print(f"[ERR] Failed checking {service_name}: {e}")
        return False


def check_docker_container(container_name):
    try:
        # Check if running
        out = subprocess.check_output(
            f"docker inspect -f '{{{{.State.Running}}}}' {container_name}", shell=True).decode().strip()
        if out == "'true'":
            print(f"[OK] Container '{container_name}' is RUNNING.")
            return True
        else:
            print(
                f"[ERR] Container '{container_name}' is NOT running (State: {out}).")
            return False
    except subprocess.CalledProcessError:
        print(f"[ERR] Container '{container_name}' NOT FOUND.")
        return False
    except Exception as e:
        print(f"[ERR] Docker Check Failed: {e}")
        return False


def check_backend_api():
    url = "http://localhost:8000"
    print(f" -> Testing Backend URL: {url} ...")
    try:
        r = requests.get(f"{url}/", timeout=2)
        if r.status_code == 200:
            print(f"[OK] Backend Root is reachable. Response: {r.json()}")
            return True
        else:
            print(f"[ERR] Backend returned status {r.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(
            "[CRITICAL] Backend Connection REFUSED. Service is down or not mapped to localhost.")
        return False


def check_frontend_dev_server():
    # Helper to check common vite ports
    ports_to_check = [3000, 5173, 5174]
    found = False
    for p in ports_to_check:
        if check_port("localhost", p, f"Frontend (Vite)"):
            print(f"[OK] Frontend found active on Port {p}")
            found = True
            # Try HTTP get
            try:
                r = requests.get(f"http://localhost:{p}", timeout=2)
                if r.status_code == 200:
                    print(f"[OK] Frontend HTTP Get 200 OK.")
                else:
                    print(
                        f"[WARN] Frontend Port Open but returned {r.status_code}.")
            except:
                print("[WARN] Port Open but HTTP Request failed.")
            return True

    if not found:
        print(
            "[CRITICAL] NO Frontend Server detected on standard ports (3000, 5173, 5174).")
    return False


def run_diagnostics():
    print("=== SADIT v1.2 FULL STACK DIAGNOSTIC ===")

    # 1. Docker Level
    print("\n1. INSPECTING INFRASTRUCTURE (Docker)")
    db_ok = check_docker_container("sadit_db_v1")
    core_ok = check_docker_container("sadit_core_v1")

    # 2. Network Level
    print("\n2. INSPECTING NETWORK PORTS")
    db_port = check_port("localhost", 5432, "PostgreSQL")
    api_port = check_port("localhost", 8000, "FastAPI Backend")

    # 3. Application Level
    print("\n3. INSPECTING APPLICATION CONNECTIVITY")
    api_audit = False
    if api_port:
        api_audit = check_backend_api()

    print("\n4. INSPECTING FRONTEND")
    fe_ok = check_frontend_dev_server()

    # Summary
    print("\n=== DIAGNOSTIC CONCLUSION ===")
    if not db_ok:
        print("-> FATAL: Database Container is DOWN.")
    if not core_ok:
        print("-> FATAL: Backend Container is DOWN.")
    if core_ok and not api_port:
        print("-> FATAL: Backend is running but Port 8000 is NOT exposed to Windows.")
    if api_port and not api_audit:
        print("-> ERROR: Backend Port Open but Application not responding (Crashloop?).")
    if not fe_ok:
        print("-> FATAL: Frontend Server is NOT RUNNING. 'npm run dev' is dead or blocked.")

    if db_ok and core_ok and api_audit and fe_ok:
        print("-> SYSTEM HEALTHY. If browser fails, check Firewall/CORS or Browser Config.")
    elif db_ok and core_ok and api_audit and not fe_ok:
        print("-> PARTIAL: Backend is Perfect. FRONTEND IS DEAD. Restart 'npm run dev'.")


if __name__ == "__main__":
    run_diagnostics()
