from locust import HttpUser, task, between
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (20000, 21000))


class LocustUser(HttpUser):
    wait_time = between(0.5, 3.0)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def index_get(self):
        self.client.get("/index")

    @task
    def showSummary_get(self):
        self.client.post("/showSummary", data=dict(email='john@simplylift.co'))

    @task
    def booking_get(self):
        self.client.get("/book/Fall%20Classic/Simply%20Lift")

    @task
    def booking_post(self):
        self.client.post(
            "/book/Spring%20Festival/Simply%20Lift",
            data={'placesRequired': 2},
        )

    @task
    def points_get(self):
        self.client.post("/clubSummary")
