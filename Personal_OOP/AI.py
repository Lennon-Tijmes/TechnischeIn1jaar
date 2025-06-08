from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np

# Simulate some training data
# for extra info, sit_seconds, stand_seconds, shock_count

X = [
    [0, 0, 0], # No information

    [60, 0, 5],  # sitting without standing up

    [60, 20, 1], # This is good

    [20, 10, 0],  # Balanced

    [20, 0, 0], # Just sitting

    [30, 20, 7],  # Too many shocks

    [40, 30, 2], # not balanced

    [10, 0, 20], # Holy smackeroni I smell burnt toast
]

# It is ordered with the given training data.
y = [
    "not_started",
    "too_much_sitting",
    "balanced",
    "short_balanced",
    "idle_sitting",
    "too_many_shocks",
    "slightly_imbalanced",
    "danger",
]

# Making sure you can get unique messages
label_messages = {
    "not_started": [
        "Go sit before asking.",
        "Go sit then work and drink tea.",
        "Standing while working, don't do that."
    ],
    "too_much_sitting" : [
        "Try to stand more.",
        "Why aren't you standing more?",
        "Remember the leg!"
    ],
    "balanced" : [
        "Great job",
        "I am proud of you!"
    ],
    "short_balanced" : [
        "Small session, great success!",
        "food break?"
    ],
    "idle_sitting" : [
        "Stretch your legs!",
        "Could use a friendly shock!",
        "I would suggest to walk around."
    ],
    "too_many_shocks" : [
        "Maybe dont zap too much.",
        "Are you okay? Go stand please."
    ],
    "slightly_imbalanced" : [
        "I suggest to do something else."
    ],
    "danger" : [
        "I smell burnt toast..",
        "Maybe don't use this function",
        "Should I call 112?"
    ]
}

model = RandomForestClassifier()
model.fit(X, y)

with open("AI_model.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "label_messages": label_messages
    }, f)

print("Model being trained and saved")