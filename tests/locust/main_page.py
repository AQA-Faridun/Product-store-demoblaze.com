import os

from locust import HttpUser, between, task, events


class MainPage(HttpUser):
    wait_time = between(1, 3)

    @task
    def success_open_main_page(self):
        response = self.client.get("/entries")

        if response.status_code not in (200, 201):
            print("🔴 Отказ в доступе", response.status_code)

@events.quitting.add_listener
def save_summary(environment, **kwargs):
    total = environment.stats.total
    with open(f"{os.getcwd()}/summaries/main_page_summary.txt", "a") as f:
        f.write(
            f"Total Requests: {total.num_requests}\n"
            f"Failures: {total.num_failures}\n"
            f"RPS: {total.total_rps:.2f}\n"
            f"Min Response Time: {total.min_response_time:.2f} ms\n"
            f"Avg Response Time: {total.avg_response_time:.2f} ms\n"
            f"Max Response Time: {total.max_response_time:.2f} ms\n\n"
        )
