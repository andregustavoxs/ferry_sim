from typing import Dict

class HttpRequest:

    def __init__(self, body: Dict[str, str]={}, params: Dict[str, str]={}) -> None:

        self.body = body
        self.params = params

