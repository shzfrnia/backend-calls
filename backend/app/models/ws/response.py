class WebSocketJsonResponse():
    def __init__(self, type: str, payload):
        self.type = type
        self.payload = payload

    def to_dict(self):
        return {"type": self.type, "payload": self.payload}
