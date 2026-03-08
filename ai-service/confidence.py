import numpy as np

def compute_confidence(probabilities):

    probs = np.array(list(probabilities.values()))

    # Highest predicted disease probability
    max_prob = np.max(probs)

    # Second highest
    sorted_probs = np.sort(probs)
    second_max = sorted_probs[-2]

    # Margin between top predictions
    margin = max_prob - second_max

    # Confidence score
    certainty = 0.7 * max_prob + 0.3 * margin

    if certainty > 0.7:
        level = "Very High"
    elif certainty > 0.5:
        level = "High"
    elif certainty > 0.3:
        level = "Moderate"
    else:
        level = "Low"

    return round(float(certainty),3), level, round(float(max_prob),3)