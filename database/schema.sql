CREATE TABLE IF NOT EXISTS transactions (
 transaction_id TEXT PRIMARY KEY, sender_id TEXT NOT NULL, receiver_id TEXT NOT NULL,
 merchant_id TEXT, amount REAL NOT NULL, timestamp TEXT NOT NULL, frequency_24h INTEGER DEFAULT 1,
 account_age_days INTEGER DEFAULT 365, category TEXT DEFAULT 'retail', payment_status TEXT DEFAULT 'COMPLETED',
 is_fraud INTEGER DEFAULT 0, source TEXT DEFAULT 'synthetic'
);
