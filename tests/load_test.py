from locust import HttpLocust, TaskSet, task
import logging



class LoginWithUniqueUsersSteps(TaskSet):
    username = "NOT_FOUND"
    password = "NOT_FOUND"

    @task
    def login(self):
        self.client.post("/authorization/login/", {
            'username': 'himanshu', 'password': 'test'
        })
        # logging.info('Login with %s username and %s password', self.username, self.password)


class LoginWithUniqueUsersTest(HttpLocust):
    task_set = LoginWithUniqueUsersSteps
    host = "http://127.0.0.1:5000"
    sock = None

    def __init__(self):
        super(LoginWithUniqueUsersTest, self).__init__()


# locust -f load_test.py --no-reset-stats
