🔗 **Live App:** [Try the Delivery Outcome Predictor]https://6ln2ip6qjvdanjceipbg9u.streamlit.app/
# Delivery Outcome Risk Report
**Prepared for:** Operations & Logistics Leadership
**Prepared by:** Mahi
**Date:** [Date]

---

## Executive Summary

This project builds a model that predicts whether a new order will be delivered on time, delayed, or cancelled, using information like order value, distance, delivery category, and courier partner. It helps the company understand how to reach out to customers early, choose better courier partners, and flag risky orders before they ship.

---

## Business Context

Today, the company only discovers a delivery problem after it's already happened — a customer waiting on a late order, or an order getting cancelled outright. This creates avoidable costs: customer complaints, lost trust, and wasted operational effort reacting to problems instead of preventing them. Without any way to flag risk in advance, every order is treated the same at the time of shipping, even though some — based on distance, courier, and payment method — are far more likely to fail than others.

---

## Key Findings

1. **Delivery distance is the strongest driver of outcome.** Average distance for on-time orders is 12.7 km, versus 18.5 km for delayed orders and 25.5 km for cancelled orders — a clear, consistent pattern. This is also the single most important feature to the model, accounting for roughly 35% of its decision-making.

2. **Courier choice matters significantly.** Sundarban has only a 54.2% on-time rate and a 6.0% cancellation rate — the worst of all 5 couriers on both measures. Pathao, the best performer, achieves a 70.7% on-time rate with only 2.7% cancellations — a gap of over 16 percentage points.

3. **Cash on Delivery orders are riskier than prepaid orders.** 67.5% of cancelled orders and 60.9% of delayed orders used Cash on Delivery, compared to only 52.9% of on-time orders. This likely reflects that prepaid customers (card, mobile banking) are more committed to receiving the order.

4. **Customer rating history is a weak individual signal**, showing only a small difference between groups on its own — but it still contributes some value when combined with other features.

5. **The model reliably confirms safe orders, but struggles to catch risky ones.** After tuning for class imbalance, our best model correctly identifies 71% of true on-time orders and 35% of true cancelled orders — a major improvement over an untuned model, which caught 0% of cancellations. This reflects a genuine data limitation: cancelled orders make up only 3.4% of historical orders, giving the model few examples to learn from.

---

## Recommendations

1. **Operational, immediate:** Review Sundarban's service — renegotiate delivery terms, reduce order volume routed to them, or audit specific failure points in their process.
2. **Immediate use of the model:** Use the model as an early-warning flag for orders that are long-distance, routed through lower-performing couriers, and/or paid via Cash on Delivery — not as an automatic decision-maker.
3. **Customer communication:** For orders flagged as high-risk, consider proactive communication (e.g. an SMS confirming delivery windows) to reduce cancellation likelihood, particularly for Cash on Delivery orders.
4. **Next model iteration:** Collect more examples of cancelled orders, or apply further techniques for rare-outcome prediction, to improve the model's ability to catch cancellations specifically.
5. **Data collection:** Consider capturing additional signals not currently available (e.g. weather, real-time courier capacity, customer's order history with the company) which likely explain some of the currently unaccounted-for variation.

---

## Methodology *(brief — for technical review)*

- **Data:** ~8,900 historical orders (Jan 2023 – Dec 2024), cleaned for missing values, duplicate records, and inconsistent text entries.
- **Feature engineering:** Extracted order month and day-of-week from raw order dates; one-hot encoded category, courier partner, warehouse city, and payment method.
- **Models tested:** Logistic Regression, Decision Tree, and Random Forest, each tested with and without class balancing (`class_weight='balanced'`), on an 80/20 train/test split.
- **Evaluation:** 3-class confusion matrix and per-class precision/recall, since overall accuracy alone was found to be misleading on this imbalanced target.
- **Deployment:** Final model deployed as a live, interactive web app (Streamlit), allowing non-technical staff to enter a new order's details and receive an instant prediction with confidence scores.

---

## Limitations

- The model has not been validated on live, real-time data — only historical records.
- Cancelled orders are rare in the training data (3.4%), which limits how confidently the model can identify that outcome; even after tuning, it catches only about a third of true cancellations.
- The model does not currently account for external factors such as weather, holidays, or day-to-day courier capacity.
- Results should be treated as a directional risk signal to support human decision-making, not as a fully automated go/no-go system at this stage.

---

*Full technical notebook, code, and live app link available in the accompanying repository.*
