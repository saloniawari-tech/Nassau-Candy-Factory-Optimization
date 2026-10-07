# Factory Reallocation & Shipping Optimization Recommendation System

## Nassau Candy Distributor

A decision-intelligence project that combines predictive modeling, route analysis, scenario simulation, and optimization logic to evaluate factory assignments and recommend whether products should be reassigned to alternative factories.

## 🎯 Business Problem

Nassau Candy Distributor uses static factory assignments. This can lead to:

- Suboptimal shipping distances
- Higher lead times for certain regions
- Logistics inefficiencies
- Potential margin pressure

This project evaluates alternative factory assignments before execution and provides data-driven recommendations.

## 📊 Dataset

The dataset contains **10,194 orders** and **18 original fields**, including:

- Order Date
- Ship Date
- Ship Mode
- Region
- Product Name
- Sales
- Units
- Gross Profit
- Cost

Additional features were created for modeling and optimization.

## 🔬 Methodology

### 1. Data Preparation
- Data validation
- Date processing
- Lead-time calculation
- Feature engineering
- Categorical encoding

### 2. Predictive Modeling

The project evaluates:

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor

The selected model is **Gradient Boosting Regressor**.

| Model | RMSE | MAE | R² |
|---|---:|---:|---:|
| Linear Regression | 182.43 | 181.41 | 0.5294 |
| Random Forest | 192.47 | 172.88 | 0.4762 |
| Gradient Boosting | **181.58** | 179.96 | **0.5338** |

### 3. Route Clustering

Reliable product-region routes were grouped using K-Means clustering to identify similar route-performance patterns.

### 4. Scenario Simulation

The system evaluates alternative factory assignments for reliable product-region combinations.

**120 factory scenarios** were evaluated.

### 5. Recommendation Logic

Factory alternatives are ranked using:

- Lead-time reduction
- Profit stability
- Factory-region distance

## 📈 Key Results

| KPI | Result |
|---|---:|
| Total scenarios evaluated | 120 |
| Alternative factory scenarios | 96 |
| Beneficial reassignment scenarios | 0 |
| Current factory retained | 24 |
| Average predicted lead-time reduction | -12.59% |
| Profit impact stability | 100% |
| Scenario confidence score | 53.38% |
| Recommendation coverage | 0% |

### Main Finding

No evaluated alternative factory assignment produced a predicted lead-time improvement under the current model and scenario assumptions.

Therefore, the system recommends:

**Keep the current factory assignment for the evaluated product-region routes.**

## 🖥️ Streamlit Dashboard

The project includes an interactive Streamlit decision-support dashboard.

### Dashboard features

- Factory Optimization Simulator
- What-If Scenario Analysis
- Recommendation Dashboard
- Risk & Impact Panel
- Product selector
- Region selector
- Ship mode filter
- Optimization priority controls

### 🚀 Live Dashboard

**[Open the Factory Shipping Optimization Dashboard](https://factory-shipping-optimizer.streamlit.app/)**

## 📁 Project Structure

```text
Nassau-Candy-Factory-Optimization/
│
├── data/
│   ├── Nassau Candy Distributor.csv
│   └── processed/
│
├── notebooks/
│   ├── 01_data_validation.ipynb
│   ├── 02_clustering_and_optimization.ipynb
│   └── 03_streamlit_preparation.ipynb
│
├── streamlit/
│   └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
