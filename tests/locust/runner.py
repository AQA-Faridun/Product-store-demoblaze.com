import os
import re
import subprocess
import requests

# ==== QASE CONFIGURATION ====
QASE_API_TOKEN = os.getenv("QASE_PYTEST_API_TOKEN")
QASE_PROJECT_CODE = "PS"
QASE_RUN_ID = 17

# ==== SCENARIOS TO RUN ====
SCENARIOS = [
    {"file": "sign_up.py", "case_id": 198},
    {"file": "log_in.py", "case_id": 199},
    {"file": "main_page.py", "case_id": 200},
    {"file": "product_card.py", "case_id": 201},
    {"file": "cart.py", "case_id": 202}
]

SUMMARY_FILES = [
    f"{os.getcwd()}/summaries/sign_up_summary.txt",
    f"{os.getcwd()}/summaries/log_in_summary.txt",
    f"{os.getcwd()}/summaries/main_page_summary.txt",
    f"{os.getcwd()}/summaries/product_card_summary.txt",
    f"{os.getcwd()}/summaries/cart_summary.txt"
    ]

# ==== LOCUST OPTIONS ====
USERS = ["30", "150", "500"]
SPAWN_RATE = ["5", "10", "30"]
RUN_TIME = ["2m", "5m", "10m"]
LOCUST_ARGS = []

for i in range(1):
    LOCUST_ARGS.append(["--headless", "-u", USERS[i], "-r", SPAWN_RATE[i], "--run-time", RUN_TIME[i], "--host", "https://api.demoblaze.com"])

# ==== MAIN RUNNER ====
def run_scenario(file, case_id, summary_file):
    print(f"\nRunning scenario: {file} (Qase case ID: {case_id})")

    cmd = []
    for j in range(1):
        cmd.append(["locust", "-f", file, "--exit-code-on-error", "0"] + LOCUST_ARGS[j])

    if os.path.exists(summary_file):
        os.remove(summary_file)

    status, comment = "", ""
    for k in range(1):
        result = subprocess.run(cmd[k], capture_output=True, text=True, cwd=os.getcwd())
        print(result.stdout)

        if not os.path.exists(summary_file):
            print("❌ Summary file not found. Test may not have executed correctly.")
            comment += (result.stdout[-1000:] or "(No output)") + "\n"
            status = "invalid"
        else:
            with open(summary_file, "r") as f:
                comment += f.read() + "\n"

            failures = re.search(r"Failures: \d+$", comment)
            failures_count: int = int(re.search(r"\d+", failures.group(0))[0]) if failures is not None else 0

            if (k == 0 and failures_count <= 3) or (k == 1 and failures_count <= 20) or (k == 2 and failures_count <= 150):
                status = "passed"
            elif (k == 0 and failures_count > 3) or (k == 1 and failures_count > 20) or (k == 2 and failures_count > 150):
                print("failures_count -", failures_count)
                status = "failed"
                comment += "\n" + result.stdout[-1000:]

    send_to_qase(case_id, status, comment)
    print("✅ Done!")


def send_to_qase(case_id, status, comment):
    headers = {
        "Token": QASE_API_TOKEN,
        "Content-Type": "application/json"
    }

    data = {
        "case_id": case_id,
        "status": status,
        "comment": comment
    }

    url = f"https://api.qase.io/v1/result/{QASE_PROJECT_CODE}/{QASE_RUN_ID}"
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("🟢 Результат отправлен в Qase")
    else:
        print("🔴 Код ответа от Qase:", res.status_code)
        print("🔴 Ошибка отправки в Qase:", res.text)


if __name__ == "__main__":
    for scenario in SCENARIOS:
        run_scenario(scenario["file"], scenario["case_id"], SUMMARY_FILES[SCENARIOS.index(scenario)])
