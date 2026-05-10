import random
import streamlit as st
import plotly.graph_objects as go
from logic import generator, scorer, feedback as fb_module
from views.icon_utils import svg_icon_html
from views.ui_components import learning_callout


_ALL_TYPES = ["normal", "right_skewed", "left_skewed", "bimodal", "uniform"]

_LABELS = {
    "normal": "Normal",
    "right_skewed": "Right-Skewed",
    "left_skewed": "Left-Skewed",
    "bimodal": "Bimodal",
    "uniform": "Uniform",
}

_DEFINITIONS = {
    "normal": "Symmetric, bell-shaped. Mean ≈ Median ≈ Mode. E.g. heights of adults.",
    "right_skewed": "Long tail to the right. Mean > Median. E.g. household incomes.",
    "left_skewed": "Long tail to the left. Mean < Median. E.g. age at retirement.",
    "bimodal": "Two distinct peaks. Indicates two sub-populations. E.g. exam scores with two cohorts.",
    "uniform": "All values equally likely. Flat histogram. E.g. rolling a fair die many times.",
}


def _score_header():
    rn = st.session_state.round_number
    score = st.session_state.score
    st.markdown(f"""
    <div style="
        display:flex;align-items:center;justify-content:space-between;
        background:#ffffff;border:1px solid #d9d8d0;
        border-radius:4px;padding:14px 20px;margin-bottom:24px;
    ">
        <div>
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;">Round</div>
            <div style="font-family:'Limelight',cursive;font-size:26px;color:#14080e;line-height:1;">{rn} / 5</div>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;gap:8px;
                    font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                    letter-spacing:0.15em;text-transform:uppercase;color:#799496;text-align:center;line-height:1;">
            {svg_icon_html("distribution.svg", size=18, alt="Name That Distribution")}
            <span>Name That Distribution</span>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;">Score</div>
            <div style="font-family:'Limelight',cursive;font-size:26px;color:#14080e;line-height:1;">{score}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _histogram(data):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data["data"],
        nbinsx=25,
        marker=dict(color="#acc196", line=dict(color="#49475b", width=0.8)),
        opacity=0.9,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#e8e7e2", zeroline=False, title=""),
        bargap=0.05,
        height=300,
    )
    return fig


def show():
    difficulty = st.session_state.get("difficulty", "easy")

    if st.session_state.get("round_data") is None:
        raw = generator.generate_distribution_data(difficulty)
        correct = raw["distribution_type"]
        wrong = [t for t in _ALL_TYPES if t != correct]
        options = random.sample(wrong, 3) + [correct]
        random.shuffle(options)
        raw["options"] = options
        st.session_state.round_data = raw
        st.session_state.round_submitted = False

    data = st.session_state.round_data

    _score_header()

    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:13px;font-weight:300;
                color:#799496;letter-spacing:0.06em;margin-bottom:12px;">
        Examine the histogram and identify the distribution shape.
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(_histogram(data), use_container_width=True, config={"displayModeBar": False})

    if not st.session_state.get("round_submitted", False):
        options = data["options"]
        answer_cols = st.columns(4)

        for col, opt in zip(answer_cols, options):
            with col:
                if st.button(_LABELS[opt], key=f"dist_{opt}"):
                    correct = data["distribution_type"]
                    is_correct = (opt == correct)
                    earned = scorer.score_distribution(opt, correct)
                    st.session_state.score += earned
                    st.session_state.rounds_data.append({
                        "round": st.session_state.round_number,
                        "score_earned": earned,
                        "max_score": 100,
                        "correct": is_correct,
                    })
                    st.session_state.round_submitted = True
                    st.session_state.last_answer = opt
                    st.session_state.last_correct = is_correct
                    st.session_state.last_earned = earned
                    st.rerun()

    else:
        answer = st.session_state.get("last_answer", "")
        is_correct = st.session_state.get("last_correct", False)
        correct_type = data["distribution_type"]
        earned = st.session_state.get("last_earned", 0)
        skewness = data["skewness"]

        banner_bg = "#e8f5e4" if is_correct else "#fdf0f0"
        banner_border = "#acc196" if is_correct else "#c97c7c"
        result_word = "Correct!" if is_correct else "Not Quite"
        fb_text = fb_module.FEEDBACK.get(("distribution", is_correct), "")

        st.markdown(f"""
        <div style="
            background:{banner_bg};
            border:1px solid {banner_border};
            border-left:3px solid {banner_border};
            border-radius:2px;
            padding:16px 20px;
            margin-bottom:16px;
        ">
            <div style="font-family:'Outfit',sans-serif;font-size:10px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;
                        color:{'#3a7a35' if is_correct else '#a05252'};margin-bottom:8px;">
                {result_word}
            </div>
            <div style="display:flex;gap:24px;margin-bottom:10px;">
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Your Answer</div>
                    <div style="font-family:'Limelight',cursive;font-size:18px;
                                color:{'#14080e' if is_correct else '#a05252'};">
                        {_LABELS.get(answer, answer)}
                    </div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Correct Answer</div>
                    <div style="font-family:'Limelight',cursive;font-size:18px;color:#14080e;">
                        {_LABELS[correct_type]}
                    </div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Measured Skewness</div>
                    <div style="font-family:'Limelight',cursive;font-size:18px;color:#49475b;">
                        {skewness:+.2f}
                    </div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Points</div>
                    <div style="font-family:'Limelight',cursive;font-size:18px;color:#14080e;">+{earned}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        learning_callout(fb_text, _DEFINITIONS[correct_type])

        rn = st.session_state.round_number
        if rn >= 5:
            if st.button("See Results →", key="dist_results"):
                st.session_state.game_complete = True
                st.session_state.page = "results"
                st.rerun()
        else:
            if st.button("Next Round →", key="dist_next"):
                st.session_state.round_number += 1
                st.session_state.round_data = None
                st.session_state.round_submitted = False
                st.rerun()
