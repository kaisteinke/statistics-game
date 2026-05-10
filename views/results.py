import json
import os
import streamlit as st
import plotly.graph_objects as go

from views.icon_utils import svg_icon_html


_LEADERBOARD_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "leaderboard.json")

_PERFORMANCE = [
    (900, "Stats Oracle"),
    (700, "Correlation Wizard"),
    (500, "Distribution Detective"),
    (300, "Aspiring Analyst"),
    (0,   "Stats Padawan"),
]

_MODE_LABELS = {
    "game_correlation": "Correlation",
    "game_distribution": "Distribution",
    "game_outlier": "Outlier",
}


def _load_leaderboard():
    try:
        with open(_LEADERBOARD_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_leaderboard(entries):
    with open(_LEADERBOARD_PATH, "w") as f:
        json.dump(entries, f, indent=2)


def _performance_label(score):
    for threshold, label in _PERFORMANCE:
        if score >= threshold:
            return label
    return "Stats Padawan"


def _rounds_chart(rounds_data):
    rounds = [r["round"] for r in rounds_data]
    scores = [r["score_earned"] for r in rounds_data]
    colours = ["#acc196" if r["correct"] else "#49475b" for r in rounds_data]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[f"Round {r}" for r in rounds],
        y=scores,
        marker=dict(color=colours, line=dict(color="#ffffff", width=1)),
        text=[f"+{s}" for s in scores],
        textposition="outside",
        textfont=dict(family="Outfit", size=12, color="#49475b"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False, zeroline=False, title="",
                   tickfont=dict(family="Outfit", size=12, color="#799496")),
        yaxis=dict(showgrid=True, gridcolor="#e8e7e2", zeroline=False, title="Points"),
        height=260,
        showlegend=False,
    )
    return fig


