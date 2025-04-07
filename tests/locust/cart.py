import os
import random

from locust import HttpUser, between, task, events


class Cart(HttpUser):
    wait_time = between(1, 3)

    @task
    def success_add_to_cart(self):
        product = random.randint(1, 9)
        response = self.client.post("/addtocart", json={"flag": False, "cookie": "user=97d2a6ac-48fe-c487-2094-ad3a9ada0c56", "prod_id": product})

        if response.status_code == 200:
            cart_response = self.client.post("/viewcart", json={"flag": False, "cookie": "user=97d2a6ac-48fe-c487-2094-ad3a9ada0c56"})

            if cart_response.status_code != 200:
                print("🔴 Товар не был добавлен в корзину")


@events.quitting.add_listener
def save_summary(environment, **kwargs):
    total = environment.stats.total
    with open(f"{os.getcwd()}/summaries/cart_summary.txt", "a") as f:
        f.write(
            f"Total Requests: {total.num_requests}\n"
            f"Failures: {total.num_failures}\n"
            f"RPS: {total.total_rps:.2f}\n"
            f"Min Response Time: {total.min_response_time:.2f} ms\n"
            f"Avg Response Time: {total.avg_response_time:.2f} ms\n"
            f"Max Response Time: {total.max_response_time:.2f} ms\n\n"
        )
