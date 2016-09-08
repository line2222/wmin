import os
import requests

dict_list = [
    "/admin",
    "/login",
    "/manage",
    "/index",
    "/test",
    "/info",
    "/xadmin",
    "/web"
]


class test:
    def __init__(self, url):
        self.www = url

    def scan(self):
        url = self.www + dict_list.pop()
        print(str(os.getpid())+"-"+url+"--"+str(requests.get(url).
                                                status_code))

    def run(self):
        for i in dict_list:
            self.scan()
