"""
=========================================
NovaMind AI - Appearance Settings
=========================================
"""

import streamlit as st


def show_appearance_settings(settings):
    """
    Appearance Settings Component
    """

    st.subheader("🎨 Appearance")

    # =====================================
    # Theme
    # =====================================

    themes = [
        "Auto",
        "Light",
        "Dark",
    ]

    theme_value = str(
        settings.get("theme", "Auto")
    ).strip().lower()

    theme_index = {
        "auto": 0,
        "system": 0,
        "light": 1,
        "dark": 2,
    }.get(theme_value, 0)

    # =====================================
    # Accent Color
    # =====================================

    accents = [
        "Blue",
        "Green",
        "Purple",
        "Orange",
        "Red",
    ]

    accent_value = str(
        settings.get("accent", "Blue")
    ).strip().title()

    if accent_value not in accents:
        accent_value = "Blue"

    accent_index = accents.index(accent_value)

    # =====================================
    # Font Size
    # =====================================

    fonts = [
        "Small",
        "Medium",
        "Large",
    ]

    font_value = str(
        settings.get("font_size", "Medium")
    ).strip().title()

    if font_value not in fonts:
        font_value = "Medium"

    font_index = fonts.index(font_value)

    # =====================================
    # Layout
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        theme = st.selectbox(
            "Theme",
            options=themes,
            index=theme_index,
            key="appearance_theme",
        )

        accent = st.selectbox(
            "Accent Color",
            options=accents,
            index=accent_index,
            key="appearance_accent",
        )

    with col2:

        font_size = st.selectbox(
            "Font Size",
            options=fonts,
            index=font_index,
            key="appearance_font",
        )

        compact_mode = st.toggle(
            "Compact Mode",
            value=bool(
                settings.get(
                    "compact_mode",
                    False,
                )
            ),
            key="appearance_compact",
        )

    # =====================================
    # Return Selected Settings
    # =====================================

    return {
        "theme": theme,
        "accent": accent,
        "font_size": font_size,
        "compact_mode": compact_mode,
    }