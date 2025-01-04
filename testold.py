from google.cloud import firestore

def test_firestore():
    try:
        # Initialize Firestore
        db = firestore.Client()

        # Add a test document
        doc_ref = db.collection('test_collection').add({
            "message": "Hello, Firestore!",
            "status": "success"
        })
        print(f"Document added with ID: {doc_ref[1].id}")

        # Fetch documents in the collection
        docs = db.collection('test_collection').stream()
        print("Documents in Firestore:")
        for doc in docs:
            print(f"{doc.id} => {doc.to_dict()}")

        print("Firestore integration is working!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_firestore()


# graceful-cider-438814-e0-firebase-adminsdk-8958u-a2289d9f51.json
# graceful-cider-438814-e0-d7d6b439e94b.json

# gitignore
# seismic-hexagon-440010-f7-be7f6e5c5716.json
# .env