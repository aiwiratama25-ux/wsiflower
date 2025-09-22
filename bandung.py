import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# === Koneksi ke database MySQL ===
conn = mysql.connector.connect(
    host="localhost",       # ganti dengan IP/host DB
    user="userdb",          # ganti dengan user DB
    password="passworddb",  # ganti dengan password DB
    database="bandung"      # nama database
)

# === Query data dari DT_DIST ===
query = """
SELECT 
    timestamp,
    IN1_FLOW_AVG,
    IN1_PRESSURE_AVG,
    IN2_FLOW_AVG,
    IN2_PRESSURE_AVG
FROM DT_DIST
WHERE timestamp >= NOW() - INTERVAL 1 DAY
ORDER BY timestamp;
"""

df = pd.read_sql(query, conn)
conn.close()

# Pastikan kolom timestamp jadi datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# === Plot grafik ===
plt.figure(figsize=(12,6))

# Flow Intake 1 vs Flow Intake 2
plt.plot(df['timestamp'], df['IN1_FLOW_AVG'], label="Flow Intake 1")
plt.plot(df['timestamp'], df['IN2_FLOW_AVG'], label="Flow Intake 2")

# Pressure Intake 1 vs Intake 2 (opsional, beda sumbu)
plt.plot(df['timestamp'], df['IN1_PRESSURE_AVG'], label="Pressure Intake 1", linestyle="--")
plt.plot(df['timestamp'], df['IN2_PRESSURE_AVG'], label="Pressure Intake 2", linestyle="--")

plt.xlabel("Waktu")
plt.ylabel("Nilai")
plt.title("Trend Flow & Pressure dari DT_DIST (1 Hari Terakhir)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
