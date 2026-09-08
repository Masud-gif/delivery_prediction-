import streamlit as st
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
rf_model = joblib.load(os.path.join(BASE_DIR, 'delivery_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'delivery_scaler.pkl'))
training_columns = joblib.load(os.path.join(BASE_DIR, 'delivery_columns.pkl'))

st.title("Delivery Outcome Predictor")
st.write("Enter a new order's details to predict if it will be On-Time, Delayed, or Cancelled.")

# --- Simple input widgets — these replace typing a Python dictionary by hand ---
order_value = st.number_input("Order Value (taka)", min_value=100, max_value=30000, value=2000)
distance_km = st.number_input("Distance (km)", min_value=1, max_value=150, value=15)
customer_rating_history = st.slider("Customer Rating History", 1.0, 5.0, 4.0)
num_items = st.number_input("Number of Items", min_value=1, max_value=15, value=2)
promo_applied = st.selectbox("Promo Applied?", ["No", "Yes"])
order_month = st.selectbox("Order Month", list(range(1, 13)))
order_dayofweek = st.selectbox("Day of Week (0=Mon, 6=Sun)", list(range(0, 7)))

category = st.selectbox("Category", ["electronics", "clothing", "groceries", "home & kitchen", "beauty", "books"])
warehouse_city = st.selectbox("Warehouse City", ["Dhaka", "Chattogram", "Sylhet", "Khulna", "Rajshahi"])
courier_partner = st.selectbox("Courier Partner", ["pathao", "redx", "e-courier", "sa paribahan", "sundarban"])
payment_method = st.selectbox("Payment Method", ["Cash on Delivery", "Card", "Mobile Banking"])

# --- When the button is clicked, build the row and predict ---
if st.button("Predict Delivery Outcome"):

    # Step 1: build the raw order as a dictionary
    order_details = {
        'order_value': order_value,
        'distance_km': distance_km,
        'customer_rating_history': customer_rating_history,
        'num_items': num_items,
        'promo_applied': 1 if promo_applied == "Yes" else 0,
        'order_month': order_month,
        'order_of_the_week': order_dayofweek,
        f'category_{category}': 1,
        f'warehouse_city_{warehouse_city}': 1,
        f'courier_partner_{courier_partner}': 1,
        f'payment_method_{payment_method}': 1,
    }

    # Step 2: turn it into a dataframe, one-hot encode, align columns (same as before)
    new_order_df = pd.DataFrame([order_details])
    new_order_encoded = pd.get_dummies(new_order_df)
    new_order_aligned = new_order_encoded.reindex(columns=training_columns, fill_value=0)

    # Step 3: scale using the SAME scaler from training
    new_order_scaled = scaler.transform(new_order_aligned)

    # Step 4: predict
    prediction = rf_model.predict(new_order_scaled)[0]
    probabilities = rf_model.predict_proba(new_order_scaled)[0]

    st.subheader(f"Prediction: {prediction}")

    # Show confidence for each class
    st.write("Confidence breakdown:")
    prob_df = pd.DataFrame({
        'Outcome': rf_model.classes_,
        'Probability': probabilities
    }).sort_values('Probability', ascending=False)
    st.dataframe(prob_df)
    import os

