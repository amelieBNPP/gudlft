from locust import HttpUser, task

class LocustUser(HttpUser):
    @task
    def init_test(self):
        self.client.get("/")