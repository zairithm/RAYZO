def compute_triage(probabilities):
    weights = {
        "Pneumonia": 0.5,
        "Effusion": 0.3,
        "Atelectasis": 0.2,
        "No Finding": -0.5
    }

    score = sum(probabilities[label] * weights[label] for label in probabilities)

    if score > 0.6:
        level = "HIGH"
    elif score > 0.3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return round(score, 3), level