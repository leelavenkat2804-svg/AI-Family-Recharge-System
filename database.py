import sqlite3


# ---------------------------------------------------
# CREATE DATABASE
# ---------------------------------------------------

def create_database():

    connection = sqlite3.connect("family.db")

    cursor = connection.cursor()


    # ---------------------------------------------------
    # FAMILY MEMBERS TABLE
    # ---------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL
        )
    """)


    # ---------------------------------------------------
    # RECHARGE HISTORY TABLE
    # ---------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recharge_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            plan TEXT NOT NULL,
            amount INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            recharge_date TEXT NOT NULL
        )
    """)


    # ---------------------------------------------------
    # ML TRAINING DATA TABLE
    # ---------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ml_training_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usage REAL NOT NULL,
            budget INTEGER NOT NULL,
            previous_plan TEXT,
            selected_plan TEXT NOT NULL
        )
    """)


    connection.commit()
    connection.close()


# ---------------------------------------------------
# CREATE TABLES
# ---------------------------------------------------

create_database()


# ---------------------------------------------------
# RESET DEMO ML TRAINING DATA
# ---------------------------------------------------

connection = sqlite3.connect("family.db")

cursor = connection.cursor()

cursor.execute("""
    DELETE FROM ml_training_data
""")


# ---------------------------------------------------
# IMPROVED DEMO TRAINING DATA
# ---------------------------------------------------
#
# usage  = daily data usage in GB
# budget = maximum recharge budget
# previous_plan = previous recharge plan
# selected_plan = suitable plan
#
# NOTE:
# This is synthetic training data for our project demo.
# It is not real telecom customer data.
# ---------------------------------------------------

training_data = [

    # -----------------------------------------------
    # ₹199 PLAN
    # Lower usage + lower budget
    # -----------------------------------------------

    (0.8, 199, "₹199 Plan", "₹199 Plan"),
    (1.0, 200, "₹199 Plan", "₹199 Plan"),
    (1.2, 220, "₹199 Plan", "₹199 Plan"),
    (1.4, 230, "₹199 Plan", "₹199 Plan"),
    (1.5, 250, "₹199 Plan", "₹199 Plan"),

    (0.9, 199, None, "₹199 Plan"),
    (1.1, 210, None, "₹199 Plan"),
    (1.3, 230, None, "₹199 Plan"),


    # -----------------------------------------------
    # ₹299 PLAN
    # Medium usage + medium budget
    # -----------------------------------------------

    (1.6, 280, "₹199 Plan", "₹299 Plan"),
    (1.8, 299, "₹199 Plan", "₹299 Plan"),
    (2.0, 300, "₹199 Plan", "₹299 Plan"),
    (2.0, 320, "₹199 Plan", "₹299 Plan"),
    (2.1, 330, "₹299 Plan", "₹299 Plan"),
    (2.2, 299, "₹199 Plan", "₹299 Plan"),
    (2.3, 320, "₹299 Plan", "₹299 Plan"),


    # -----------------------------------------------
    # ₹349 PLAN
    # Higher usage + higher budget
    # -----------------------------------------------

    (2.4, 349, "₹299 Plan", "₹349 Plan"),
    (2.5, 350, "₹299 Plan", "₹349 Plan"),
    (2.6, 360, "₹299 Plan", "₹349 Plan"),
    (2.7, 370, "₹299 Plan", "₹349 Plan"),
    (2.8, 349, "₹299 Plan", "₹349 Plan"),
    (2.9, 380, "₹349 Plan", "₹349 Plan"),


    # -----------------------------------------------
    # ₹399 PLAN
    # High usage + high budget
    # -----------------------------------------------

    (3.0, 399, "₹349 Plan", "₹399 Plan"),
    (3.1, 400, "₹349 Plan", "₹399 Plan"),
    (3.2, 399, "₹349 Plan", "₹399 Plan"),
    (3.3, 420, "₹349 Plan", "₹399 Plan"),
    (3.4, 430, "₹349 Plan", "₹399 Plan"),
    (3.5, 450, "₹399 Plan", "₹399 Plan"),
    (3.8, 450, "₹399 Plan", "₹399 Plan"),
    (4.0, 500, "₹399 Plan", "₹399 Plan")
]


# ---------------------------------------------------
# INSERT TRAINING DATA
# ---------------------------------------------------

cursor.executemany("""
    INSERT INTO ml_training_data
    (
        usage,
        budget,
        previous_plan,
        selected_plan
    )
    VALUES (?, ?, ?, ?)
""", training_data)


connection.commit()
connection.close()


# ---------------------------------------------------
# SUCCESS MESSAGE
# ---------------------------------------------------

print("Database created successfully!")

print(
    f"ML training data added successfully: {len(training_data)} rows"
)