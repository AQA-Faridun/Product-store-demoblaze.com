import os
import random
import string
from locust import HttpUser, task, between, events
import csv


class SignUp(HttpUser):
    wait_time = between(1, 3)

    @task
    def success_sign_up(self):
        username = f"test_user_{''.join(random.choices(string.ascii_letters + string.digits, k=4))}_{random.randint(2500, 5500)}"
        password = f"password{random.randint(2500, 5500)}"
        self.save_to_csv(username, password)

        response = self.client.post("/signup", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            self.save_to_csv(username, password)


    def save_to_csv(self, username, password):
        file_path = f"{os.getcwd()}/data/registered_users.csv"
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password"], delimiter=",")
            if not file_exists:
                writer.writeheader()
            writer.writerow({"username": username, "password": password})

@events.quitting.add_listener
def save_summary(environment, **kwargs):
    total = environment.stats.total
    with open(f"{os.getcwd()}/summaries/sign_up_summary.txt", "a") as f:
        f.write(
            f"Total Requests: {total.num_requests}\n"
            f"Failures: {total.num_failures}\n"
            f"RPS: {total.total_rps:.2f}\n"
            f"Min Response Time: {total.min_response_time:.2f} ms\n"
            f"Avg Response Time: {total.avg_response_time:.2f} ms\n"
            f"Max Response Time: {total.max_response_time:.2f} ms\n\n"
        )
