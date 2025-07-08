from cloudevents.http import CloudEvent
import functions_framework
from google.cloud import firestore
from google.events.cloud.firestore_v1 import DocumentEventData
from datetime import datetime, timezone

# Constants
HOURLY_RATE = 100.0
DB_NAME = "mydb"

@functions_framework.cloud_event
def enrich_timesheet(event: CloudEvent):
    # Parse Firestore event data
    data = DocumentEventData()
    data._pb.ParseFromString(event.data)
    doc = data.value
    fields = doc.fields
    document_path = doc.name.split("documents/")[-1]  

    print(f"📥 Triggered by document: {document_path}")

    # Extract required fields
    try:
        hours = float(fields["hours"].double_value)
        email = fields["user"].string_value
    except Exception as e:
        print("❌ Failed to parse document fields:", e)
        return

    enriched_data = {
        "status": "approved",
        "pay": hours * HOURLY_RATE,
        "processed_at": datetime.now(timezone.utc).isoformat()
    }

    db = firestore.Client(database=DB_NAME)
    doc_ref = db.document(document_path)
    doc_ref.update({"enriched": enriched_data})

    print(f"✅ Enriched document with: {enriched_data}")
