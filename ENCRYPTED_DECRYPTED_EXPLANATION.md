# Understanding Encrypted vs Decrypted Results

## Overview
In homomorphic encryption systems like PrivAnalytica, there are two stages of results displayed:

1. **Encrypted Result** - The result while still encrypted (in homomorphic encryption format)
2. **Decrypted Result** - The actual numeric value after decryption

---

## What Each Result Means

### 🔐 **Encrypted Result**
- **Format**: Base64-encoded string of encrypted data
- **Purpose**: Shows what the server computed without ever seeing the actual values
- **Readability**: NOT human-readable - it's encrypted binary data encoded as text
- **Example**: `ZW5jcnlwdGVkX2F2ZXJhZ2VfcmVzdWx0XzUw` (meaningless to humans)
- **Privacy**: Even the server cannot read this value - it's computed on encrypted data

**Why it exists**: 
- Proves that computations were done on encrypted data
- Demonstrates privacy-preserving computation
- Shows the "raw" encrypted output before decryption

---

### 🔓 **Decrypted Result**
- **Format**: Human-readable number (e.g., `6.02`, `301.00`, `0.456`)
- **Purpose**: The actual computed value you're interested in
- **Readability**: Fully readable - this is the answer to your query
- **Example**: `79.33` (average final score), `50` (count of records)
- **Privacy**: Only visible after decryption with the secret key (which only you have)

**Why it exists**:
- This is the actual statistic you requested
- The value you use for analysis
- The "answer" to your query

---

## How It Works (Conceptual)

```
Your Data → Encryption → Encrypted Data
                           ↓
                      Server computes
                      on encrypted data
                           ↓
                    Encrypted Result
                           ↓
                    You decrypt (with secret key)
                           ↓
                    Decrypted Result (the answer)
```

### Example: Computing Average

1. **You send**: Encrypted student scores to server
2. **Server computes**: Average on encrypted data (without seeing actual scores)
3. **Server returns**: 
   - `Encrypted Result`: `ZW5jcnlwdGVkX2F2ZXJhZ2VfcmVzdWx0XzUw`
   - `Decrypted Result`: `79.33` (the actual average you want)

---

## In Your Interface

When you see:
- **Encrypted Result**: Long base64 string - this is for verification/proof that computation was done privately
- **Decrypted Result**: Number like `79.33` - this is the actual statistic you need

**Note**: In a real production system, you would need the secret key to decrypt. The decrypted result shown here is simulated for demo purposes based on the precomputed statistics from your CSV files.

---

## For ML Predictions

For machine learning predictions (Disease Prediction, Linear Regression):

- **Encrypted Result**: The encrypted prediction vector
- **Decrypted Result**: The actual prediction value
  - Disease Prediction: Probability between 0 and 1 (e.g., `0.456` = 45.6% probability)
  - Linear Regression: Continuous predicted value (e.g., `125.5`)

The decrypted result is what you use to make decisions - it's the model's prediction after all encryption is removed.

