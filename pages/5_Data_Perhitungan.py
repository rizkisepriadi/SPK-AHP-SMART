import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import auth

auth.initialize_auth_state()

auth.require_auth()

# Sidebar
with st.sidebar:
    if st.button("Logout", use_container_width=True):
        success, error_msg = auth.sign_out()
        if success:
            st.success("Berhasil logout!")
            st.rerun()
        else:
            st.error(f"Logout gagal: {error_msg}")

st.title("5. Perhitungan AHP + SMART")

if "kriteria" not in st.session_state or not st.session_state.kriteria:
    st.error("Hitung bobot AHP terlebih dahulu pada halaman Data Kriteria.")
    st.stop()

if "penilaian" not in st.session_state:
    st.error("Isi Data Penilaian terlebih dahulu.")
    st.stop()

if "bobot_ahp" not in st.session_state:
    st.error("Hitung bobot AHP terlebih dahulu pada halaman Data Kriteria.")
    st.stop()

weights = st.session_state.bobot_ahp.copy()
pen = st.session_state.penilaian.copy()

norm = pen.copy()

# COST → Harga & Pengiriman
for col in ["Harga", "Pengiriman"]:
    v = norm[col].astype(float)
    norm[col] = (v.max() - v) / (v.max() - v.min())

# BENEFIT → 3 Likert
for col in ["Kualitas","Fleksibilitas","Pelayanan"]:
    v = norm[col].astype(float)
    norm[col] = (v - v.min()) / (v.max() - v.min())

criteria = ["Harga","Kualitas","Pengiriman","Fleksibilitas","Pelayanan"]
w = np.array(weights)

scores = (norm[criteria].values * w).sum(axis=1)

result = pd.DataFrame({
    "Alternatif": pen["Alternatif"],
    "Score": scores,
})
result["Rank"] = result["Score"].rank(ascending=False, method="min").astype(int)
result = result.sort_values("Score", ascending=False)

st.subheader("Normalisasi SMART")
st.table(norm)

st.subheader("Hasil Perhitungan")
st.table(result)

st.session_state.hasil = result
