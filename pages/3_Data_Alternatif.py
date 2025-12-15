import streamlit as st
import pandas as pd

st.title("3. Data Alternatif (Supplier)")

# ============ INITIAL DATA ===============
if "alternatif" not in st.session_state:
    st.session_state.alternatif = pd.DataFrame({
        "Alternatif": [
            "Beska","Fow","Gerai Hutan","Pesirah","Benawa",
            "Samping Roastery","Koloni","Agam Pisan","Dialek","Diego"
        ]
    })

# ============ HEADER + TOMBOL TAMBAH ==============
col1, col2 = st.columns([3,1])

with col1:
    st.subheader("Daftar Alternatif")

with col2:
    show_add = st.toggle("➕ Tambah Data")  # ganti modal dengan toggle


# ============ FORM TAMBAH DATA (EXPANDER) ===========
if show_add:
    with st.expander("Form Tambah Alternatif", expanded=True):
        new_name = st.text_input("Nama Alternatif Baru")

        if st.button("Simpan"):
            if new_name.strip() == "":
                st.error("Nama alternatif tidak boleh kosong.")
            else:
                # Tambah data
                new_row = pd.DataFrame({"Alternatif": [new_name]})
                st.session_state.alternatif = pd.concat(
                    [st.session_state.alternatif, new_row],
                    ignore_index=True
                )
                st.success("Alternatif berhasil ditambahkan!")
                st.rerun()

# ============ TABLE DATA EDITOR (TANPA DUPLIKAT) ============
edited = st.data_editor(
    st.session_state.alternatif,
    num_rows="dynamic"
)

st.session_state.alternatif = edited
