import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def line_chart(df, x, y, title):

    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        markers=False
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        title_x=0.5
    )

    return fig


def pie_chart(df, column, title):

    data = (
        df[column]
        .value_counts()
        .reset_index()
    )

    data.columns = [column, "Count"]

    fig = px.pie(
        data,
        names=column,
        values="Count",
        hole=0.45,
        title=title
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        title_x=0.5
    )

    return fig


def histogram(df, column, title):

    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        title=title
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        title_x=0.5
    )

    return fig

def bar_chart(df, x, y, title):

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=y
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        title_x=0.5
    )

    return fig


def scatter_chart(df, x, y, title):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=title,
        color=y
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        title_x=0.5
    )

    return fig



def pde_chart(distance, concentration, source_location):

    import pandas as pd
    import plotly.express as px

    data = pd.DataFrame({
        "Distance (km)": distance,
        "Pollution (mg/L)": concentration
    })

    fig = px.line(
        data,
        x="Distance (km)",
        y="Pollution (mg/L)",
        title="Pollutant Concentration Along River"
    )

    fig.update_traces(line_width=4)

    # Pollution source marker
    fig.add_vline(
        x=source_location,
        line_dash="dash",
        line_color="red",
        annotation_text="Pollution Source",
        annotation_position="top"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        title_x=0.5,
        xaxis_title="River Distance (km)",
        yaxis_title="Pollution Concentration (mg/L)"
    )

    return fig

def heatmap_chart(history, distance):

    fig = px.imshow(
        history,
        x=distance,
        aspect="auto",
        color_continuous_scale="Turbo",
        labels={
            "x": "River Distance (km)",
            "y": "Time Step",
            "color": "Pollution (mg/L)"
        },
        title="Pollution Evolution Over Time"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        title_x=0.5
    )

    return fig




def animation_chart(distance, history):

    fig = go.Figure()

    # First Frame
    fig.add_trace(
        go.Scatter(
            x=distance,
            y=history[0],
            mode="lines",
            line=dict(width=4)
        )
    )

    # Animation Frames
    frames = []

    for i in range(len(history)):

        frames.append(

            go.Frame(

                data=[
                    go.Scatter(
                        x=distance,
                        y=history[i]
                    )
                ],

                name=str(i)

            )

        )

    fig.frames = frames

    fig.update_layout(

        title="Animated Pollution Transport",

        template="plotly_dark",

        xaxis_title="River Distance (km)",

        yaxis_title="Pollution (mg/L)",

        height=600,

        updatemenus=[
            {
                "type": "buttons",

                "buttons": [

                    {
                        "label": "▶ Play",

                        "method": "animate",

                        "args": [
                            None,
                            {
                                "frame": {"duration": 40},
                                "fromcurrent": True
                            }
                        ]
                    },

                    {
                        "label": "⏸ Pause",

                        "method": "animate",

                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0},
                                "mode": "immediate"
                            }
                        ]
                    }

                ]
            }
        ]

    )

    return fig