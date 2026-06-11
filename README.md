# High-Volume Space & Scheduling Utilization Analyzer

A polyglot data pipeline built to ingest, aggregate, and evaluate scheduling efficiency parameters across enterprise infrastructures. This project showcases how to handle heavy math and relational database patterns across **100,000+ data rows**.

## 🛠️ Tech Stack & Roles
- **SQL (Relational Storage):** Implements schemas with compound indices engineered to execute fast relational joins and time-series selections.
- **Python (Data Science):** Utilizes `pandas` and `numpy` matrix calculations to analyze metrics, pinpoint scheduling bottlenecks, and identify system anomalies.
- **TypeScript (API Layer):** Orchestrates analytical executions using a backend Node.js environment to safely deliver report arrays via REST interfaces.

## 📈 Computational Performance Metrics
- **Data Throughput:** Evaluates **100,000+ scheduling data records** seamlessly using vectorized matrix formats.
- **Key Indicators Calculated:** Seat-Fill Matrix Ratios, Peak Hour Overloads, and Facility Under-Utilization tracking profiles.

## 🚀 Execution & Verification

### 1. Initialize TypeScript Server
```bash
npm install express typescript @types/express @types/node ts-node
npx ts-node server.ts
