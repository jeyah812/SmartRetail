# 🛒 SmartRetail
## A Data-Driven Decision Support System for Sustainable Retail Operations

SmartRetail is a web-based **retail analytics and intelligent decision support system** designed to help retail businesses analyze sales performance, monitor inventory, predict profit, and make data-driven operational decisions.

The system combines **Business Intelligence, Machine Learning, Inventory Analytics, Rule-Based Recommendations, AI Assistance, and Sustainability Indicators** into a unified retail management platform.

---

## 🎯 Project Objective

Traditional retail systems primarily record transactions but provide limited support for analyzing business performance and making intelligent decisions.

SmartRetail addresses this problem by transforming raw retail transaction data into:

- 📊 Business intelligence dashboards
- 📈 Sales and profit analytics
- 🤖 Machine learning-based profit prediction
- 📦 Inventory monitoring and reorder alerts
- 💡 Intelligent business recommendations
- 🌱 Sustainability indicators
- 💬 AI-assisted retail data interaction

The primary goal is to help retail stakeholders understand current business performance and use predictive insights to support better decisions.

---

## ✨ Key Features

### 📊 Sales & Business Analytics

SmartRetail provides dynamic analytics based on the active retail dataset.

Features include:

- Total Sales
- Total Profit
- Total Quantity
- Profit Margin
- Average Sale
- Average Discount
- Records Analyzed
- Sales by Category
- Profit by Category
- Sales Trends
- Profit Trends
- Product Performance
- Category Distribution
- Sales Distribution

All major analytics are generated dynamically from the currently active dataset.

---

### 🤖 Profit Prediction

SmartRetail uses Machine Learning to predict retail profit.

The system supports:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

The prediction system uses retail features such as:

- Sales
- Quantity
- Discount
- Category
- Sub-Category
- Region
- Segment
- Shipping Days
- Order Year
- Order Quarter

The system evaluates model performance using:

- R² Score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

The best-performing model is selected for profit prediction.

---

### 📈 Actual vs Predicted Profit Analysis

After prediction, SmartRetail provides a comparison between:

- Actual Profit
- Predicted Profit
- Prediction Variance
- Error Percentage

The system also generates a category-level comparison visualization showing actual profit against predicted profit.

---

### 📦 Inventory Management

SmartRetail provides inventory monitoring features including:

- Product tracking
- Current stock monitoring
- Reorder levels
- Low-stock detection
- Critical-stock alerts
- Product category distribution
- Product addition
- Supplier information
- Unit price tracking
- Last updated information

The inventory dashboard helps identify products requiring immediate attention.

---

### 💡 Intelligent Recommendations

SmartRetail generates business recommendations based on retail performance data.

Recommendations can address:

- Sales performance
- Profitability
- Discounts
- Inventory conditions
- Product performance
- Operational improvements

The recommendation engine converts analytical results into actionable business suggestions.

---

### 💬 SmartRetail AI Assistant

The system includes an AI-style retail assistant that allows users to interact with their retail information.

It can assist with queries related to:

- Sales
- Profit
- Inventory
- Product performance
- Sustainability
- Business insights

This provides a conversational interface for accessing important retail information.

---

### 🌱 Sustainability Support

SmartRetail incorporates sustainability-oriented indicators to support responsible retail operations.

The system provides indicators related to:

- SDG 8 – Decent Work and Economic Growth
- SDG 9 – Industry, Innovation and Infrastructure
- SDG 12 – Responsible Consumption and Production

The system particularly supports **SDG 12** by using inventory monitoring, sales analysis, and decision support to help reduce inventory imbalance and improve resource utilization.

---

## 🧠 Machine Learning Workflow

The prediction workflow follows these steps:

```text
Retail Dataset
      ↓
Dataset Validation
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Feature Selection
      ↓
Train ML Models
      ↓
Evaluate Models
      ↓
Select Best Model
      ↓
Predict Profit
      ↓
Compare Actual vs Predicted
      ↓
Generate Business Insights