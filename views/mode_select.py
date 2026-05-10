import streamlit as st

from views.icon_utils import svg_icon_html


_MODES = [
    {
        "key": "game_correlation",
        "icon": "correlation.svg",
        "name": "Guess the Correlation",
        "desc": "Estimate Pearson's r from a scatter plot",
        "pts": "200 pts / round",
        "border": "#acc196",
    },
    {
        "key": "game_distribution",
        "icon": "distribution.svg",
        "name": "Name That Distribution",
        "desc": "Identify the histogram shape from 4 options",
        "pts": "100 pts / round",
        "border": "#799496",
    },
    {
        "key": "game_outlier",
        "icon": "outlier.svg",
        "name": "Spot the Outlier",
        "desc": "Click the outlier point in the strip plot",
        "pts": "150 pts / round",
        "border": "#49475b",
    },
]


def show():
    diff = st.session_state.get("difficulty", "easy").capitalize()

    st.markdown(f"""
    <div style="margin-bottom:32px;">
        <div style="
            font-family:'Limelight',cursive;
            font-size:36px;
            color:#14080e;
            line-height:1.1;
        ">Choose Your Mode</div>
        <div style="
            font-family:'Outfit',sans-serif;
            font-size:13px;
            font-weight:300;
            color:#799496;
            margin-top:6px;
            letter-spacing:0.08em;
        ">Difficulty: {diff} · 5 rounds per session</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    for col, mode in zip(cols, _MODES):
        with col:
            st.markdown(f"""
            <div class="sq-mode-card" style="
                background:#ffffff;
                border:1px solid #d9d8d0;
                border-left:3px solid {mode['border']};
                border-radius:4px 4px 0 0;
                padding:24px 20px 20px;
                min-height:176px;
                box-sizing:border-box;
            ">
                <div style="
                    width:40px;height:40px;
                    background:#e9eb9e;
                    border:1px solid #acc196;
                    border-radius:2px;
                    display:flex;align-items:center;justify-content:center;
                    line-height:0;
                    margin-bottom:14px;
                ">{svg_icon_html(mode['icon'], size=20, alt=mode['name'])}</div>
                <div style="
                    font-family:'Limelight',cursive;
                    font-size:15px;
                    color:#14080e;
                    line-height:1.3;
                    margin-bottom:6px;
                ">{mode['name']}</div>
                <div style="
                    font-family:'Outfit',sans-serif;
                    font-size:12px;
                    font-weight:300;
                    color:#799496;
                    margin-bottom:12px;
                    line-height:1.5;
                ">{mode['desc']}</div>
                <div style="
                    font-family:'Outfit',sans-serif;
                    font-size:11px;
                    font-weight:600;
                    letter-spacing:0.1em;
                    text-transform:uppercase;
                    color:{mode['border']};
                ">{mode['pts']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Play", key=f"play_{mode['key']}"):
                st.session_state.current_mode = mode["key"]
                st.session_state.score = 0
                st.session_state.round_number = 1
                st.session_state.rounds_data = []
                st.session_state.game_complete = False
                st.session_state.round_data = None
                st.session_state.round_submitted = False
                st.session_state.page = mode["key"]
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_home"):
        st.session_state.page = "home"
        st.rerun()
