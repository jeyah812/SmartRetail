# SmartRetail - AI-Powered Retail Analytics & Decision Support Platform

SmartRetail is an intelligent retail decision-support platform designed to help retail managers and store owners analyze sales performance, evaluate profit predictions against actual financial results, optimize inventory stock levels, and monitor sustainability metrics aligned with UN Sustainable Development Goals (SDGs).

---

## 🌟 Key Features

1. **Owner Analytics Dashboard**: Comprehensive KPI cards (Total Sales, Total Profit, Profit Margin, Average Order Value, Average Discount) with dynamic charts.
2. **Actual Profit vs. Predicted Profit Comparison**: Side-by-side financial metric comparison, deviation percentage, MAE/RMSE model metrics, and monthly comparison visualization.
3. **Derived Inventory Insights**: Stock health indicators, turnover rates, estimated days of supply, reorder alerts, and overstock warnings computed directly from sales patterns.
4. **Sustainability Dashboard (SDG Alignment)**: Environmental impact metrics (Estimated CO₂ emissions, shipping mode emissions, packaging waste, return rate, SDG 8, 9, 12, 13 tracking).
5. **Smart AI Business Advisor**: Integrated Groq LLM assistant providing tailored tactical advice across sales, inventory, and profitability.

---

## 🏗 System Architecture

```
SmartRetail/
├── app.py                 # Flask web application routes & controllers
├── config.py              # Application settings & environment configuration
├── advisor.py             # Groq LLM API client integration
├── requirements.txt       # Project Python dependencies
├── data/                  # Raw and processed CSV datasets
├── models/                # Trained ML models, encoders, and performance metrics
├── src/
│   ├── dashboard.py       # KPI statistics, dynamic chart generation, sustainability & inventory
│   ├── predict.py         # Model loading, feature preprocessing & profit prediction comparison
│   ├── validator.py       # CSV dataset structure validation
│   ├── feature_engineering.py # Date, shipping, and sales feature extraction
│   └── recommendation.py  # Rule-based business recommendation engine
├── templates/             # Jinja2 HTML templates
└── static/                # CSS stylesheets, static images, generated charts, and uploads
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SmartRetail
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=smartretail-secret-key
   ```

4. **Train Machine Learning Model (Optional)**:
   ```bash
   python src/train_model.py
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

---

## 📊 SDG Alignment

- **SDG 8: Decent Work & Economic Growth**: Enhances retail productivity and profitability through data-driven operational decision-making.
- **SDG 9: Industry, Innovation & Infrastructure**: Leverages predictive machine learning models to modernize small/medium enterprise retail infrastructure.
- **SDG 12: Responsible Consumption & Production**: Identifies overstocked items and reduces product waste through sales-derived inventory turnover analytics.
- **SDG 13: Climate Action**: Tracks logistics CO₂ footprint and promotes eco-friendly shipping modes.
