# StatQuest

StatQuest is an interactive Python game for practicing core statistics concepts through visual reasoning. It was developed for **Statistics for Computer Science, Advanced** at the **Lucerne University of Applied Sciences and Arts**.

The project turns short statistics exercises into a browser-based mini-game. Players choose a difficulty level, complete five randomized rounds in one of three modes, receive immediate feedback, and can save their result to a local leaderboard. The goal is to connect statistical formulas with visible data patterns rather than treating statistics as a calculator-only task.

## Learning Goals

StatQuest supports the course goals of applying statistical methods with Python, interpreting statistical results, and communicating data-based conclusions clearly. It focuses on three concepts that are useful for later data analysis:

- **Pearson correlation**: estimate the strength and direction of a linear relationship from a scatter plot.
- **Distribution shape**: identify normal, skewed, bimodal, and uniform distributions from histograms.
- **Outlier detection**: find unusual observations using visual inspection and z-score feedback.

Each round gives immediate feedback showing the correct value or category, the points earned, and a short explanation of the relevant statistical idea. Randomized data generation keeps repeated play from becoming memorization.

## Game Modes

| Mode | Points/Round | Task |
|------|--------------|------|
| Guess the Correlation | 200 | Estimate Pearson's r from a scatter plot using a slider from -1 to 1. |
| Name That Distribution | 100 | Classify a histogram as normal, right-skewed, left-skewed, bimodal, or uniform. |
| Spot the Outlier | 150 | Click the point that appears most unusual in a strip plot. |

## Difficulty

| Difficulty | Data Points | Effect |
|------------|-------------|--------|
| Easy | 30 | Clearer, more distinct visual patterns. |
| Medium | 60 | Broader range of generated examples. |
| Hard | 100 | More subtle differences, especially for correlation estimates. |

## Implementation

StatQuest is built with Streamlit so the full experience can run as a Python application in the browser without a separate frontend framework.

- **Streamlit** handles routing, user input, session state, and layout.
- **NumPy** generates randomized datasets.
- **SciPy** computes Pearson correlation, skewness, and statistical values used for feedback.
- **Plotly** renders scatter plots, histograms, strip plots, and results charts.
- **JSON storage** keeps a local leaderboard with initials, score, mode, and difficulty.

The code is organized into view modules for the screens and game modes, plus shared logic modules for data generation, scoring, and educational feedback.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Project Report

A fuller description of the concept, statistical background, implementation, and learning value is available in `docs/StatQuest_Project_Description.pdf`.
