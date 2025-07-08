from google.cloud import firestore
from google.oauth2 import service_account

# Path to your downloaded JSON key file
SERVICE_ACCOUNT_FILE = "key.json"
DB_NAME = "mydb"

# Load credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)

# Initialize Firestore client
db = firestore.Client(credentials=credentials, project=credentials.project_id, database=DB_NAME)

def submit_feedback(name, email, feedback):
    doc_ref = db.collection("feedback").document(email)
    doc_ref.set({
        "name": name,
        "email": email,
        "feedback": feedback
    })
    print(f"✅ Submitted to database: {DB_NAME}")

# Example use
submit_feedback("Alice", "alice@example.com", "Loving this course!")