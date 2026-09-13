from flask import Flask, render_template, request, session
import sqlite3
from datetime import datetime

from ml.history_analysis import get_most_used_plans
from ml.ml_predictor import predict_plan


app = Flask(__name__)

app.secret_key = "family-recharge-secret-key"


# ---------------------------------------------------
# HOME
# ---------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------
# FAMILY MEMBERS
# ---------------------------------------------------

@app.route("/members")
def members():
    return render_template("members.html")


@app.route("/add-member", methods=["POST"])
def add_member():

    name = request.form["name"]
    mobile = request.form["mobile"]

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO members (name, mobile) VALUES (?, ?)",
        (name, mobile)
    )

    connection.commit()
    connection.close()

    return f"Member {name} added successfully!"


@app.route("/members-list")
def members_list():

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, mobile FROM members"
    )

    members = cursor.fetchall()

    connection.close()

    return render_template(
        "members_list.html",
        members=members
    )


# ---------------------------------------------------
# RECHARGE PLANS
# ---------------------------------------------------

@app.route("/plans")
def plans():

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, mobile FROM members"
    )

    members = cursor.fetchall()

    connection.close()

    return render_template(
        "plans.html",
        members=members
    )


# ---------------------------------------------------
# ADD TO CART
# ---------------------------------------------------

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():

    member_id = request.form["member_id"]
    plan = request.form["plan"]
    price = int(request.form["price"])

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name, mobile FROM members WHERE id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    connection.close()

    if member is None:
        return "Family member not found!"

    item = {
        "name": member[0],
        "mobile": member[1],
        "plan": plan,
        "price": price
    }

    cart = session.get("cart", [])

    cart.append(item)

    session["cart"] = cart

    return render_template(
        "cart.html",
        cart=cart,
        total=sum(item["price"] for item in cart)
    )


# ---------------------------------------------------
# VIEW CART
# ---------------------------------------------------

@app.route("/cart")
def cart():

    cart = session.get("cart", [])

    total = sum(
        item["price"] for item in cart
    )

    return render_template(
        "cart.html",
        cart=cart,
        total=total
    )


# ---------------------------------------------------
# PAYMENT
# ---------------------------------------------------

@app.route("/payment")
def payment():

    cart = session.get("cart", [])

    if not cart:
        return "Your cart is empty!"

    total = sum(
        item["price"] for item in cart
    )

    return render_template(
        "payment.html",
        cart=cart,
        total=total
    )


# ---------------------------------------------------
# PROCESS PAYMENT
# ---------------------------------------------------

