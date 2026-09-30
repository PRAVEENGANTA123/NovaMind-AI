"""
=========================================
NovaMind AI - Dashboard Activity
=========================================

Displays the user's AI chat activity
over the last 7 days.
"""

from datetime import datetime, timedelta

import plotly.graph_objects as go
import streamlit as st

from database.mongodb import chats_collection


# =====================================
# Dashboard Activity
# =====================================

def show_dashboard_activity(email: str):
    """
    Display last 7 days AI chat activity.
    """

    today = datetime.utcnow()

    labels = []

    values = []

    # ---------------------------------
    # Last 7 Days
    # ---------------------------------

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        start = datetime(
            day.year,
            day.month,
            day.day,
        )

        end = start + timedelta(days=1)

        total = chats_collection.count_documents(

            {
                "email": email,

                "created_at": {

                    "$gte": start,

                    "$lt": end,

                },

            }

        )

        labels.append(

            day.strftime("%a")

        )

        values.append(total)

    # ---------------------------------
    # Plotly Chart
    # ---------------------------------

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=labels,

            y=values,

            mode="lines+markers",

            line=dict(

                color="#2563EB",

                width=4,

            ),

            marker=dict(

                size=8,

                color="#2563EB",

            ),

            fill="tozeroy",

            fillcolor="rgba(37,99,235,0.12)",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Chats: %{y}<extra></extra>"
            ),

        )

    )

    fig.update_layout(

        height=320,

        margin=dict(

            l=10,

            r=10,

            t=15,

            b=10,

        ),

        showlegend=False,

        paper_bgcolor="white",

        plot_bgcolor="white",

        hovermode="x unified",

        xaxis=dict(

            title="",

            showgrid=False,

            zeroline=False,

        ),

        yaxis=dict(

            title="Chats",

            rangemode="tozero",

            gridcolor="#E5E7EB",

            zeroline=False,

        ),

    )

    st.plotly_chart(

        fig,

        width="stretch",

    )

    # ---------------------------------
    # Summary
    # ---------------------------------

    total_week = sum(values)

    busiest = max(values) if values else 0

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Chats This Week",

            total_week,

        )

    with c2:

        st.metric(

            "Most Active Day",

            busiest,

        )