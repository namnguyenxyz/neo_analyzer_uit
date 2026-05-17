import streamlit as st

from src.dashboard import data_access, plots, ui


def main():
    st.set_page_config(page_title="NEO-Light Dashboard", layout="wide")
    st.title("NEO-Light — Dashboard")

    totals = data_access.get_totals()

    cols = st.columns(3)
    ui.kpi_card(cols[0], "Total NEOs", totals.get("total_neos"))
    ui.kpi_card(cols[1], "Total PHAs", totals.get("total_phas"))
    closest = data_access.get_closest_approach_today()
    ui.kpi_card(cols[2], "Closest Approach Today", closest[0] if closest else "n/a")

    st.sidebar.header("Explorer Filters")
    search_text = st.sidebar.text_input("Search object name")
    hazard_only = st.sidebar.checkbox("Hazard candidates only", value=False)
    sort_desc = st.sidebar.checkbox("Sort by farthest first", value=False)
    page_size = st.sidebar.selectbox("Rows per page", [25, 50, 100], index=1)

    st.header("Recent NEOs")
    rows = data_access.fetch_latest_filtered(
        limit=page_size,
        offset=0,
        search_text=search_text,
        hazard_only=hazard_only,
        sort_desc=sort_desc,
    )
    if rows:
        ui.table_view(rows)
    else:
        st.info("No data available — run the analytics build first.")

    st.header("Visualizations")
    frame = data_access.fetch_visualization_frame()
    if len(frame) > 0:
        left, right = st.columns(2)
        left.plotly_chart(plots.size_distribution(frame), use_container_width=True)
        right.plotly_chart(plots.approach_velocity_scatter(frame), use_container_width=True)
    else:
        st.info("No visualization data available.")


if __name__ == "__main__":
    main()
