import requests

class DistributedDB:
    def __init__(self):
        self.db_urls = [
            "https://dsci551-marketsphere-db1-default-rtdb.firebaseio.com/",
            "https://dsci551-marketsphere-db2-default-rtdb.firebaseio.com/"
        ]

    def compute_hash(self, item):
        """Compute a hash to distribute data across databases for both string and integer keys."""
        return sum(ord(c) for c in item) % 2

    def get_db_url(self, pk, path):
        """Get the full URL for a resource"""
        index = self.compute_hash(pk)
        #print("compute hash", pk, index)
        return f"{self.db_urls[index]}{path}.json"
    #read data
    def get(self, pk, path):
        """General method to get data from Firebase"""
        url = self.get_db_url(pk, path)
        response = requests.get(url)
        return response.json()
    #create
    def put(self, pk, path, data):
        """General method to write data to Firebase"""
        url = self.get_db_url(pk, path)
        response = requests.put(url, json=data)
        return response.json()
    #update
    def patch(self, pk, path, data):
        """General method to update data in Firebase"""
        url = self.get_db_url(pk, path)
        response = requests.patch(url, json=data)
        return response.json()
    #delete
    def delete(self, pk, path):
        """General method to delete data from Firebase"""
        url = self.get_db_url(pk, path)
        response = requests.delete(url)
        return response.json()


    
