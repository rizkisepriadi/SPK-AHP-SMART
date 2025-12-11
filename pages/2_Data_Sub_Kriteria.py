import streamlit as st
import pandas as pd
import sys
from pathlib import Path

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import auth

auth.initialize_auth_state()

auth.require_auth()

st.title("2. Data Sub-Kriteria (SMART)")

st.write("Sub-kriteria hanya untuk Harga & Pengiriman.")

# Sidebar
with st.sidebar:
    if st.button("Logout", use_container_width=True):
        success, error_msg = auth.sign_out()
        if success:
            st.success("Berhasil logout!")
            st.rerun()
        else:
            st.error(f"Logout gagal: {error_msg}")

if 'subkriteria' not in st.session_state:
    df = pd.DataFrame({
        "Kriteria": ["Harga", "Pengiriman"],
        "SubKriteria": ["Harga Biji Kopi", "Waktu Pengiriman"]
    })
    st.session_state.subkriteria = df

edited = st.data_editor(st.session_state.subkriteria, num_rows="dynamic")
st.session_state.subkriteria = edited

st.subheader("Sub-Kriteria Saat Ini:")
st.table(edited)


st.info("Tidak menggunakan bobot sub-kriteria — SMART langsung memakai nilai numerik.")
