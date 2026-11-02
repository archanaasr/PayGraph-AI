# PayGraph AI
**Connecting the Dots. Predicting Fraud. Securing Every Payment.**

PayGraph AI is a hackathon-ready payment-risk intelligence prototype. It combines synthetic transaction generation, graph relationship analysis, classical ML anomaly detection, explainable transaction features, an optional OpenAI investigation assistant, and PayPal Sandbox order creation.

## Important scope and honesty
- The included graph module uses NetworkX relationship analysis. It is **not** a trained Graph Neural Network.
- The initial fraud classifier is a Random Forest baseline. It is trained on generated synthetic labels and is not evidence of real-world fraud detection performance.
- The anomaly detector is Isolation Forest.
- PayPal Sandbox orders are test payments, not real customer payments and do not provide fraud labels.
- The app does not automatically block payments. Risk scores are for human review.
- OpenAI and PayPal credentials are optional; the dashboard and synthetic demo can run without them.

## Windows setup
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and add your PayPal Sandbox client ID and secret if you want to test PayPal order creation. Add an OpenAI API key only if you want the hosted AI assistant.

## Run
```powershell
streamlit run app.py
```
Open the local URL shown by Streamlit. Select **Overview → Generate demo transactions**.

## Tests
```powershell
pytest -q
```

## PayPal Sandbox
1. Create a REST app in the PayPal Developer Dashboard.
2. Copy Sandbox client ID and secret into `.env`.
3. Keep `PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com`.
4. Use the PayPal Sandbox page in the app to create a test order.
5. To capture an order, use the backend `capture_order(order_id)` function after buyer approval. Do not expose secrets in the browser.

## Project structure
- `app.py`: Streamlit UI
- `paypal/`: OAuth, orders, webhook signature verification
- `models/`: Random Forest baseline and Isolation Forest
- `graph/`: transaction graph construction and summary
- `ai/`: optional OpenAI investigation helper
- `database/`: SQLite schema and persistence
- `utils/`: synthetic data and feature preparation

## Future development
A next research iteration can add a genuinely trained PyTorch Geometric GCN/GraphSAGE model, temporal graph features, validated public fraud datasets, model calibration, role-based access, and a dedicated webhook receiver with event idempotency.
