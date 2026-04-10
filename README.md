# 🚚 SwiftShip Logistics Tracker

## 📌 Project Overview

SwiftShip is a logistics tracking and analytics system designed to monitor shipment performance, identify delays, and evaluate delivery partners.
This project combines **SQL, Machine Learning, and Streamlit UI** to deliver an end-to-end solution.

---

## 🎯 Objectives

* Identify **delayed shipments**
* Analyze **delivery partner performance**
* Find **high-demand destination cities**
* Predict **future shipment delays using Machine Learning**

---

## 🛠️ Tech Stack

* **Database:** MySQL (MySQL Workbench)
* **Query Language:** SQL
* **Backend & ML:** Python (Pandas, Scikit-learn)
* **Frontend UI:** Streamlit
* **Version Control:** Git & GitHub

---

## 🗂️ Project Structure

```
SwiftShip-Logistics/
│
├── SwiftShape.sql      # Database schema + sample data
├── swiftshape.py       # ML model + DB connection + Streamlit UI
├── requirements.txt    # Dependencies
├── .gitignore
└── README.md
```

---

## 🧩 Database Design

### 🔹 Tables Used

* **Partners** → Stores delivery partner details
* **Shipments** → Stores shipment information
* **DeliveryLogs** → Tracks shipment updates

---

## 📊 Key Features

### 🚚 1. Delayed Shipment Detection

Identifies shipments where:

```
ActualDeliveryDate > PromisedDate
```

---

### 📊 2. Partner Performance Scorecard

* Total Shipments
* Delayed Shipments
* On-Time Delivery Percentage

---

### 🏙️ 3. Popular Destination Analysis

Finds the most frequent destination city in the last 30 days.

---

### 🤖 4. Machine Learning Prediction

* Model: **Random Forest Classifier**
* Predicts whether a shipment will be:

  * ✅ On-Time
  * ⚠️ Delayed

---

## ▶️ How to Run the Project

### 🔹 1. Setup Database

Run the SQL file in MySQL Workbench:

```sql
CREATE DATABASE SwiftShip;
USE SwiftShip;
-- Run SwiftShape.sql
```

---

### 🔹 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 3. Run Streamlit App

```bash
streamlit run app.py
```

---

## 📈 Sample Outputs

### 📊 Partner Scorecard

* Displays partner performance ranking

### 🚚 Delayed Shipments

* Lists all late deliveries

### 📈 Dashboard Visualization

* Bar chart showing partner efficiency

### 🤖 Prediction Output

* User inputs shipment details
* Model predicts delay status

---

## 🔥 Key Highlights

* End-to-end project: **Database → Analytics → ML → UI**
* Real-world logistics use case
* Integrated SQL queries with ML predictions
* Interactive dashboard using Streamlit

---

## 🚀 Future Enhancements

* Add **real-time tracking system**
* Integrate **Power BI dashboard**
* Improve ML model using **XGBoost**
* Add **route optimization algorithms**

---

## 👩‍💻 Author

**Iswaryakarthick**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
