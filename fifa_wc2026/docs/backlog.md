# Product Backlog — FIFA World Cup 2026 Prediction Project

## Epic 1 — Data Collection & Storage (Sprint 1)

| ID | User Story | Acceptance Criteria | Priority | Points |
|----|-----------|---------------------|----------|--------|
| US-01 | As a data engineer, I want to connect to API-Football so that I can fetch live World Cup match data. | API returns match results, team stats, fixtures as JSON. Credentials in `.env`. | High | 3 |
| US-02 | As a data engineer, I want to download historical FIFA datasets so that I have data for training. | Historical dataset saved to `data/raw`. Fallback sample generator works offline. | High | 2 |
| US-03 | As a data engineer, I want structured local storage so data is easy to query. | Data saved as CSV/JSON with documented schema. | High | 2 |
| US-04 | As a data engineer, I want scheduled updates so predictions use fresh data. | Script can be re-run to append new results. | Medium | 3 |

**Definition of Done:** Raw data collected from at least 2 sources, stored, version-controlled.

---

## Epic 2 — Data Processing & EDA (Sprint 2)

| ID | User Story | Acceptance Criteria | Priority | Points |
|----|-----------|---------------------|----------|--------|
| US-05 | As a data analyst, I want clean data so analysis isn't skewed by errors. | No nulls/duplicates. Cleaning documented. | High | 3 |
| US-06 | As a data analyst, I want engineered features (form, ranking, xG) for modelling. | ≥8 features created and documented. | High | 5 |
| US-07 | As a data analyst, I want visualizations of team trends. | ≥5 charts covering form, goals, head-to-head. | Medium | 3 |
| US-08 | As a data analyst, I want a correlation heatmap to pick top features. | Heatmap + top 10 features documented. | Medium | 2 |

**Definition of Done:** EDA notebook complete, features engineered & documented.

---

## Epic 3 — ML Model Development (Sprint 3)

| ID | User Story | Acceptance Criteria | Priority | Points |
|----|-----------|---------------------|----------|--------|
| US-09 | As an ML engineer, I want a Logistic Regression baseline. | Accuracy/precision/recall/F1 reported & saved. | High | 3 |
| US-10 | As an ML engineer, I want an XGBoost model to beat the baseline. | ≥5% improvement, hyperparameters tuned. | High | 5 |
| US-11 | As an ML engineer, I want a Keras neural network. | Trained, val accuracy reported, architecture documented. | Medium | 8 |
| US-12 | As an ML engineer, I want to compare all models and pick the best. | Comparison table; best model saved as `.pkl`/`.h5`. | High | 2 |
| US-13 | As an ML engineer, I want cross-validation for reliable results. | 5-fold CV, mean/std reported. | High | 3 |

**Definition of Done:** Best model saved, evaluated, ready for dashboard integration.

---

## Epic 4 — Dashboard & Deployment (Sprint 4)

| ID | User Story | Acceptance Criteria | Priority | Points |
|----|-----------|---------------------|----------|--------|
| US-14 | As a user, I want to see fixtures & predictions. | Dashboard shows fixture, predicted winner, win probability. | High | 5 |
| US-15 | As a user, I want team stats and charts. | ≥3 interactive charts per team. | High | 5 |
| US-16 | As a user, I want to filter by group/knockout stage. | Sidebar filter functions correctly. | Medium | 3 |
| US-17 | As a developer, I want the app deployed publicly. | Live on Streamlit Cloud, no crashes, README link. | High | 2 |
| US-18 | As a developer, I want a polished README. | Description, stack, setup, screenshots, demo link. | Medium | 2 |

**Definition of Done:** App live and publicly accessible; repo portfolio-ready.

---

## Scrum Ceremonies

| Ceremony | Frequency | Duration | Purpose |
|---------|-----------|----------|---------|
| Sprint Planning | Start of sprint | 1h | Pick stories, estimate points |
| Daily Standup | Daily | 10 min | Progress + blockers (solo journal) |
| Sprint Review | End of sprint | 30 min | Demo against acceptance criteria |
| Retrospective | End of sprint | 20 min | What worked / what to improve |

## Sprint Timeline

| Sprint | Dates | Focus |
|--------|-------|-------|
| 1 | Jun 11 – Jun 24 | Data collection |
| 2 | Jun 25 – Jul 8 | EDA & features |
| 3 | Jul 9 – Jul 16 | ML models |
| 4 | Jul 17 – Jul 19 | Dashboard & deployment |
