import streamlit as st

from views.icon_utils import svg_icon_html


def learning_callout(text, detail=None):
    detail_html = ""
    if detail:
        detail_html = f'<div class="sq-learning-detail">{detail}</div>'

    st.markdown(
        f"""
        <div class="sq-learning-callout">
            <div class="sq-learning-title">
                {svg_icon_html("statquest-mark.svg", size=16, alt="Learning takeaway")}
                <span>Learning takeaway</span>
            </div>
            <div class="sq-learning-text">{text}</div>
            {detail_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
