import streamlit as st


# ============================================================
# GLOBAL PAGE STYLE
# ============================================================

def inject_global_css():
    css = """
<style>
    .app-title {
        font-size: 32px;
        font-weight: 700;
        color: white;
        margin-bottom: 6px;
    }

    .app-subtitle {
        font-size: 16px;
        color: #dbeafe;
        line-height: 1.5;
    }

    .page-header {
        background: linear-gradient(
            135deg,
            #123f63 0%,
            #176b82 100%
        );
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }

    .page-header-title {
        color: white;
        font-size: 30px;
        font-weight: 700;
        margin: 0;
    }

    .page-header-subtitle {
        color: #d9edf5;
        font-size: 15px;
        margin-top: 7px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #16324f;
        margin-top: 22px;
        margin-bottom: 14px;
    }

    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 20px 18px;
        min-height: 145px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }

    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 10px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #123f63;
        margin-bottom: 7px;
    }

    .kpi-description {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.4;
    }

    .home-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        min-height: 190px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 5px 16px rgba(0,0,0,0.07);
        margin-bottom: 18px;
    }

    .home-card-title {
        font-size: 20px;
        font-weight: 700;
        color: #16324f;
        margin-bottom: 10px;
    }

    .home-card-text {
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
    }

    .welcome-card {
        background: white;
        border-radius: 16px;
        padding: 25px 30px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 22px;
    }

    .welcome-title {
        font-size: 18px;
        font-weight: 700;
        color: #16324f;
        margin-bottom: 12px;
    }

    .welcome-text {
        font-size: 14px;
        color: #475569;
        line-height: 1.7;
    }
</style>
"""

    st.markdown(css, unsafe_allow_html=True)


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def inject_custom_css():
    inject_global_css()


# ============================================================
# HEADER
# ============================================================

def render_header(title, subtitle=""):
    html = (
        '<div class="page-header">'
        f'<div class="page-header-title">{title}</div>'
        f'<div class="page-header-subtitle">{subtitle}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# KPI CARD
# ============================================================

def render_kpi(title, value, description=""):
    html = (
        '<div class="kpi-card">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-description">{description}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SECTION TITLE
# ============================================================

def render_section_title(title):
    html = f'<div class="section-title">{title}</div>'

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# HOME WELCOME CARD
# ============================================================

def render_welcome(title, text):
    html = (
        '<div class="welcome-card">'
        f'<div class="welcome-title">{title}</div>'
        f'<div class="welcome-text">{text}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# HOME FEATURE CARD
# ============================================================

def render_home_card(title, text):
    html = (
        '<div class="home-card">'
        f'<div class="home-card-title">{title}</div>'
        f'<div class="home-card-text">{text}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

def render_footer():
    html = (
        '<div style="text-align:center; '
        'color:#94a3b8; '
        'font-size:12px; '
        'padding:20px 0;">'
        'Pharma Inventory Analytics Platform'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# HOME PAGE TITLE
# ============================================================

def render_app_title(title, subtitle=""):
    html = (
        '<div class="app-title">'
        f'{title}'
        '</div>'
        '<div class="app-subtitle">'
        f'{subtitle}'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# HOME PAGE WELCOME
# ============================================================

def render_home_welcome(title, text):
    html = (
        '<div class="welcome-card">'
        f'<div class="welcome-title">{title}</div>'
        f'<div class="welcome-text">{text}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# HOME AI FEATURE CARD
# ============================================================

def render_ai_card(title, text):
    html = (
        '<div class="ai-card">'
        f'<div class="ai-card-title">{title}</div>'
        f'<div class="ai-card-text">{text}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)
# ============================================================
# IMPORTANT:
# DO NOT CALL inject_global_css() HERE
# ============================================================