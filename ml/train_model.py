import sqlite3
import pandas as pd

from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------
# LOAD ML TRAINING DATA FROM DATABASE
# ---------------------------------------------------

connection = sqlite3.connect("family.db")

query = """
SELECT
    usage,
    budget,
    previous_plan,
    selected_plan
FROM ml_training_data
"""

data = pd.read_sql_query(query, connection)

connection.close()


print("ML Training Data:")
print(data)


# ---------------------------------------------------
# CHECK DATA
# ---------------------------------------------------

if len(data) < 2:

    print("\nNot enough data to train the ML model.")
    print("Use the AI Recommendation page a few more times.")

else:

    # ------------------------------------------------
    # CONVERT PREVIOUS PLAN INTO NUMERIC VALUE
    # ------------------------------------------------

    plan_mapping = {
        "₹199 Plan": 199,
        "₹299 Plan": 299,
        "₹349 Plan": 349,
        "₹399 Plan": 399
    }

    data["previous_plan"] = (
        data["previous_plan"]
        .map(plan_mapping)
        .fillna(0)
    )


    # ------------------------------------------------
    # FEATURES
    # ------------------------------------------------

    X = data[
        [
            "usage",
            "budget",
            "previous_plan"
        ]
    ]


    # ------------------------------------------------
    # TARGET
    # ------------------------------------------------

    y = data["selected_plan"]


    # ------------------------------------------------
    # CREATE DECISION TREE
    # ------------------------------------------------

    model = DecisionTreeClassifier(
        random_state=42
    )


    # ------------------------------------------------
    # TRAIN MODEL
    # ------------------------------------------------

    model.fit(X, y)


    print("\nML Model trained successfully!")


    # ------------------------------------------------
    # TEST PREDICTION
    # ------------------------------------------------

    test_data = pd.DataFrame(
        [[2.0, 300, 299]],
        columns=[
            "usage",
            "budget",
            "previous_plan"
        ]
    )


    prediction = model.predict(test_data)


    print("\nTest Input:")
    print("Daily Usage: 2 GB")
    print("Budget: ₹300")
    print("Previous Plan: ₹299 Plan")


    print("\nML Model Prediction:")
    print(prediction[0])