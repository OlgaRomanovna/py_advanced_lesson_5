from requests import Response

from app.client.session import BaseSession


class HttpClient:

    def __init__(self, base_url):
        self.session = BaseSession(base_url)
        # self.set_headers({
        #     'Accept': 'application/json',
        #     'Content-Type': 'application/json'
        # })

    def set_headers(self, headers: dict):
        self.session.headers.update(headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def request(self, method: str, url: str = None, **kwargs) -> Response:
        return self.session.request(method, url, **kwargs)

    def get(self, url=None, **kwargs):
        return self.session.request("GET", url, **kwargs)

    def post(self, url=None, **kwargs):
        return self.session.request("POST", url, **kwargs)

    def put(self, url=None, **kwargs):
        return self.session.request("PUT", url, **kwargs)

    def patch(self, url=None, **kwargs):
        return self.session.request("PATCH", url, **kwargs)

    def delete(self, url=None, **kwargs):
        return self.session.request("DELETE", url, **kwargs)