import streamlit as st
import plotly.graph_objects as go
from logic import generator, scorer, feedback as fb_module
from views.icon_utils import svg_icon_html
from views.ui_components import learning_callout


def _score_header():
    rn = st.session_state.round_number
    score = st.session_state.score
    st.markdown(f"""
    <div style="
        display:flex;align-items:center;justify-content:space-between;
        background:#ffffff;
        border:1px solid #d9d8d0;
        border-radius:4px;
        padding:14px 20px;
        margin-bottom:24px;
    ">
        <div>
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;">Round</div>
            <div style="font-family:'Limelight',cursive;font-size:26px;color:#14080e;line-height:1;">{rn} / 5</div>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;gap:8px;
                    font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                    letter-spacing:0.15em;text-transform:uppercase;color:#799496;text-align:center;line-height:1;">
            {svg_icon_html("correlation.svg", size=18, alt="Guess the Correlation")}
            <span>Guess the Correlation</span>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;">Score</div>
            <div style="font-family:'Limelight',cursive;font-size:26px;color:#14080e;line-height:1;">{score}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _scatter(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["x"],
        y=data["y"],
        mode="markers",
        marker=dict(color="#49475b", size=7, opacity=0.75,
                    line=dict(color="#acc196", width=0.5)),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor="#e8e7e2", zeroline=False,
                   showticklabels=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#e8e7e2", zeroline=False,
                   showticklabels=False, title=""),
        height=340,
    )
    return fig


def show():
    difficulty = st.session_state.get("difficulty", "easy")

    # Generate data once per round
    if st.session_state.get("round_data") is None:
        st.session_state.round_data = generator.generate_correlation_data(difficulty)
        st.session_state.round_submitted = False

    data = st.session_state.round_data

    _score_header()

    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:13px;font-weight:300;
                color:#799496;letter-spacing:0.06em;margin-bottom:12px;">
        Study the scatter plot and estimate the Pearson correlation coefficient.
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(_scatter(data), use_container_width=True, config={"displayModeBar": False})

    if not st.session_state.get("round_submitted", False):
        guess = st.slider(
            "Your guess (r)",
            min_value=-1.0, max_value=1.0, value=0.0, step=0.05,
            key="corr_guess",
        )

        st.markdown(f"""
        <div style="text-align:center;margin-bottom:4px;">
            <span style="font-family:'Limelight',cursive;font-size:32px;color:#14080e;">
                {guess:+.2f}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Submit Guess", key="corr_submit"):
            earned, grade = scorer.score_correlation(guess, data["actual_r"])
            st.session_state.score += earned
            st.session_state.rounds_data.append({
                "round": st.session_state.round_number,
                "score_earned": earned,
                "max_score": 200,
                "correct": earned >= 100,
            })
            st.session_state.round_submitted = True
            st.session_state.last_guess = guess
            st.session_state.last_grade = grade
            st.session_state.last_earned = earned
            st.rerun()

    else:
        guess = st.session_state.get("last_guess", 0.0)
        grade = st.session_state.get("last_grade", "Off")
        earned = st.session_state.get("last_earned", 0)
        actual = data["actual_r"]
        diff = abs(guess - actual)

        grade_colours = {
            "Excellent": "#acc196",
            "Good": "#49475b",
            "Close": "#799496",
            "Off": "#a05252",
        }
        border_col = grade_colours.get(grade, "#799496")

        st.markdown(f"""
        <div style="
            background:#f3f5ec;
            border:1px solid #acc196;
            border-left:3px solid {border_col};
            border-radius:2px;
            padding:16px 20px;
            margin-bottom:16px;
        ">
            <div style="font-family:'Outfit',sans-serif;font-size:10px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#49475b;margin-bottom:6px;">
                {grade} — actual r = {actual:+.2f}
            </div>
            <div style="display:flex;gap:24px;margin-bottom:10px;">
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Your Guess</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#14080e;">{guess:+.2f}</div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Actual r</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#49475b;">{actual:+.2f}</div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Points Earned</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#14080e;">+{earned}</div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Off by</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#799496;">{diff:.2f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        learning_callout(fb_module.FEEDBACK.get(("correlation", grade), ""))

        rn = st.session_state.round_number
        if rn >= 5:
            if st.button("See Results →", key="corr_results"):
                st.session_state.game_complete = True
                st.session_state.page = "results"
                st.rerun()
        else:
            if st.button("Next Round →", key="corr_next"):
                st.session_state.round_number += 1
                st.session_state.round_data = None
                st.session_state.round_submitted = False
                st.rerun()
