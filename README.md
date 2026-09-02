# SmartRetail 🛒

### A Data-Driven Decision Support System for Sustainable Retail Operations

SmartRetail is a web-based retail analytics and decision support system that helps businesses understand sales performance, monitor inventory, predict profit, and make data-driven decisions.

The system combines **Business Intelligence, Machine Learning, Inventory Analytics, Recommendation Systems, AI Assistance, and Sustainability Indicators** into a single platform.

---

## ✨ Features

### 📊 Sales Analytics
- Total sales and profit analysis
- Profit margin calculation
- Average sales and discount analysis
- Sales and profit trends
- Category-wise sales and profit
- Product performance analysis
- Dynamic charts generated from the active dataset

### 🤖 Profit Prediction
- Machine learning-based profit prediction
- Actual vs predicted profit comparison
- Category-level prediction analysis
- Prediction variance and error calculation

### 🧠 Machine Learning Models
SmartRetail evaluates multiple regression models:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Model performance is evaluated using:

- R² Score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

The best-performing model is selected for prediction.

### 📦 Inventory Management
- Product tracking
- Stock-level monitoring
- Reorder levels
- Low-stock alerts
- Critical-stock alerts
- Product category distribution
- Add and manage products
- Supplier and pricing information

### 💡 Recommendations
The system generates actionable recommendations based on retail performance, including:

- Sales performance
- Profitability
- Inventory conditions
- Discount patterns
- Product performance

### 💬 SmartRetail AI Assistant
An integrated assistant helps users interact with retail information and provides insights related to:

- Sales
- Profit
- Inventory
- Product performance
- Sustainability

### 🌱 Sustainability
SmartRetail incorporates sustainability indicators related to:

- **SDG 8** – Decent Work and Economic Growth
- **SDG 9** – Industry, Innovation and Infrastructure
- **SDG 12** – Responsible Consumption and Production

The system primarily supports SDG 12 through inventory monitoring and data-driven resource management.

---

## 🛠️ Tech Stack

| Area | Technologies |
|---|---|
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Backend | Python, Flask |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib, Plotly |
| Database | SQLite |
| Model Storage | Joblib |
| Data Storage | CSV, JSON |

---

## 📂 Project Structure

```text
SmartRetail/
│
├── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│
├── docs/
│
├── models/
│   ├── best_model.pkl
│   ├── encoders.pkl
│   └── model_metrics.json
│
├── reports/
├── presentation/
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── eda.py
│   ├── prediction.py
│   ├── recommendation.py
│   ├── dashboard.py
│   └── utils.py
│
├── static/
│   ├── images/
│   └── uploads/
│
├── templates/
│
├── requirements.txt
└── README.md