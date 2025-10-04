import requests
import xml.etree.ElementTree as ET
import sqlite3

# Fetch XML
url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
params = {
    "api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
    "format": "xml"
}
headers = {"accept": "application/xml"}
response = requests.get(url, params=params, headers=headers)

# Parse XML
root = ET.fromstring(response.text)

# Connect to SQLite
conn = sqlite3.connect("database/mandi.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mandi_data (
        commodity TEXT,
        state TEXT,
        district TEXT,
        market TEXT,
        arrival_date TEXT,
        min_price INTEGER,
        max_price INTEGER,
        modal_price INTEGER
    )
""")

# Extract and insert data
for record in root.findall(".//record"):
    cursor.execute("""
        INSERT INTO mandi_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.findtext("commodity"),
        record.findtext("state"),
        record.findtext("district"),
        record.findtext("market"),
        record.findtext("arrival_date"),
        int(record.findtext("min_price") or 0),
        int(record.findtext("max_price") or 0),
        int(record.findtext("modal_price") or 0)
    ))

conn.commit()
conn.close()
