# Stock prediction and stock safety, using SciKit-Learn on a New York stock exchange dataset.

The datafile contains stock exchange data. The symbol corresponds to a company. Each row has the lowest price, highest price, opening price, closing price and volume of traded shares.
These attributes are used for two tasks:
- Predict the price for the next day (Regression).
- Predict if the stock is "safe for investment", i.e. has small variance. Since there is not data specifically on safety, k-means clustering (2 clusters) is used on the price's approximate variances and their closing prices' variance. The "safe" shares are the ones "bellow" the "lower" centroid.

**Usage:** python main.py *choice* [company=*LABEL*]
Where choice is one of:
- "stock" or "prediction" for stock next day prediction.
- "share" or "safety" for stock safety.
And company label is one of the companies' stock exchange labels. The default test value is ORCL (Oracle).