@app.route("/process-payment", methods=["POST"])
def process_payment():

    cart = session.get("cart", [])

    if not cart:
        return "Your cart is empty!"

    payment_method = request.form["payment_method"]

    total = sum(
        item["price"] for item in cart
    )

    recharge_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    for item in cart:

        cursor.execute("""
            INSERT INTO recharge_history
            (
                member_name,
                mobile,
                plan,
                amount,
                payment_method,
                recharge_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            item["name"],
            item["mobile"],
            item["plan"],
            item["price"],
            payment_method,
            recharge_date
        ))

    connection.commit()
    connection.close()

    session["cart"] = []

    return render_template(
        "payment_success.html",
        cart=cart,
        total=total,
        payment_method=payment_method
    )


# ---------------------------------------------------
# RECHARGE HISTORY
# ---------------------------------------------------

@app.route("/history")
def history():

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            member_name,
            mobile,
            plan,
            amount,
            payment_method,
            recharge_date
        FROM recharge_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return render_template(
        "history.html",
        history=history
    )


# ---------------------------------------------------
# AI SMART RECOMMENDATION
# ---------------------------------------------------

@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():

    recommended_plan = None
    usage = None
    budget = None
    previous_plan = None
    selected_member = None
    members = []
    saved_plan = None

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, mobile FROM members"
    )

    members = cursor.fetchall()

    connection.close()


    # =================================================
    # SAVE ACTUAL USER SELECTION
    # =================================================

    if request.method == "POST" and request.form.get("actual_plan"):

        member_id = request.form.get("member_id")

        usage = float(
            request.form.get("usage")
        )

        budget = int(
            request.form.get("budget")
        )

        actual_plan = request.form.get(
            "actual_plan"
        )


        connection = sqlite3.connect("family.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, mobile
            FROM members
            WHERE id = ?
        """, (member_id,))

        member = cursor.fetchone()

        if member is None:

            connection.close()

            return "Family member not found!"

        selected_member = member


        cursor.execute("""
            SELECT plan
            FROM recharge_history
            WHERE member_name = ?
            ORDER BY id DESC
            LIMIT 1
        """, (member[0],))

        result = cursor.fetchone()

        connection.close()


        if result:
            previous_plan = result[0]


        # Save actual user selection
        connection = sqlite3.connect(
            "family.db"
        )

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO ml_training_data
            (
                usage,
                budget,
                previous_plan,
                selected_plan
            )
            VALUES (?, ?, ?, ?)
        """, (
            usage,
            budget,
            previous_plan,
            actual_plan
        ))

        connection.commit()
        connection.close()


        saved_plan = actual_plan


        # Get updated recommendation
        recommended_plan = predict_plan(
            usage=usage,
            budget=budget,
            previous_plan=previous_plan
        )


    # =================================================
    # GET AI RECOMMENDATION
    # =================================================

    elif request.method == "POST":

        member_id = request.form["member_id"]

        usage = float(
            request.form["usage"]
        )

        budget = int(
            request.form["budget"]
        )


        connection = sqlite3.connect("family.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, mobile
            FROM members
            WHERE id = ?
        """, (member_id,))

        member = cursor.fetchone()

        if member is None:

            connection.close()

            return "Family member not found!"

        selected_member = member


        cursor.execute("""
            SELECT plan
            FROM recharge_history
            WHERE member_name = ?
            ORDER BY id DESC
            LIMIT 1
        """, (member[0],))

        result = cursor.fetchone()

        connection.close()


        if result:
            previous_plan = result[0]


        recommended_plan = predict_plan(
            usage=usage,
            budget=budget,
            previous_plan=previous_plan
        )


    return render_template(
        "recommendations.html",
        members=members,
        selected_member=selected_member,
        usage=usage,
        budget=budget,
        previous_plan=previous_plan,
        recommended_plan=recommended_plan,
        saved_plan=saved_plan
    )


# ---------------------------------------------------
# AI HISTORY ANALYSIS
# ---------------------------------------------------

@app.route("/ai-history")
def ai_history():

    most_used = get_most_used_plans()

    return render_template(
        "ai_history.html",
        most_used=most_used
    )


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

@app.route("/dashboard")
def dashboard():

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()


    # Total family members

    cursor.execute("""
        SELECT COUNT(*)
        FROM members
    """)

    total_members = cursor.fetchone()[0]


    # Total recharges

    cursor.execute("""
        SELECT COUNT(*)
        FROM recharge_history
    """)

    total_recharges = cursor.fetchone()[0]


    # Total spending

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM recharge_history
    """)

    total_spent = cursor.fetchone()[0]


    # Most used plan

    cursor.execute("""
        SELECT plan, COUNT(*) AS count
        FROM recharge_history
        GROUP BY plan
        ORDER BY count DESC
        LIMIT 1
    """)

    result = cursor.fetchone()


    if result:

        most_used_plan = result[0]

    else:

        most_used_plan = "No data yet"


    connection.close()


    return render_template(
        "dashboard.html",
        total_members=total_members,
        total_recharges=total_recharges,
        total_spent=total_spent,
        most_used_plan=most_used_plan
    )


# ---------------------------------------------------
# CLEAR CART
# ---------------------------------------------------

@app.route("/clear-cart")
def clear_cart():

    session["cart"] = []

    return render_template(
        "cart.html",
        cart=[],
        total=0
    )


# ---------------------------------------------------
# START FLASK
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)