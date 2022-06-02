from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def madlibs_2(self):
        self.client.get("/madlibs")