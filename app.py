import os
import streamlit as st
from views.icon_utils import icon_path

st.set_page_config(
    page_title="StatQuest",
    page_icon=icon_path("favicon.png"),
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Inject global CSS
_css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
with open(_css_path, encoding="utf-8") as _f:
    st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)

# Session state defaults
_DEFAULTS = {
    "page": "home",
    "score": 0,
    "round_number": 1,
    "current_mode": "",
    "difficulty": "easy",
    "rounds_data": [],
    "game_complete": False,
    "round_data": None,
    "round_submitted": False,
    "clicked_index": None,
    "score_saved": False,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# Reset score_saved flag when starting a new game
if st.session_state.page != "results":
    st.session_state.score_saved = False

# Import pages (deferred to avoid circular issues at module load)
from views import home, mode_select, game_correlation, game_distribution, game_outlier, results  # noqa: E402

_ROUTES = {
    "home": home.show,
    "mode_select": mode_select.show,
    "game_correlation": game_correlation.show,
    "game_distribution": game_distribution.show,
    "game_outlier": game_outlier.show,
    "results": results.show,
}

_page = st.session_state.get("page", "home")
_ROUTES.get(_page, home.show)()
