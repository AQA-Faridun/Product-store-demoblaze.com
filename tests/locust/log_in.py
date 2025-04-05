import csv
import os
from itertools import cycle

from locust import HttpUser, between, task, events

def load_users():
    with open(f"{os.getcwd()}/data/registered_users.csv") as f:
        reader = csv.DictReader(f)
        return list(reader)

users = cycle(load_users())

class LogIn(HttpUser):
    wait_time = between(1, 3)

    @task
    def success_log_in(self):
        user = next(users)

        response = self.client.post("/login", json={
            "username": user["username"],
            "password": user["password"],
        })

        if response.status_code != 200:
            print("🔴 Ошибка авторизации:", response.status_code)
            print("🔴 Ошибка авторизации:", response.text)

@events.quitting.add_listener
def save_summary(environment, **kwargs):
    total = environment.stats.total
    with open(f"{os.getcwd()}/summaries/log_in_summary.txt", "a") as f:
        f.write(
            f"Total Requests: {total.num_requests}\n"
            f"Failures: {total.num_failures}\n"
            f"RPS: {total.total_rps:.2f}\n"
            f"Min Response Time: {total.min_response_time:.2f} ms\n"
            f"Avg Response Time: {total.avg_response_time:.2f} ms\n"
            f"Max Response Time: {total.max_response_time:.2f} ms\n\n"
        )
