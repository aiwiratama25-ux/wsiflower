import streamlit as st
import math

st.title("📊 Nila Farming Optimizer")
st.write("Hitung potensi hasil panen, kebutuhan pakan, biaya, dan profit berdasarkan parameter kolam.")

# === Input kolam ===
diameter = st.number_input("Diameter kolam (m)", 1.0, 10.0, 3.0, 0.1)
tinggi_air = st.number_input("Tinggi air (m)", 0.5, 2.0, 1.2, 0.1)
volume = math.pi * (diameter/2)**2 * tinggi_air
st.write(f"**Volume kolam** ≈ {volume:.2f} m³")

# === Input target ===
kg_m3 = st.selectbox("Target biomassa (kg/m³)", [10,20,30,40], index=1)
fish_price = st.number_input("Harga jual (Rp/kg)", 10000, 50000, 30000, 1000)
fingerling_price = st.number_input("Harga benih (Rp/ekor)", 100, 2000, 500, 50)
feed_price = st.number_input("Harga pakan (Rp/kg)", 5000, 20000, 12500, 500)

# === Input teknis ===
fcr = st.slider("FCR (Feed Conversion Ratio)", 1.0, 2.0, 1.4, 0.05)
sr = st.slider("SR (Survival Rate %)", 50, 100, 90, 1)
fish_size = st.selectbox("Ukuran panen (gram/ekor)", [200,250,300,400,500], index=2)

# === Hitung panen ===
harvest_kg = kg_m3 * volume
harvest_fish = harvest_kg*1000 / fish_size
stocking = harvest_fish / (sr/100)
feed_kg = harvest_kg * fcr

# === Biaya ===
fry_cost = stocking * fingerling_price
feed_cost = feed_kg * feed_price
operational = 400_000 if kg_m3<=20 else 600_000  # probiotik/kimia
misc = 0.1*(fry_cost+feed_cost+operational)
total_cost = fry_cost+feed_cost+operational+misc

# === Pendapatan & Laba ===
revenue = harvest_kg * fish_price
profit = revenue - total_cost

# === Output ===
st.subheader("📈 Hasil Perhitungan")
st.metric("Biomassa Panen (kg)", f"{harvest_kg:,.0f}")
st.metric("Jumlah Panen (ekor)", f"{harvest_fish:,.0f}")
st.metric("Benih Tebar (ekor)", f"{stocking:,.0f}")
st.metric("Kebutuhan Pakan (kg)", f"{feed_kg:,.0f}")

st.subheader("💰 Rincian Biaya")
st.write({
    "Biaya Benih (Rp)": int(fry_cost),
    "Biaya Pakan (Rp)": int(feed_cost),
    "Kimia/Probiotik (Rp)": operational,
    "Kontinjensi 10% (Rp)": int(misc),
    "Total Biaya (Rp)": int(total_cost)
})

st.subheader("💹 Profitabilitas")
st.metric("Pendapatan (Rp)", f"{int(revenue):,}")
st.metric("Laba (Rp)", f"{int(profit):,}")

# === Analisa singkat ===
st.subheader("📌 Analisa")
st.write(f"Dengan SR {sr}% dan FCR {fcr}, panen {harvest_kg:.0f} kg akan memberi laba sekitar Rp {profit:,.0f}.")
st.write("Anda bisa menurunkan FCR atau meningkatkan SR untuk menaikkan profit.")