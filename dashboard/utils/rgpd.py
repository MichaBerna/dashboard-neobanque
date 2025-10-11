import streamlit as st


def show_rgpd_conseiller(translations):
    with st.container():
        st.subheader(translations["rgpd_conseiller_title"])

        st.write(translations["rgpd_conseiller_intro"])
        st.write(translations["rgpd_conseiller_detail_1"])
        st.write(translations["rgpd_conseiller_detail_2"])
        st.write(translations["rgpd_conseiller_detail_3"])

        if st.checkbox(translations["rgpd_conseiller_checkbox"]):
            st.session_state["rgpd_conseiller"] = True
            st.success(translations["rgpd_conseiller_success"])
            st.rerun()
        else:
            st.error(translations["rgpd_conseiller_warning"])
            st.stop()
