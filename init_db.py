import sqlite3

conn = sqlite3.connect("database/mandi.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS mandi_prices (
        commodity TEXT,
        modal_price INTEGER,
        date TEXT
    )
""")
conn.commit()
conn.close()

print("✅ mandi.db created with mandi_prices table.")