def show():
    score = st.session_state.get("score", 0)
    rounds_data = st.session_state.get("rounds_data", [])
    mode_key = st.session_state.get("current_mode", "")
    difficulty = st.session_state.get("difficulty", "easy").capitalize()
    mode_label = _MODE_LABELS.get(mode_key, mode_key)

    perf_label = _performance_label(score)
    correct_count = sum(1 for r in rounds_data if r.get("correct"))
    avg_score = round(score / max(len(rounds_data), 1))

    # Hero score block
    st.markdown(f"""
    <div style="
        background:#e9eb9e;
        border:1px solid #acc196;
        border-radius:4px;
        padding:40px 32px;
        text-align:center;
        margin-bottom:32px;
        position:relative;overflow:hidden;
    ">
        <div style="
            position:absolute;inset:0;
            background:
                repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(172,193,150,0.25) 39px,rgba(172,193,150,0.25) 40px),
                repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(172,193,150,0.25) 39px,rgba(172,193,150,0.25) 40px);
        "></div>
        <div style="position:relative;">
            <div style="font-family:'Outfit',sans-serif;font-size:10px;font-weight:600;
                        letter-spacing:0.3em;text-transform:uppercase;color:#49475b;margin-bottom:12px;">
                Game Complete · {mode_label} · {difficulty}
            </div>
            <div style="font-family:'Limelight',cursive;font-size:72px;color:#14080e;line-height:1;">
                {score}
            </div>
            <div style="font-family:'Outfit',sans-serif;font-size:13px;font-weight:300;
                        letter-spacing:0.2em;text-transform:uppercase;color:#49475b;margin-top:8px;">
                {perf_label}
            </div>
            <div style="display:flex;align-items:center;justify-content:center;
                        gap:12px;margin-top:20px;">
                <div style="width:60px;height:1px;background:#acc196;"></div>
                <div style="width:5px;height:5px;background:#49475b;transform:rotate(45deg);"></div>
                <div style="width:60px;height:1px;background:#acc196;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats summary row
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-bottom:24px;">
        <div style="flex:1;background:#ffffff;border:1px solid #d9d8d0;border-radius:4px;
                    padding:16px;text-align:center;">
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;margin-bottom:4px;">
                Correct Rounds
            </div>
            <div style="font-family:'Limelight',cursive;font-size:28px;color:#14080e;">{correct_count} / {len(rounds_data)}</div>
        </div>
        <div style="flex:1;background:#ffffff;border:1px solid #d9d8d0;border-radius:4px;
                    padding:16px;text-align:center;">
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;margin-bottom:4px;">
                Avg per Round
            </div>
            <div style="font-family:'Limelight',cursive;font-size:28px;color:#14080e;">{avg_score}</div>
        </div>
        <div style="flex:1;background:#ffffff;border:1px solid #d9d8d0;border-radius:4px;
                    padding:16px;text-align:center;">
            <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:0.15em;text-transform:uppercase;color:#799496;margin-bottom:4px;">
                Difficulty
            </div>
            <div style="font-family:'Limelight',cursive;font-size:28px;color:#14080e;">{difficulty}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Per-round chart
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                letter-spacing:0.18em;text-transform:uppercase;color:#799496;
                display:flex;align-items:center;gap:14px;margin-bottom:12px;">
        Round by Round
        <div style="flex:1;height:1px;background:linear-gradient(to right,#acc196,transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    if rounds_data:
        st.plotly_chart(_rounds_chart(rounds_data), use_container_width=True,
                        config={"displayModeBar": False})

        st.markdown("""
        <div style="display:flex;gap:16px;margin-bottom:24px;">
            <div style="display:flex;align-items:center;gap:6px;">
                <div style="width:12px;height:12px;background:#acc196;border-radius:2px;"></div>
                <span style="font-family:'Outfit',sans-serif;font-size:12px;color:#799496;">Good answer</span>
            </div>
            <div style="display:flex;align-items:center;gap:6px;">
                <div style="width:12px;height:12px;background:#49475b;border-radius:2px;"></div>
                <span style="font-family:'Outfit',sans-serif;font-size:12px;color:#799496;">Needs work</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again", key="res_again"):
            for key in ["score", "round_number", "rounds_data", "game_complete", "round_data",
                        "round_submitted", "clicked_index", "last_guess", "last_grade",
                        "last_earned", "last_answer", "last_correct", "current_mode"]:
                st.session_state[key] = {
                    "score": 0, "round_number": 1, "rounds_data": [], "game_complete": False,
                    "round_data": None, "round_submitted": False, "clicked_index": None,
                    "last_guess": 0.0, "last_grade": "", "last_earned": 0,
                    "last_answer": "", "last_correct": False, "current_mode": "",
                }.get(key)
            st.session_state.page = "home"
            st.rerun()

    with col2:
        if st.button("Try Another Mode", key="res_mode"):
            st.session_state.score = 0
            st.session_state.round_number = 1
            st.session_state.rounds_data = []
            st.session_state.game_complete = False
            st.session_state.round_data = None
            st.session_state.round_submitted = False
            st.session_state.clicked_index = None
            st.session_state.page = "mode_select"
            st.rerun()

    # Leaderboard section
    st.markdown("""
    <div style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:600;
                letter-spacing:0.18em;text-transform:uppercase;color:#799496;
                display:flex;align-items:center;gap:14px;margin-top:32px;margin-bottom:16px;">
        Leaderboard
        <div style="flex:1;height:1px;background:linear-gradient(to right,#acc196,transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("score_saved", False):
        initials_col, btn_col = st.columns([3, 1])
        with initials_col:
            initials = st.text_input(
                "Your initials (3 chars)",
                max_chars=3,
                placeholder="e.g. KAI",
                key="lb_initials",
            )
        with btn_col:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Save Score", key="lb_save"):
                if initials.strip():
                    entries = _load_leaderboard()
                    entries.append({
                        "initials": initials.strip().upper(),
                        "score": score,
                        "mode": mode_label,
                        "difficulty": difficulty,
                    })
                    _save_leaderboard(entries)
                    st.session_state.score_saved = True
                    st.rerun()

    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;font-family:'Outfit',sans-serif;
                    font-size:12px;color:#3a7a35;margin-bottom:12px;">
            """ + svg_icon_html("check.svg", size=16, alt="Score saved") + """
            <span>Score saved!</span>
        </div>
        """, unsafe_allow_html=True)

    # Top 5 leaderboard
    entries = _load_leaderboard()
    if entries:
        top5 = sorted(entries, key=lambda e: e["score"], reverse=True)[:5]
        header = """
        <div style="display:flex;background:#f5f4ee;border:1px solid #d9d8d0;
                    border-bottom:none;border-radius:4px 4px 0 0;padding:8px 16px;">
            <div style="width:40px;font-size:10px;font-weight:600;letter-spacing:0.15em;
                        text-transform:uppercase;color:#799496;">#</div>
            <div style="flex:1;font-size:10px;font-weight:600;letter-spacing:0.15em;
                        text-transform:uppercase;color:#799496;">Player</div>
            <div style="width:80px;font-size:10px;font-weight:600;letter-spacing:0.15em;
                        text-transform:uppercase;color:#799496;">Score</div>
            <div style="width:120px;font-size:10px;font-weight:600;letter-spacing:0.15em;
                        text-transform:uppercase;color:#799496;">Mode</div>
            <div style="width:80px;font-size:10px;font-weight:600;letter-spacing:0.15em;
                        text-transform:uppercase;color:#799496;">Level</div>
        </div>"""
        rows = ""
        medals = [
            svg_icon_html("medal-gold.svg", size=18, alt="1st place"),
            svg_icon_html("medal-silver.svg", size=18, alt="2nd place"),
            svg_icon_html("medal-bronze.svg", size=18, alt="3rd place"),
            '<span style="display:inline-block;width:18px;text-align:center;">4.</span>',
            '<span style="display:inline-block;width:18px;text-align:center;">5.</span>',
        ]
        for i, e in enumerate(top5, 1):
            bg = "#ffffff" if i % 2 == 0 else "#fafaf8"
            radius = "0 0 4px 4px" if i == len(top5) else "0"
            rows += f"""
        <div style="display:flex;align-items:center;background:{bg};
                    border:1px solid #d9d8d0;border-top:none;
                    border-radius:{radius};padding:10px 16px;">
            <div style="width:40px;font-size:13px;color:#799496;display:flex;align-items:center;">{medals[i-1]}</div>
            <div style="flex:1;font-family:'Limelight',cursive;font-size:16px;color:#14080e;">
                {e.get('initials','???')}</div>
            <div style="width:80px;font-family:'Limelight',cursive;font-size:16px;color:#14080e;">
                {e.get('score',0)}</div>
            <div style="width:120px;font-size:12px;color:#799496;">{e.get('mode','')}</div>
            <div style="width:80px;font-size:12px;color:#799496;">{e.get('difficulty','')}</div>
        </div>"""
        st.markdown(header + rows, unsafe_allow_html=True)
