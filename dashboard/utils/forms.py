from datetime import datetime

import streamlit as st


def render_input_field(
    col, translations, key, client_data, default, input_type="text", options=None
):
    value = client_data.get(key, default)
    with col:
        if input_type == "text":
            return st.text_input(
                translations[key],
                value=value,
                placeholder=translations.get(key + "_placeholder", ""),
                key=key,
            )
        elif input_type == "select":
            if options is None:
                options = []
            selected_index = 0
            if value in options:
                selected_index = options.index(value)
            return st.selectbox(translations[key], options=options, index=selected_index, key=key)
        elif input_type == "date":
            date_value = None
            if value:
                try:
                    date_value = datetime.strptime(value, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    date_value = None
            return st.date_input(translations[key], value=date_value, key=key)
        elif input_type == "number":
            return st.number_input(translations[key], value=int(value) if value else 0, key=key)
