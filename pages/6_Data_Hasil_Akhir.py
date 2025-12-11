import streamlit as st
import pandas as pd
import altair as alt
import sys
from pathlib import Path

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import auth

auth.initialize_auth_state()

auth.require_auth()

st.title("6. Hasil Akhir & Download")

# Sidebar
with st.sidebar:
    if st.button("Logout", use_container_width=True):
        success, error_msg = auth.sign_out()
        if success:
            st.success("Berhasil logout!")
            st.rerun()
        else:
            st.error(f"Logout gagal: {error_msg}")

if "hasil" not in st.session_state:
    st.error("Belum ada hasil perhitungan.")
    st.stop()

res = st.session_state.hasil.copy()
res["Score"] = res["Score"].round(4)

st.subheader("Ranking Akhir")
st.table(res)

chart = alt.Chart(res).mark_bar().encode(
    x="Score",
    y=alt.Y("Alternatif", sort="-x")
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

csv = res.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "hasil_ahp_smart.csv", "text/csv")
