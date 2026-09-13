import sqlite3


def get_recharge_history():

    connection = sqlite3.connect("family.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT member_name, mobile, plan, amount, recharge_date
        FROM recharge_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history


def get_most_used_plans():

    history = get_recharge_history()

    plan_count = {}

    for item in history:

        member_name = item[0]
        plan = item[2]

        if member_name not in plan_count:
            plan_count[member_name] = {}

        if plan not in plan_count[member_name]:
            plan_count[member_name][plan] = 0

        plan_count[member_name][plan] += 1

    most_used = {}

    for member in plan_count:

        most_used[member] = max(
            plan_count[member],
            key=plan_count[member].get
        )

    return most_used


if __name__ == "__main__":

    most_used = get_most_used_plans()

    print("Most Used Recharge Plans")
    print("------------------------")

    if not most_used:

        print("No recharge history found.")

    else:

        for member, plan in most_used.items():

            print(
                f"{member} → {plan}"
            )