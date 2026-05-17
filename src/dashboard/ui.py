import streamlit as st


def kpi_card(col, label, value):
    col.metric(label, value)


def table_view(rows):
    st.dataframe(rows)
