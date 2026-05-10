def score_correlation(guess, actual_r):
    diff = abs(guess - actual_r)
    score = int(max(0, 200 - diff * 1000))
    if diff < 0.05:
        grade = "Excellent"
    elif diff < 0.15:
        grade = "Good"
    elif diff < 0.25:
        grade = "Close"
    else:
        grade = "Off"
    return score, grade


def score_distribution(guess, correct):
    return 100 if guess == correct else 0


def score_outlier(clicked_index, outlier_index, all_zscores):
    if clicked_index == outlier_index:
        return 150
    if abs(all_zscores[clicked_index]) > 2.0:
        return 75
    return 0
