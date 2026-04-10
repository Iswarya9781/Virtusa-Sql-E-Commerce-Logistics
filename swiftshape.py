import streamlit as st
import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# -------------------------------
# 1. DB CONNECTION
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="IsWarya@7811",
    database="SwiftShip"
)

# -------------------------------
# 2. FETCH DATA FUNCTION
# -------------------------------
def fetch_data(query):
    return pd.read_sql(query, conn)

st.title("🚚 SwiftShip Logistics Dashboard")

# -------------------------------
# 3. PARTNER SCORECARD
# -------------------------------
st.header("📊 Partner Scorecard")

score_query = """
SELECT 
    P.PartnerName,
    COUNT(*) AS TotalShipments,
    COUNT(CASE WHEN S.ActualDeliveryDate > S.PromisedDate THEN 1 END) AS DelayedShipments,
    ROUND(
        (COUNT(*) - COUNT(CASE WHEN S.ActualDeliveryDate > S.PromisedDate THEN 1 END)) * 100.0 / COUNT(*),
        2
    ) AS OnTimePercentage
FROM Shipments S
JOIN Partners P ON S.PartnerID = P.PartnerID
GROUP BY P.PartnerName
ORDER BY DelayedShipments ASC;
"""

df_score = fetch_data(score_query)
st.dataframe(df_score)

# -------------------------------
# 4. DELAYED SHIPMENTS
# -------------------------------
st.header("🚚 Delayed Shipments")

delay_query = """
SELECT * FROM Shipments
WHERE ActualDeliveryDate > PromisedDate;
"""

df_delay = fetch_data(delay_query)
st.dataframe(df_delay)

# -------------------------------
# 5. POPULAR DESTINATION
# -------------------------------
st.header("🏙️ Most Popular Destination")

popular_query = """
SELECT DestinationCity, COUNT(*) AS TotalOrders
FROM Shipments
WHERE OrderDate >= CURDATE() - INTERVAL 30 DAY
GROUP BY DestinationCity
ORDER BY TotalOrders DESC
LIMIT 1;
"""

df_popular = fetch_data(popular_query)
st.table(df_popular)

# -------------------------------
# 6. TRAIN ML MODEL
# -------------------------------
st.header("🤖 Delay Prediction")

ml_query = """
SELECT PartnerID, OriginCity, DestinationCity, OrderDate, PromisedDate, ActualDeliveryDate
FROM Shipments;
"""

df = fetch_data(ml_query)

# Feature engineering
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['PromisedDate'] = pd.to_datetime(df['PromisedDate'])
df['ActualDeliveryDate'] = pd.to_datetime(df['ActualDeliveryDate'])

df['Delayed'] = (df['ActualDeliveryDate'] > df['PromisedDate']).astype(int)
df['DeliveryTime'] = (df['ActualDeliveryDate'] - df['OrderDate']).dt.days
df['PromisedTime'] = (df['PromisedDate'] - df['OrderDate']).dt.days

# Encode
le1 = LabelEncoder()
le2 = LabelEncoder()

df['OriginCity'] = le1.fit_transform(df['OriginCity'])
df['DestinationCity'] = le2.fit_transform(df['DestinationCity'])

X = df[['PartnerID', 'OriginCity', 'DestinationCity', 'DeliveryTime', 'PromisedTime']]
y = df['Delayed']

model = RandomForestClassifier()
model.fit(X, y)

# -------------------------------
# 7. USER INPUT UI
# -------------------------------
st.subheader("Enter Shipment Details")

partner = st.number_input("Partner ID", min_value=1, step=1)
origin = st.text_input("Origin City")
destination = st.text_input("Destination City")
delivery_days = st.number_input("Estimated Delivery Days", min_value=1)
promised_days = st.number_input("Promised Days", min_value=1)

if st.button("Predict Delay"):
    try:
        origin_enc = le1.transform([origin])[0]
        dest_enc = le2.transform([destination])[0]

        input_data = [[partner, origin_enc, dest_enc, delivery_days, promised_days]]

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.error("⚠️ Shipment will be DELAYED")
        else:
            st.success("✅ Shipment will be ON-TIME")

    except:
        st.warning("⚠️ Enter valid city names from dataset")

# -------------------------------
# 8. CHART
# -------------------------------
st.header("📈 Partner Performance")

st.bar_chart(df_score.set_index("PartnerName")["OnTimePercentage"])