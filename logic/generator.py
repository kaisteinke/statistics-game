import numpy as np
from scipy import stats

_DIFFICULTY_N = {"easy": 30, "medium": 60, "hard": 100}

_EASY_R = [0.3, 0.5, 0.7, -0.4, -0.6]
_MEDIUM_R = [r / 10 for r in range(-9, 10) if r != 0]


def generate_correlation_data(difficulty):
    n = _DIFFICULTY_N[difficulty]

    if difficulty == "easy":
        target_r = float(np.random.choice(_EASY_R))
    elif difficulty == "medium":
        target_r = float(np.random.choice(_MEDIUM_R))
    else:  # hard — two close r values, player must discriminate
        anchor = float(np.random.choice([r / 10 for r in range(-8, 9) if r != 0]))
        candidates = [anchor + d for d in (0.1, -0.1, 0.15, -0.15) if -1.0 < anchor + d < 1.0]
        target_r = float(np.random.choice(candidates)) if candidates else anchor

    cov = [[1.0, target_r], [target_r, 1.0]]
    xy = np.random.multivariate_normal([0, 0], cov, size=n)
    actual_r, _ = stats.pearsonr(xy[:, 0], xy[:, 1])

    return {
        "x": xy[:, 0].tolist(),
        "y": xy[:, 1].tolist(),
        "target_r": target_r,
        "actual_r": float(actual_r),
    }


def generate_distribution_data(difficulty):
    n = _DIFFICULTY_N[difficulty]
    dist_type = np.random.choice(
        ["normal", "right_skewed", "left_skewed", "bimodal", "uniform"]
    )

    for _ in range(10):
        data = _sample(dist_type, n)
        skewness = float(stats.skew(data))
        if dist_type == "normal" and abs(skewness) > 0.5:
            continue
        break

    return {
        "data": data.tolist(),
        "distribution_type": dist_type,
        "skewness": skewness,
    }


def _sample(dist_type, n):
    if dist_type == "normal":
        return np.random.normal(0, 1, n)
    if dist_type == "right_skewed":
        return np.random.lognormal(0, 0.6, n)
    if dist_type == "left_skewed":
        return -np.random.lognormal(0, 0.6, n)
    if dist_type == "bimodal":
        return np.concatenate(
            [np.random.normal(-2, 0.8, n // 2), np.random.normal(2, 0.8, n // 2)]
        )
    # uniform
    return np.random.uniform(-3, 3, n)


def generate_outlier_data(difficulty):
    n = _DIFFICULTY_N[difficulty]
    base = np.random.normal(0, 1, n)

    # pick outlier z-score magnitude and sign
    outlier_z = float(np.random.uniform(2.8, 4.0)) * float(np.random.choice([-1, 1]))
    outlier_index = int(np.random.randint(0, n))
    base[outlier_index] = outlier_z  # inject as a raw value (mean=0, std=1 base)

    mean = float(np.mean(base))
    std = float(np.std(base))
    all_zscores = ((base - mean) / std) if std > 0 else base

    return {
        "data": base.tolist(),
        "outlier_index": outlier_index,
        "outlier_zscore": float(all_zscores[outlier_index]),
        "all_zscores": all_zscores.tolist(),
    }
