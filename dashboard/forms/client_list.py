import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, StAggridTheme
from utils.api_client import get_clients


def render_client_list(translations):
    st.subheader(translations["client_list_title"])

    # Alignement horizontal des boutons "Rafraîchir" et "Créer un client"
    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            translations["refresh_list"],
            key="refresh_button",
            icon=":material/refresh:",
            width="stretch",
        ):
            st.session_state["refresh_requested"] = True
    with col2:
        if st.button(
            translations["create_client_button"],
            key="create_client_button",
            icon=":material/add:",
            width="stretch",
        ):
            st.session_state["page"] = "new_client"
            st.rerun()

    # Récupération des clients
    clients = get_clients()
    if not clients:
        st.warning(translations["no_clients"])
        return

    # Conversion en DataFrame
    df_clients = pd.DataFrame(clients)

    # Sélection des colonnes à afficher
    columns_to_display = ["id", "nom", "prenom", "age", "telephone", "email"]
    df_clients = df_clients[columns_to_display]

    # Configuration de AG Grid
    gb = GridOptionsBuilder.from_dataframe(df_clients)
    gb.configure_pagination(enabled=True, paginationPageSize=10)
    gb.configure_side_bar()

    # Configuration pour que TOUTES les colonnes soient filtrables
    gb.configure_default_column(
        editable=False,
        filterable=True,
        sortable=True,
        resizable=True,
    )

    # Configuration des colonnes avec filtres adaptés
    gb.configure_column("id", header_name=translations["id"], width=80)
    gb.configure_column(
        "nom", header_name=translations["nom"], width=120, filter="agTextColumnFilter"
    )
    gb.configure_column(
        "prenom", header_name=translations["prenom"], width=120, filter="agTextColumnFilter"
    )
    gb.configure_column("age", header_name=translations["age"], width=80)
    gb.configure_column("telephone", header_name=translations["telephone"], width=150)
    gb.configure_column("email", header_name=translations["email"], width=150)

    gb.configure_selection(
        selection_mode="single",
        use_checkbox=False,
    )

    # Affichage du tableau
    theme = (
        StAggridTheme(base="alpine")
        .withParams(**{"fontSize": 16, "rowBorder": True})
        .withParts(*["iconSetAlpine", "colorSchemeDark"])  # type: ignore
    )

    grid_response = AgGrid(
        df_clients,
        gridOptions=gb.build(),
        height=400,
        width="100%",
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme=theme,
    )

    # Vérification de la sélection
    selected_rows = grid_response.get("selected_rows", None)
    if selected_rows is not None and not selected_rows.empty:
        selected_row = selected_rows.iloc[0].to_dict()
        st.session_state["page"] = "client_details"
        st.session_state["selected_client_id"] = selected_row["id"]
        st.rerun()
