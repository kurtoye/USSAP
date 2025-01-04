from google.cloud import firestore
from google.oauth2 import service_account

# Set your service account credentials file path
CREDENTIALS_PATH = r'C:/Users/t4r1k/..work/Projects/....cloud/USSAP/seismic-hexagon-440010-f7-1cc50bd5a587.json'

def test_firestore():
    try:
        # Authenticate and initialize Firestore
        credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
        db = firestore.Client(credentials=credentials)
        
        # Test adding a document
        print("📥 Adding a test document to Firestore...")
        test_doc_ref = db.collection('test_collection').add({
            "message": "Hello, Firestore!",
            "status": "success"
        })
        print(f"✅ Document added with ID: {test_doc_ref[1].id}")
        
        # Test fetching documents
        print("\n📤 Fetching documents from 'test_collection'...")
        docs = db.collection('test_collection').stream()
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")
        
        print("\n✅ Firestore connection and operations are working correctly!")

    except Exception as e:
        print("❌ An error occurred while testing Firestore:")
        print(e)

if __name__ == "__main__":
    test_firestore()
