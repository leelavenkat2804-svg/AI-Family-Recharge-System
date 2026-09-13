def recommend_plan(usage, budget, previous_plan=None):
    """
    Smart recharge recommendation based on:
    - Daily data usage
    - Budget
    - Previous recharge plan
    """

    # Available recharge plans
    plans = [
        {
            "name": "₹199 Plan",
            "price": 199,
            "data": 1.5
        },
        {
            "name": "₹299 Plan",
            "price": 299,
            "data": 2
        },
        {
            "name": "₹349 Plan",
            "price": 349,
            "data": 2.5
        },
        {
            "name": "₹399 Plan",
            "price": 399,
            "data": 3
        }
    ]

    best_plan = None
    best_score = -1


    # Compare every available plan
    for plan in plans:

        # Skip plans above the user's budget
        if plan["price"] > budget:
            continue


        score = 0


        # -----------------------------------------
        # 1. DATA USAGE SCORE
        # -----------------------------------------

        if plan["data"] >= usage:

            score += 50

        else:

            score -= 30


        # -----------------------------------------
        # 2. BUDGET SCORE
        # -----------------------------------------

        remaining_budget = budget - plan["price"]

        if remaining_budget >= 0:

            score += 20


        # -----------------------------------------
        # 3. PREVIOUS PLAN SCORE
        # -----------------------------------------

        if previous_plan == plan["name"]:

            score += 30


        # -----------------------------------------
        # SELECT BEST PLAN
        # -----------------------------------------

        if score > best_score:

            best_score = score
            best_plan = plan["name"]


    # No suitable plan
    if best_plan is None:

        return "No suitable plan found"


    return best_plan


# ---------------------------------------------------
# TEST THE AI RECOMMENDATION
# ---------------------------------------------------

if __name__ == "__main__":

    usage = 2

    budget = 300

    previous_plan = "₹299 Plan"


    recommendation = recommend_plan(
        usage,
        budget,
        previous_plan
    )


    print("Daily Usage:", usage, "GB")

    print("Budget: ₹", budget)

    print("Previous Plan:", previous_plan)

    print("Recommended Plan:", recommendation)