FEEDBACK = {
    ("correlation", "Excellent"): (
        "Pearson's r measures linear association between -1 and +1. "
        "Values above 0.7 are considered strong in most social science contexts."
    ),
    ("correlation", "Good"): (
        "Correlation does not imply causation — a strong r between two variables "
        "may be explained by a hidden third variable (a confound)."
    ),
    ("correlation", "Close"): (
        "Pearson's r is sensitive to outliers. Even one extreme point can shift r "
        "by 0.2 or more in small samples."
    ),
    ("correlation", "Off"): (
        "A quick heuristic: if the scatter plot looks like a football, r ≈ 0. "
        "A thin diagonal cigar shape means r is close to ±1."
    ),
    ("distribution", True): (
        "The Central Limit Theorem states that means of large samples approach normality "
        "regardless of the original distribution — the foundation of much of inferential statistics."
    ),
    ("distribution", False): (
        "Skewness measures asymmetry: positive skew means a long right tail (e.g. income), "
        "negative skew means a long left tail (e.g. age at retirement)."
    ),
    ("outlier", True): (
        "Z-scores standardise values to units of standard deviation. A Z-score above ±2.5 "
        "occurs in less than 1.2% of a normal distribution — a reliable outlier threshold."
    ),
    ("outlier", False): (
        "The IQR method flags points outside Q1 - 1.5×IQR or Q3 + 1.5×IQR. "
        "It is more robust than Z-scores for skewed or non-normal data."
    ),
}
