import json

class RestAPI(object):
    def __init__(self, database=None):
        self.database = database
        self.user_payload = {
            "name": "",
            "owes": {},
            "owed_by": {},
            "balance": 0.0
        }

    def get(self, url, payload=None):
        if url == "/users":
            if payload:
                if type(json.loads(payload)) == type({}):
                    self.user_payload.update({"name": json.loads(payload)['users'][0]})
                    return json.dumps({
                        "users": [self.user_payload]
                    })
            return json.dumps({"users": self.database['users']})

    def post(self, url, payload=None):
        if url == "/add":
            self.user_payload.update({"name": json.loads(payload)['user']})
            return json.dumps(self.user_payload)

        if url == "/iou":
            payload = json.loads(payload)
            for i in self.database['users']:
                if i["name"] == payload["lender"]:
                    i.update({
                        "name": payload["lender"],
                        "owed_by": {
                            payload["borrower"]: payload["amount"]
                            },
                        "balance": i["balance"] + payload["amount"]
                    })
                if i["name"] == payload["borrower"]:
                    i.update({
                        "name": payload["borrower"],
                        "owes": {
                            payload["lender"]: payload["amount"]
                        },
                        "balance": i["balance"] - payload["amount"]
                    })
            return json.dumps(self.database)
