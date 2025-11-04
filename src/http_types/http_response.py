from typing import Dict

class HttpResponse:

    def __init__(self, body: Dict[str, str]={}, status_code: int=404) -> None:

        self.body = body
        self.status_code = status_code