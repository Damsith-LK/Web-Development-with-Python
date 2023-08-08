import requests

class Post:
    def __init__(self):
        response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
        self.blogs = response.json()

    def get_blogs(self):
        return self.blogs