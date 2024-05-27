import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime

from google.cloud.firestore_v1 import FieldFilter

# Check if the Firebase app is already initialized
cred = credentials.Certificate("zysec-app.json")
firebase_admin.initialize_app(cred)

class FirestoreHandler:
    def __init__(self):
        self.db = firestore.client()

    def fetch_data(self, collection_name, date_filter=None):
        query = self.db.collection(collection_name)
        if date_filter:
            query = query.where(filter=FieldFilter('dateUpdated', '>=', date_filter))
        docs = query.stream()
        return [self._doc_to_dict(doc) for doc in docs][::-1]

    def add_data(self, collection_name, data):
        self.db.collection(collection_name).add(data)

    def update_data(self, collection_name, doc_id, data):
        self.db.collection(collection_name).document(doc_id).update(data)

    def delete_data(self, collection_name, doc_id):
        self.db.collection(collection_name).document(doc_id).delete()

    @staticmethod
    def _doc_to_dict(doc):
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id  # Add the document ID for reference
        return doc_dict
