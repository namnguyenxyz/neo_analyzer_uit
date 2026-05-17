import plotly.express as px


def size_distribution(df):
    fig = px.histogram(df, x="estimated_diameter_m", nbins=30, title="Size distribution")
    return fig


def approach_velocity_scatter(df):
    fig = px.scatter(
        df,
        x="miss_distance_au",
        y="relative_velocity_km_s",
        color="is_potentially_hazardous",
        title="Approach velocity vs miss distance",
    )
    return fig
