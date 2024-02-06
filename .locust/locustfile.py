from locust import HttpUser, constant_throughput, task


class TestUser(HttpUser):
    wait_time = constant_throughput(0.1)

    @task
    def courses(self):
        self.client.get("/api/v1/courses?symbols=btc&currency=usd")
