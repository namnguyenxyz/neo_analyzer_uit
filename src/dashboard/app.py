import streamlit as st
from . import data_access


def main():
    st.set_page_config(page_title="NEO-Light Dashboard", layout="wide")
    st.title("NEO-Light — Dashboard")

    totals = data_access.get_totals()

    cols = st.columns(3)
    cols[0].metric("Total NEOs", totals.get("total_neos"))
    cols[1].metric("Total PHAs", totals.get("total_phas"))
    closest = data_access.get_closest_approach_today()
    cols[2].metric("Closest Approach Today", closest[0] if closest else "n/a")

    st.header("Recent NEOs")
    rows = data_access.fetch_latest(100)
    if rows:
        st.dataframe(rows)
    else:
        st.info("No data available — run the analytics build first.")


if __name__ == "__main__":
    main()
