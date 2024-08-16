from firebase_admin import credentials, firestore, storage, auth
import firebase_admin
import os
from dotenv import load_dotenv

load_dotenv()


firebase_credentials_path = os.getenv("CERIFICATE_PATH")
firebase_storage_bucket = os.getenv("APP_NAME")
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred, {'storageBucket': firebase_storage_bucket})


db = firestore.client()
bucket = storage.bucket()

db = firestore.client()
user_ref = db.collection('user')

def get_doc_id_by_email(email):
    query = user_ref.where("email", "==", email)
    docs = query.get()
    doc_id = [doc.id for doc in docs]
    print(f"user_id: {doc_id}")
    if not doc_id:
        return 
    else:
        return doc_id

def delete_user_data(doc_id):

    try:
        user_ref.document(doc_id).delete()
        auth.delete_user(doc_id)
        
        blob_folder = f"image/{doc_id}/"
        blobs = bucket.list_blobs(prefix=blob_folder)
        for blob in blobs:
            blob.delete()
    except Exception as e:
        print(f"Error occured: {e}")
