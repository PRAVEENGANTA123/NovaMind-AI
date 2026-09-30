import streamlit as st
import plotly.graph_objects as go


def show_dashboard_charts():
    st.error("NEW CHART COMPONENT LOADED")
def show_dashboard_charts():

    days = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"]

    requests = [
        35,
        52,
        41,
        63,
        58,
        72,
        81
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=days,
            y=requests,
            mode="lines+markers",
            line=dict(
                color="#7C5CFC",
                width=4
            ),
            marker=dict(
                color="#7C5CFC",
                size=8
            ),
            fill="tozeroy",
            fillcolor="rgba(124,92,252,0.15)"
        )
    )

    fig.update_layout(

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        font=dict(
            color="white",
            size=14
        ),

        height=340,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        showlegend=False,

        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#94A3B8")
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#263244",
            zeroline=False,
            tickfont=dict(color="#94A3B8")
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "displaylogo": False
        }
    )