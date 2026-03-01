# Polymarket Trader — Configuration

## API Setup

### Polymarket CLOB Authentication

✅ **Credentials derived from wallet**

Store these securely (e.g., in `.env` or GitHub Secrets):

```
POLYMARKET_API_KEY = "8ae662ee-020d-3651-55f5-6235d5f3582d"
POLYMARKET_API_SECRET = "DL3_ozipxLzX7nwHNEJ_onVuYHwl3B4EP4s9-9uu3sM="
POLYMARKET_API_PASSPHRASE = "c3d8ec3719a8dbaae2385e92d702fb255e4fcbcdc41be577df840336bebb2157"
POLYMARKET_ENDPOINT = "https://clob.polymarket.com"
POLYMARKET_CHAIN_ID = 137  # Polygon mainnet
```

### Wallet Info

- **Address:** Derived from private key (wallet-based auth)
- **Network:** Polygon (137) — lower fees, faster settlements
- **Mode:** Paper Trading (simulated, no real money)

### Funding

- **Paper Trading:** Virtual $500 USDC (simulated)
- **Starting Capital:** $500.00
- **Account Status:** ✅ Ready to trade

---

Status: ✅ Credentials active, ready to scan markets
