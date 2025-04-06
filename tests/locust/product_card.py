import os
import random

from locust import HttpUser, between, task, events


class ProductCard(HttpUser):
    wait_time = between(1, 3)

    @task
    def success_open_product_card(self):
        response = self.client.post("/view", json={
            "id": random.randint(1, 9).__str__()
        })

        if response.status_code not in (200, 201):
            print("🔴 Отказ в доступе", response.status_code)
            print(f"🔴 Содержимое и url response: request url - {response.request.url} and request body - {response.request.body}")

@events.quitting.add_listener
def save_summary(environment, **kwargs):
    total = environment.stats.total
    with open(f"{os.getcwd()}/summaries/product_card_summary.txt", "a") as f:
        f.write(
            f"Total Requests: {total.num_requests}\n"
            f"Failures: {total.num_failures}\n"
            f"RPS: {total.total_rps:.2f}\n"
            f"Min Response Time: {total.min_response_time:.2f} ms\n"
            f"Avg Response Time: {total.avg_response_time:.2f} ms\n"
            f"Max Response Time: {total.max_response_time:.2f} ms\n\n"
        )
