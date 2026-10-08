# Data

This project uses a manually downloaded delayed SPX option-chain snapshot from Cboe.

For the analysis shown in the repository:

- quote date: 7 October 2026
- expiration: 20 November 2026
- underlying: SPX
- expiration type: Standard

Save the downloaded file as:

```text
data/raw/spx_quotedata.csv
```

The raw CSV is intentionally excluded from version control. The code uses only bid/ask quotes and reconstructs implied volatility rather than relying on Cboe's displayed IV column.
