import webbrowser
import socket
from urllib.parse import urlparse, parse_qs
from authlib.integrations.requests_client import OAuth2Session
import requests
from google.oauth2 import service_account
from google.cloud import firestore
from datetime import datetime, timezone

# === CONFIG ===
CLIENT_ID = "<YOUR_CLIENT_ID>"
CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
REDIRECT_URI = "http://localhost:8080"
SCOPES = ["openid", "email", "profile"]
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

SERVICE_ACCOUNT_FILE = "key.json"
DB_NAME = "mydb"

# === Local OAuth handler ===
class OAuthHandler(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("localhost", 8080))
        self.listen(1)
        self.code = None

    def wait_for_code(self):
        conn, _ = self.accept()
        data = conn.recv(1024).decode()
        path = data.split(' ')[1]
        query = urlparse(path).query
        self.code = parse_qs(query).get("code", [None])[0]

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nYou may now close this window."
        conn.sendall(response.encode())
        conn.close()
        self.close()

# === Google login function ===
def login_google():
    client = OAuth2Session(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES,
        code_challenge_method="S256"
    )
    auth_url, _ = client.create_authorization_url(AUTH_URL, prompt="select_account")
    webbrowser.open(auth_url)
    print("🌐 Opening browser for Gmail login...")

    server = OAuthHandler()
    server.wait_for_code()

    if not server.code:
        print("❌ Login failed: no code received.")
        return None

    token = client.fetch_token(
        TOKEN_URL,
        code=server.code,
        client_secret=CLIENT_SECRET
    )

    id_token_value = token.get("id_token")
    if not id_token_value:
        print("❌ Failed to get ID token.")
        return None

    userinfo = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token_value}).json()
    return userinfo

# === Submit feedback to Firestore ===
def submit_feedback(name, email, feedback):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    db = firestore.Client(credentials=credentials, project=credentials.project_id, database=DB_NAME)

    doc_ref = db.collection("feedback").document(email)
    doc_ref.set({
        "name": name,
        "email": email,
        "feedback": feedback,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    })
    print(f"✅ Submitted feedback for {email} to database: {DB_NAME}")

# === Main flow ===
if __name__ == "__main__":
    user = login_google()
    if user:
        print(f"👤 Logged in as {user['name']} ({user['email']})")
        fb = input("🗣️ Enter your feedback: ").strip()
        if fb:
            submit_feedback(user["name"], user["email"], fb)
        else:
            print("⚠️ No feedback entered.")
    else:
        print("Login failed.")
