import streamlit as st

from views.icon_utils import svg_icon_html


def show():
    # Hero block
    st.markdown("""
    <div style="
        background:#e9eb9e;
        border:1px solid #acc196;
        border-radius:4px;
        padding:56px 48px 40px;
        text-align:center;
        position:relative;
        overflow:hidden;
        margin-bottom:40px;
    ">
        <div style="
            position:absolute;inset:0;
            background:
                repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(172,193,150,0.35) 39px,rgba(172,193,150,0.35) 40px),
                repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(172,193,150,0.35) 39px,rgba(172,193,150,0.35) 40px);
        "></div>
        <div style="position:relative">
            <div style="
                font-family:'Outfit',sans-serif;
                font-size:10px;
                letter-spacing:0.3em;
                text-transform:uppercase;
                color:#49475b;
                margin-bottom:16px;
            ">Interactive Statistics &middot; University Edition</div>
            <div style="
                font-family:'Limelight',cursive;
                font-size:72px;
                color:#14080e;
                line-height:1;
                letter-spacing:0.02em;
            ">Stat<span style="color:#49475b">Quest</span></div>
            <div style="
                font-family:'Outfit',sans-serif;
                font-size:13px;
                font-weight:300;
                letter-spacing:0.28em;
                text-transform:uppercase;
                color:#49475b;
                margin-top:14px;
            ">How well do you really know your stats?</div>
            <div style="
                display:flex;align-items:center;justify-content:center;
                gap:12px;margin-top:24px;
            ">
                <div style="width:80px;height:1px;background:#acc196;"></div>
                <div style="width:6px;height:6px;background:#49475b;transform:rotate(45deg);"></div>
                <div style="width:6px;height:6px;background:#49475b;transform:rotate(45deg);opacity:0.35;"></div>
                <div style="width:6px;height:6px;background:#49475b;transform:rotate(45deg);"></div>
                <div style="width:80px;height:1px;background:#acc196;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Difficulty selector label
    st.markdown("""
    <div style="
        font-family:'Outfit',sans-serif;
        font-size:11px;
        font-weight:600;
        letter-spacing:0.18em;
        text-transform:uppercase;
        color:#799496;
        display:flex;align-items:center;gap:14px;
        margin-bottom:20px;
    ">
        Choose Your Difficulty
        <div style="flex:1;height:1px;background:linear-gradient(to right,#acc196,transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    diff_info = {
        "easy": {
            "label": "Easy",
            "detail": "30 data points &middot; Distinct correlations",
            "icon": "difficulty-easy.svg",
        },
        "medium": {
            "label": "Medium",
            "detail": "60 data points &middot; Full r range",
            "icon": "difficulty-medium.svg",
        },
        "hard": {
            "label": "Hard",
            "detail": "100 data points &middot; Closely clustered r",
            "icon": "difficulty-hard.svg",
        },
    }

    cols = st.columns(3, gap="medium")
    for col, (diff_key, info) in zip(cols, diff_info.items()):
        with col:
            st.markdown(f"""
            <div class="sq-diff-card" style="
                background:#ffffff;
                border:1px solid #d9d8d0;
                border-top:3px solid #acc196;
                border-radius:4px 4px 0 0;
                padding:28px 20px 24px;
                text-align:center;
            ">
                <div class="sq-difficulty-icon">
                    {svg_icon_html(info['icon'], size=24, alt=info['label'])}
                </div>
                <div style="
                    font-family:'Limelight',cursive;
                    font-size:20px;
                    color:#14080e;
                    margin-bottom:8px;
                ">{info['label']}</div>
                <div style="
                    font-family:'Outfit',sans-serif;
                    font-size:11px;
                    font-weight:300;
                    color:#799496;
                    letter-spacing:0.06em;
                    line-height:1.6;
                ">{info['detail']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(info["label"], key=f"diff_{diff_key}"):
                st.session_state.difficulty = diff_key
                st.session_state.page = "mode_select"
                st.rerun()
