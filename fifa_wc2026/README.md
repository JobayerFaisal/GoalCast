# ⚽ FIFA World Cup 2026 — Data Analysis & Match Prediction

An end-to-end data science project combining **data analytics**, **visualization**, and **machine learning** to predict FIFA World Cup 2026 match outcomes — built using **Agile/Scrum** methodology as part of an MSc project.

🔗 **Live demo:** _add Streamlit Cloud link here after deployment_

---

## 📌 Project Overview

| | |
|---|---|
| **Goal** | Predict World Cup match outcomes (Home Win / Draw / Away Win) and visualize team performance |
| **Methodology** | Agile/Scrum — 4 sprints, 2 weeks each |
| **Data sources** | [API-Football](https://www.api-football.com/), Kaggle international results dataset |
| **ML models** | Logistic Regression → XGBoost / Random Forest → Neural Network (Keras) |
| **Deployment** | Streamlit Cloud |

---

## 🗺️ Sprint Roadmap

- **Sprint 1 ✅** — Data collection pipeline, project structure, basic dashboard
- **Sprint 2** — Data cleaning, feature engineering, EDA visualizations
- **Sprint 3** — ML model training & evaluation
- **Sprint 4** — Full prediction dashboard & deployment

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Data:** pandas, numpy
- **Visualization:** plotly, seaborn, matplotlib
- **ML:** scikit-learn, xgboost, tensorflow/keras
- **Dashboard:** Streamlit
- **Project management:** Agile/Scrum (Notion / GitHub Projects)

---

## 📂 Project Structure

```
fifa_wc2026/
├── data/
│   ├── raw/              # raw API & Kaggle data (gitignored)
│   └── processed/        # cleaned, feature-engineered data
├── notebooks/            # Jupyter notebooks for EDA
├── src/
│   ├── config.py         # central configuration
│   ├── data/
│   │   ├── api_client.py # API-Football wrapper
│   │   ├── collect.py     # data collection script
│   │   └── load_kaggle.py # historical data loader
│   ├── models/           # ML training & evaluation scripts
│   └── viz/               # reusable chart functions
├── streamlit_app/
│   └── app.py            # dashboard entry point
├── tests/                 # unit tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone & install
```bash
git clone <your-repo-url>
cd fifa_wc2026
pip install -r requirements.txt
```

### 2. (Optional) Set up API access
```bash
cp .env.example .env
# Edit .env and add your free API-Football key
# Get one at: https://www.api-football.com/
```

> **Note:** The project works without an API key too — `load_kaggle.py` generates
> a synthetic sample dataset so you can run the full pipeline immediately.

### 3. Collect data
```bash
# Historical data (works offline with sample data fallback)
python -m src.data.load_kaggle

# Live World Cup 2026 data (requires API key)
python -m src.data.collect
```

### 4. Run the dashboard
```bash
streamlit run streamlit_app/app.py
```

---

## ☁️ Deployment (Streamlit Cloud — free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set main file to `streamlit_app/app.py`
4. (Optional) Add `API_FOOTBALL_KEY` as a secret in **App settings → Secrets**
5. Deploy! 🎉

---

## 📋 Agile Process

This project follows Scrum with 2-week sprints, a product backlog, daily
standups (solo journal entries), sprint reviews, and retrospectives. See
`docs/backlog.md` for the full list of user stories and acceptance criteria.

---

## 📄 License

MIT — feel free to fork and build on this for your own portfolio!
