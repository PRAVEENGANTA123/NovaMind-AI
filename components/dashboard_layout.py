import streamlit as st


def dashboard_layout():

    # =============================
    # Statistics
    # =============================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        with st.container(border=True):
            st.empty()

    with c2:
        with st.container(border=True):
            st.empty()

    with c3:
        with st.container(border=True):
            st.empty()

    with c4:
        with st.container(border=True):
            st.empty()

    st.write("")

    # =============================
    # Middle
    # =============================

    left, right = st.columns([2, 1])

    with left:
        with st.container(border=True):
            st.empty()

    with right:
        with st.container(border=True):
            st.empty()

    st.write("")

    # =============================
    # Bottom
    # =============================

    a, b, c = st.columns(3)

    with a:
        with st.container(border=True):
            st.empty()

    with b:
        with st.container(border=True):
            st.empty()

    with c:
        with st.container(border=True):
            st.empty()