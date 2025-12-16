# Writer

## Payee Resolution API

The application exposes an API endpoint to standardize merchant names from raw transaction descriptions.

### Endpoint

`GET /payees/real-name`

### Query Parameters

- `payee` (string, required): The raw payee string from the transaction (e.g., "7-ELEVEN 23020 SEATTLE WA").

### Response

Returns a JSON object with:
- `real_name` (string): The standardized merchant name.
- `confidence` (float): A score between 0.0 and 1.0 indicating certainty.

### Examples

**Request:**
```http
GET /payees/real-name?payee=7-ELEVEN%2023020%20SEATTLE%20WA
```

**Response:**
```json
{
  "real_name": "7-Eleven",
  "confidence": 0.95
}
```

**Request:**
```http
GET /payees/real-name?payee=Unknown%20Store%20123
```

**Response:**
```json
{
  "real_name": "Unknown Store",
  "confidence": 0.4
}
```

### Logic Overview

The resolution logic uses a hybrid approach:
1.  **Cleaning:** Removes digits, common location codes (states, countries), and expands abbreviations.
2.  **Dictionary Match:** Checks against a list of known merchants.
3.  **Fuzzy Matching:** Finds similar names using string distance metrics.
4.  **Clustering (ML):** Uses TF-IDF and K-Means clustering to identify common payee patterns that aren't in the manual dictionary.
