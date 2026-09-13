import sqlite3
import pandas as pd

from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------
# LOAD TRAINING DATA
# ---------------------------------------------------

def load_training_data():

    connection = sqlite3.connect("family.db")

    query = """
    SELECT
        usage,
        budget,
        previous_plan,
        selected_plan
    FROM ml_training_data
    """

    data = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return data


# ---------------------------------------------------
# TRAIN ML MODEL
# ---------------------------------------------------

def train_model():

    data = load_training_data()

    if len(data) < 2:

        return None


    # Convert plan names into numbers

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


    # Features

    X = data[
        [
            "usage",
            "budget",
            "previous_plan"
        ]
    ]


    # Target

    y = data["selected_plan"]


    # Create model

    model = DecisionTreeClassifier(
        random_state=42
    )


    # Train model

    model.fit(X, y)


    return model


# ---------------------------------------------------
# PREDICT RECHARGE PLAN
# ---------------------------------------------------

def predict_plan(
    usage,
    budget,
    previous_plan=None
):

    model = train_model()


    if model is None:

        return "Not enough ML training data"


    # Convert previous plan

    plan_mapping = {
        "₹199 Plan": 199,
        "₹299 Plan": 299,
        "₹349 Plan": 349,
        "₹399 Plan": 399
    }


    previous_plan_number = plan_mapping.get(
        previous_plan,
        0
    )


    # Create prediction input

    input_data = pd.DataFrame(
        [[
            usage,
            budget,
            previous_plan_number
        ]],
        columns=[
            "usage",
            "budget",
            "previous_plan"
        ]
    )


    # Make prediction

    prediction = model.predict(
        input_data
    )


    return prediction[0]


# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    result = predict_plan(
        usage=2.0,
        budget=300,
        previous_plan="₹299 Plan"
    )

    print("ML Prediction:")
    print(result)