import streamlit as st


def set_page_config():
    st.set_page_config(page_title="Dashboard Neobanque", layout="wide")
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 750px !important;
                padding-left: 0rem !important;
                padding-right: 0rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
