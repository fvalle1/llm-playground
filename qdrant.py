from api import API
import uuid


class QDrant(API):
    def __init__(self, base_url="http://localhost:6333/", size=3):
        super().__init__(base_url)
        self.collection = "llama"
        if self.collection not in [collection["name"] for collection in self.list_collections()["collections"]]:
            self.create_collection(size=size)

    @property
    def collection_url(self):
        return "collections/"+self.collection+"/"

    def create_collection(self, size: int, distance="Cosine"):
        data = {
            "vectors": {
                "size": size,
                "distance": distance
            }
        }
        return self.put(self.collection_url, data=data)

    def list_collections(self):
        return self.get("collections")["result"]

    def describe_collection(self):
        return self.get(self.collection_url)["result"]

    def put_point(self, vector, **kwargs):
        data = {
            "points":
                [
                    {
                        "id": uuid.uuid4().hex,
                        "payload": {
                            **kwargs
                        },
                        "vector": vector
                    }
                ]
        }
        return self.put(self.collection_url+"points/", data=data)

    def get_point(self, point):
        return self.get(self.collection_url+"points/"+point)["result"]

    def describe_points(self, points):
        def describe(point):
            desc = self.get_point(point["id"])
            return {
                # "id": desc["id"],
                "score": point["score"] if "score" in point else -1,
                **desc["payload"]
            }
        return list(map(describe, points))

    def query(self, query_data: dict = None, prefetch: dict = None, filters: list = None, limit: int = 1):
        data = {
            "limit": limit,
            "with_payload": True
        }
        if prefetch is not None:
            data["prefetch"] = prefetch
        if filters is not None:
            data["filters"] = filters
        if query_data is not None:
            data["query"] = query_data
        return self.post(self.collection_url+"points/query", data=data)["result"]["points"]

    def query_random(self):
        return self.query({
            "sample": "random"
        })

    def query_positive_negative(self, positive_vector=[], negative_vector=[]):
        return self.query(
            {
                "recommend": {
                    "positive": positive_vector,
                    "negative": negative_vector
                }
            }
        )

    def query_filter(self, filters: list = []):
        return self.query(
            filters={
                "must": filters
            }
        )

    def generate_context(self, points, key="text"):
        return ";".join([point[key]+f" [{point['title']}]" for point in self.describe_points(points)])
