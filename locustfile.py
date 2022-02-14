from locust import HttpUser, task

class LocustUser(HttpUser):
        
    @task
    def index_get(self):
        self.client.get("/index", data={"email":"john@simplylift.co"})

    @task
    def showSummary_get(self):
        self.client.get("/showSummary")
        
    @task
    def booking_get(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def booking_post(self):
        self.client.post("/book/Spring%20Festival/Simply%20Lift", data={'placesRequired':2})
    
    @task
    def points_get(self):
        self.client.post("/points")
