from datetime import datetime

import pandas as pd

from loader import (
    getTransactions, 
    getAllPrices, 
    currentPrice,
)

# -----------------------------
# PART 4: CALLING FUNCTIONS TO PREPARE DATA
# -----------------------------
transactionsDf = getTransactions()
pricesDf = getAllPrices()

# Merge transactions and prices
preparedDf = transactionsDf.merge(pricesDf, on="blockTime", how="left")
preparedDf["costCAD"] = preparedDf["btcValue"] * preparedDf["priceCAD"]
preparedDf = preparedDf.sort_values("blockTime", ascending=False)  # newest first

# -----------------------------
# PART 5: CALLING FUNCTION TO GET LIVE PRICE
# -----------------------------
liveBitcoinPrice = currentPrice()

# -----------------------------
# PART 6: AGGREGATING TOTAL BITCOIN HELD, TOTAL COST, AND CURRENT FUND VALUE
# -----------------------------
totalBitcoinHeld = preparedDf["btcValue"].sum()
totalFiatCost = preparedDf["costCAD"].sum()
currentFundValue = totalBitcoinHeld * liveBitcoinPrice

# -----------------------------
# PART 7: CALCULATING FUND INCEPTION, FUND AGE, AND FUND PNL
# -----------------------------
# Fund inception = oldest transaction
oldestBlockTime = preparedDf["blockTime"].min()
fundInception = datetime.utcfromtimestamp(oldestBlockTime).strftime("%Y-%m-%d")

# Fund age in days
today = datetime.utcnow()
fundAge = (today - datetime.utcfromtimestamp(oldestBlockTime)).days

# Fund PnL
fundPnLFiat = currentFundValue - totalFiatCost
fundPnLPercentage = (fundPnLFiat / totalFiatCost) * 100 if totalFiatCost != 0 else 0