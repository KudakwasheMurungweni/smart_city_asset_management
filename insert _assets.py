import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Insert assets
assets = [
    ("Main Street Bridge", "Infrastructure", "Main Street", "Good", "2015-06-15", 1500000.00, "Active"),
    ("Excavator 3000", "Equipment", "Warehouse A", "Fair", "2019-04-10", 200000.00, "In Use"),
    ("Downtown Streetlights", "Utility", "Downtown", "Poor", "2010-08-25", 50000.00, "Under Maintenance"),
]

cursor.executemany("""
    INSERT INTO assets_asset (name, category, location, condition, purchase_date, cost, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", assets)

# Commit and close connection
conn.commit()
conn.close()

print("Assets added successfully!")
