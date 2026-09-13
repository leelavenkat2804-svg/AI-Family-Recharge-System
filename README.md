## 🚀 Live Demo

[Open AI Family Recharge System](https://ai-family-recharge-system.onrender.com)
# 🤖 AI Family Recharge System

A web-based family mobile recharge management system built using **Python, Flask, SQLite, and Machine Learning**.

The system allows multiple family members to be managed in one place and provides recharge-plan recommendations based on daily data usage, budget, and previous recharge information.

## 🚀 Features

* 👨‍👩‍👧‍👦 Add and manage family members
* 📱 Store family mobile numbers
* 📶 View available recharge plans
* 🛒 Add multiple recharges to a cart
* 💰 Calculate total recharge amount
* 💳 Demo payment workflow
* 📋 Recharge history
* 🤖 AI/ML-based recharge recommendation
* 🧠 Recharge history analysis
* 📊 Family recharge dashboard
* 💾 SQLite database storage

## 🤖 AI/ML Recommendation

The project uses a **Decision Tree Classifier** to recommend a suitable recharge plan.

### Input Features

* Daily data usage in GB
* User budget
* Previous recharge plan

### Output

The model predicts a suitable recharge plan from the available plans:

| Plan      | Data       |
| --------- | ---------- |
| ₹199 Plan | 1.5 GB/day |
| ₹299 Plan | 2 GB/day   |
| ₹349 Plan | 2.5 GB/day |
| ₹399 Plan | 3 GB/day   |

The current ML dataset contains **29 synthetic/demo training records**.

The system also stores the **actual plan selected by the user** as the training label. This avoids using the model's own prediction as its training label.

## 🏗️ System Workflow

### Normal Recharge Flow

```text
User
  ↓
Home Page
  ↓
Family Management
  ↓
Select Recharge Plan
  ↓
Add to Cart
  ↓
Calculate Total
  ↓
Demo Payment
  ↓
Recharge History
  ↓
Dashboard
```

### AI Recommendation Flow

```text
Daily Usage + Budget + Previous Plan
                  ↓
          Decision Tree Model
                  ↓
        Recommended Plan
                  ↓
       User Selects Actual Plan
                  ↓
          Training Data
```

## 🛠️ Technologies Used

| Technology    | Purpose                   |
| ------------- | ------------------------- |
| Python        | Backend programming       |
| Flask         | Web application framework |
| HTML          | Web page structure        |
| CSS           | User interface styling    |
| JavaScript    | Client-side interaction   |
| SQLite        | Database                  |
| Pandas        | Data processing           |
| NumPy         | Numerical operations      |
| Scikit-learn  | Machine learning          |
| Decision Tree | Plan classification       |

## 📂 Project Structure

```text
AI_FAMILY_PACKAGE/
│
├── app.py
├── database.py
├── family.db
│
├── ml/
│   ├── recommendation.py
│   ├── history_analysis.py
│   ├── train_model.py
│   └── ml_predictor.py
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── members.html
    ├── members_list.html
    ├── plans.html
    ├── cart.html
    ├── payment.html
    ├── payment_success.html
    ├── history.html
    ├── recommendations.html
    ├── ai_history.html
    └── dashboard.html
```

## 🗄️ Database

The application uses SQLite with three main tables.

### `members`

Stores family member information.

* `id`
* `name`
* `mobile`

### `recharge_history`

Stores completed demo recharge transactions.

* `id`
* `member_name`
* `mobile`
* `plan`
* `amount`
* `payment_method`
* `recharge_date`

### `ml_training_data`

Stores data used for the ML recommendation model.

* `id`
* `usage`
* `budget`
* `previous_plan`
* `selected_plan`

## 💳 Payment

The current payment workflow is **simulated for academic demonstration**.

It records the selected payment method and stores the recharge transaction.

It does **not** perform or verify a real financial transaction.

A production version could integrate an appropriate official payment gateway and telecom recharge API.

## 📊 Dashboard

The dashboard provides an overview of family recharge activity, including:

* Total family members
* Total recharges
* Total spending
* Most-used recharge plan
* Spending analytics
* Plan analytics
* AI system status

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/leelavenkat2804-svg/AI-Family-Recharge-System.git
```

### 2. Open the project

```bash
cd AI-Family-Recharge-System
```

### 3. Install required Python packages

```bash
pip install flask pandas numpy scikit-learn
```

### 4. Create the database

```bash
python database.py
```

### 5. Start the Flask application

```bash
python app.py
```

### 6. Open the application

Open the local address shown by Flask in your web browser.

Usually:

```text
http://127.0.0.1:5000
```

## 🧪 Testing

The following modules have been tested during development:

* Family member registration
* Family member listing
* Recharge plan selection
* Cart management
* Total amount calculation
* Demo payment
* Recharge history
* AI recommendation
* Actual ML plan selection
* AI history analysis
* Dashboard analytics

## ⚠️ Current Limitations

* Payment processing is simulated.
* No real telecom recharge API is connected.
* ML training data is synthetic/demo data.
* The number of available recharge plans is limited.
* More real-world data would be required for a stronger ML model.
* Production deployment would require additional security and authentication.

## 🔮 Future Enhancements

Possible future improvements include:

* Real payment gateway integration
* Telecom recharge API integration
* Larger real-world ML dataset
* Improved machine-learning models
* Personalized recommendations
* Monthly spending prediction
* Recharge reminders
* Low-balance alerts
* SMS/email notifications
* Mobile application
* Cloud deployment
* User authentication
* Advanced analytics

## 🎓 Academic Project

**Project:** AI Family Recharge System

**Degree:** B.Tech

**Branch:** Computer Science and Engineering (Artificial Intelligence and Machine Learning)

**Expected Graduation:** 2027

## 📌 Project Status

**Development Status:** Working academic prototype

The current version demonstrates family recharge management, cart processing, simulated payment, recharge history, dashboard analytics, and machine-learning-based plan recommendation.
