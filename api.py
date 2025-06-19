import requests as req

class API:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'}

    def get(self, endpoint, params={}):
        with req.get(self.base_url+endpoint, headers=self.headers, params=params) as response:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

    def post(self, endpoint, data={}):
        with req.post(self.base_url+endpoint, headers=self.headers, json=data) as response:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()
                
    def put(self, endpoint, data={}):
        with req.put(self.base_url+endpoint, headers=self.headers, json=data) as response:
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()
