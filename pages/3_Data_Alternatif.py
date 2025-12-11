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

# Sidebar
with st.sidebar:
        if st.button("Logout", use_container_width=True):
            success, error_msg = auth.sign_out()
            if success:
                st.success("Berhasil logout!")
                st.rerun()
            else:
                st.error(f"Logout gagal: {error_msg}")

st.title("3. Data Alternatif (Supplier)")

if "alternatif" not in st.session_state:
    st.session_state.alternatif = pd.DataFrame({
        "Alternatif": [
            "Beska","Fow","Gerai Hutan","Pesirah","Benawa",
            "Samping Roastery","Koloni","Agam Pisan","Dialek","Diego"
        ]
    })

edited = st.data_editor(st.session_state.alternatif, num_rows="dynamic")
st.session_state.alternatif = edited

st.subheader("Daftar Alternatif:")
st.table(edited)
