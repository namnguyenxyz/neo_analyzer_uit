import streamlit as st

from src.dashboard import data_access, plots, ui


@st.cache_data(show_spinner=False)
def _cached_totals():
    return data_access.get_totals()


@st.cache_data(show_spinner=False)
def _cached_closest():
    return data_access.get_closest_approach_today()


@st.cache_data(show_spinner=False)
def _cached_filtered_rows(search_text: str, hazard_only: bool, sort_desc: bool, limit: int, offset: int):
    return data_access.fetch_latest_filtered(
        limit=limit,
        offset=offset,
        search_text=search_text,
        hazard_only=hazard_only,
        sort_desc=sort_desc,
    )


@st.cache_data(show_spinner=False)
def _cached_filtered_count(search_text: str, hazard_only: bool):
    return data_access.count_latest_filtered(search_text=search_text, hazard_only=hazard_only)


@st.cache_data(show_spinner=False)
def _cached_frame():
    return data_access.fetch_visualization_frame()


def main():
    st.set_page_config(page_title="NEO-Light Dashboard", layout="wide")
    st.title("NEO-Light — Dashboard")

    totals = _cached_totals()

    cols = st.columns(3)
    ui.kpi_card(cols[0], "Total NEOs", totals.get("total_neos"))
    ui.kpi_card(cols[1], "Total PHAs", totals.get("total_phas"))
    closest = _cached_closest()
    ui.kpi_card(cols[2], "Closest Approach Today", closest[0] if closest else "n/a")

    st.sidebar.header("Explorer Filters")
    search_text = st.sidebar.text_input("Search object name")
    hazard_only = st.sidebar.checkbox("Hazard candidates only", value=False)
    sort_desc = st.sidebar.checkbox("Sort by farthest first", value=False)
    page_size = st.sidebar.selectbox("Rows per page", [25, 50, 100], index=1)
    total_filtered = _cached_filtered_count(search_text, hazard_only)
    total_pages = max(1, (total_filtered + page_size - 1) // page_size)
    page_number = st.sidebar.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    offset = (int(page_number) - 1) * page_size

    st.header("Recent NEOs")
    st.caption(f"Showing page {int(page_number)} of {total_pages} ({total_filtered} matching rows)")
    rows = _cached_filtered_rows(
        search_text,
        hazard_only,
        sort_desc,
        page_size,
        offset,
    )
    if rows:
        ui.table_view(rows)
    else:
        st.info("No data available — run the analytics build first.")

    st.header("Visualizations")
    frame = _cached_frame()
    if len(frame) > 0:
        left, right = st.columns(2)
        left.plotly_chart(plots.size_distribution(frame), use_container_width=True)
        right.plotly_chart(plots.approach_velocity_scatter(frame), use_container_width=True)
    else:
        st.info("No visualization data available.")


if __name__ == "__main__":
    main()
