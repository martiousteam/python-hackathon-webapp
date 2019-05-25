from locust import HttpLocust, TaskSet, task
import logging
import uuid


class RegisterUserSteps(TaskSet):
    @task
    def register(self):
        self.locust.username = str(uuid.uuid4())
        self.locust.email = self.locust.username + "@gmail.com"

        form_data = {'email': self.locust.email,
                     'username': self.locust.username,
                     'password': 'test',
                     'name': self.locust.username}

        self.client.post("/authorization/signup/", form_data)
        # logging.info('Login with %s username and %s password', self.username, self.password)


class RegisterUserTest(HttpLocust):
    task_set = RegisterUserSteps
    host = "http://127.0.0.1:5000"
    sock = None

    def __init__(self):
        super(RegisterUserTest, self).__init__()


# locust -f load_test.py --no-reset-stats
