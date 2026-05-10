import streamlit as st
import plotly.graph_objects as go
import numpy as np
from logic import generator, scorer, feedback as fb_module
from views.icon_utils import svg_icon_html
from views.ui_components import learning_callout

try:
    from streamlit_plotly_events import plotly_events
    _HAS_EVENTS = True
except ImportError:
    _HAS_EVENTS = False


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
            {svg_icon_html("outlier.svg", size=18, alt="Spot the Outlier")}
            <span>Spot the Outlier</span>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;">Score</div>
            <div style="font-family:'Limelight',cursive;font-size:26px;color:#14080e;line-height:1;">{score}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _strip_fig(data, clicked_index=None, revealed=False):
    d = data["data"]
    n = len(d)
    zscores = data["all_zscores"]
    outlier_idx = data["outlier_index"]

    rng = np.random.RandomState(42)
    jitter = rng.uniform(-0.12, 0.12, n)

    colours = []
    for i in range(n):
        if revealed:
            if i == outlier_idx:
                colours.append("#14080e")
            elif i == clicked_index and i != outlier_idx:
                colours.append("#c97c7c")
            else:
                colours.append("#acc196")
        else:
            if i == clicked_index:
                colours.append("#acc196")
            else:
                colours.append("#49475b")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(d),
        y=list(jitter),
        mode="markers",
        marker=dict(color=colours, size=10, opacity=0.85,
                    line=dict(color="#ffffff", width=0.8)),
        customdata=list(range(n)),
        hovertemplate="Value: %{x:.2f}<br>Point #%{customdata}<extra></extra>",
    ))

    if revealed:
        # Annotate outlier
        fig.add_annotation(
            x=d[outlier_idx],
            y=jitter[outlier_idx] + 0.18,
            text=f"Z={zscores[outlier_idx]:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#14080e",
            font=dict(family="Outfit", size=11, color="#14080e"),
            bgcolor="#e9eb9e",
            bordercolor="#acc196",
            borderwidth=1,
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=True, gridcolor="#e8e7e2", zeroline=True,
                   zerolinecolor="#d9d8d0", title=""),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False,
                   range=[-0.5, 0.5], title=""),
        height=260,
        showlegend=False,
        modebar=dict(bgcolor="rgba(0,0,0,0)", color="rgba(0,0,0,0)", activecolor="rgba(0,0,0,0)"),
    )
    return fig


def show():
    difficulty = st.session_state.get("difficulty", "easy")

    if st.session_state.get("round_data") is None:
        st.session_state.round_data = generator.generate_outlier_data(difficulty)
        st.session_state.round_submitted = False
        st.session_state.clicked_index = None

    data = st.session_state.round_data
    outlier_idx = data["outlier_index"]
    all_zscores = data["all_zscores"]
    clicked = st.session_state.get("clicked_index")

    _score_header()

    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:13px;font-weight:300;
                color:#799496;letter-spacing:0.06em;margin-bottom:12px;">
        Click on the point you think is the outlier, then hit Submit.
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("round_submitted", False):
        fig = _strip_fig(data, clicked_index=clicked, revealed=False)

        if _HAS_EVENTS:
            selected = plotly_events(fig, click_event=True, key=f"outlier_{st.session_state.round_number}")
            if selected:
                new_idx = selected[0].get("pointIndex", None)
                if new_idx is not None and new_idx != st.session_state.get("clicked_index"):
                    st.session_state.clicked_index = int(new_idx)
                    st.rerun()
        else:
            event = st.plotly_chart(
                fig,
                use_container_width=True,
                on_select="rerun",
                key=f"outlier_{st.session_state.round_number}",
                config={"displayModeBar": False},
            )
            if event and event.selection and event.selection.points:
                idx = event.selection.points[0].get("point_index")
                if idx is not None:
                    st.session_state.clicked_index = int(idx)
                    st.rerun()

        if clicked is not None:
            st.markdown(f"""
            <div style="font-family:'Outfit',sans-serif;font-size:13px;color:#49475b;
                        margin-top:8px;margin-bottom:12px;">
                Selected point #{clicked} — click Submit to confirm.
            </div>
            """, unsafe_allow_html=True)

        if st.button("Submit", key="outlier_submit", disabled=(clicked is None)):
            earned = scorer.score_outlier(clicked, outlier_idx, all_zscores)
            is_correct = (clicked == outlier_idx)
            st.session_state.score += earned
            st.session_state.rounds_data.append({
                "round": st.session_state.round_number,
                "score_earned": earned,
                "max_score": 150,
                "correct": is_correct,
            })
            st.session_state.last_earned = earned
            st.session_state.last_correct = is_correct
            st.session_state.round_submitted = True
            st.rerun()

    else:
        clicked = st.session_state.get("clicked_index")
        is_correct = st.session_state.get("last_correct", False)
        earned = st.session_state.get("last_earned", 0)

        fig = _strip_fig(data, clicked_index=clicked, revealed=True)
        if _HAS_EVENTS:
            plotly_events(fig, click_event=False, key=f"outlier_result_{st.session_state.round_number}")
        else:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        pick_z = all_zscores[clicked] if clicked is not None else 0.0
        true_z = data["outlier_zscore"]

        banner_bg = "#e8f5e4" if is_correct else ("#fff8e6" if earned == 75 else "#fdf0f0")
        banner_border = "#acc196" if is_correct else ("#e0a040" if earned == 75 else "#c97c7c")
        result_word = "Correct!" if is_correct else ("Partial Credit" if earned == 75 else "Missed")

        fb_text = fb_module.FEEDBACK.get(("outlier", is_correct), "")

        st.markdown(f"""
        <div style="
            background:{banner_bg};border:1px solid {banner_border};
            border-left:3px solid {banner_border};border-radius:2px;
            padding:16px 20px;margin-bottom:16px;
        ">
            <div style="font-family:'Outfit',sans-serif;font-size:10px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;
                        color:{'#3a7a35' if is_correct else '#a05252'};margin-bottom:8px;">
                {result_word}
            </div>
            <div style="display:flex;gap:24px;margin-bottom:10px;">
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Your Pick Z-score</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#14080e;">{pick_z:+.2f}</div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">True Outlier Z-score</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#49475b;">{true_z:+.2f}</div>
                </div>
                <div>
                    <div style="font-size:11px;color:#799496;font-weight:600;
                                letter-spacing:0.1em;text-transform:uppercase;">Points Earned</div>
                    <div style="font-family:'Limelight',cursive;font-size:22px;color:#14080e;">+{earned}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        learning_callout(fb_text)

        rn = st.session_state.round_number
        if rn >= 5:
            if st.button("See Results →", key="outlier_results"):
                st.session_state.game_complete = True
                st.session_state.page = "results"
                st.rerun()
        else:
            if st.button("Next Round →", key="outlier_next"):
                st.session_state.round_number += 1
                st.session_state.round_data = None
                st.session_state.round_submitted = False
                st.session_state.clicked_index = None
                st.rerun()
