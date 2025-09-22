import numpy as np
import matplotlib.pyplot as plt

# === Simulasi sensitivitas FCR & SR ===
st.subheader("📊 Simulasi Biaya Pakan vs Profit")

fcr_values = np.linspace(1.1, 1.8, 8)  # variasi FCR
sr_values = [80, 85, 90, 95]

results = []
for sr_val in sr_values:
    for fcr_val in fcr_values:
        harvest_kg_sim = kg_m3 * volume
        harvest_fish_sim = harvest_kg_sim*1000 / fish_size
        stocking_sim = harvest_fish_sim / (sr_val/100)
        feed_kg_sim = harvest_kg_sim * fcr_val
        fry_cost_sim = stocking_sim * fingerling_price
        feed_cost_sim = feed_kg_sim * feed_price
        total_cost_sim = fry_cost_sim + feed_cost_sim + operational + misc
        revenue_sim = harvest_kg_sim * fish_price
        profit_sim = revenue_sim - total_cost_sim
        results.append((sr_val, fcr_val, profit_sim))

# Tampilkan tabel ringkas
import pandas as pd
df_sim = pd.DataFrame(results, columns=["SR (%)","FCR","Profit (Rp)"])
st.dataframe(df_sim.pivot(index="FCR", columns="SR (%)", values="Profit (Rp)"))

# === Visualisasi kebutuhan pakan mingguan ===
st.subheader("📈 Kurva Kebutuhan Pakan Mingguan")

weeks = 16  # asumsi 16 minggu pemeliharaan
# Asumsi pertumbuhan linear
weekly_growth = harvest_kg / weeks
weekly_feed = [weekly_growth * fcr for fcr in [fcr]*weeks]

feed_cum = np.cumsum(weekly_feed)
weeks_range = np.arange(1, weeks+1)

fig1, ax1 = plt.subplots()
ax1.plot(weeks_range, feed_cum, marker="o")
ax1.set_xlabel("Minggu")
ax1.set_ylabel("Kumulatif Pakan (kg)")
ax1.set_title("Kebutuhan Pakan Kumulatif per Minggu")
st.pyplot(fig1)

# === Visualisasi proyeksi laba ===
st.subheader("💹 Proyeksi Laba")

profit_per_week = (revenue - total_cost) * (weeks_range/weeks)

fig2, ax2 = plt.subplots()
ax2.plot(weeks_range, profit_per_week, color="green", marker="x")
ax2.set_xlabel("Minggu")
ax2.set_ylabel("Laba (Rp)")
ax2.set_title("Proyeksi Laba per Minggu")
st.pyplot(fig2)