# Useful Oracle SQL Statements

## Fill in the fact table for any missing measures (Ex: Gold)

```sql
UPDATE daily_transactions dt1
SET dt1.price_gold = (
    SELECT dt2.price
    FROM daily_transactions dt2
    WHERE dt2.date_id = dt1.date_id AND dt2.symbol = 'GOLD'
)
WHERE EXISTS (
    SELECT 1
    FROM daily_transactions dt3
    WHERE dt3.date_id = dt1.date_id AND dt3.symbol = 'GOLD'
);
```

## Create our measure helper table that speeds up the process of filling in measures

```sql
CREATE TABLE MEASURE_HELPER AS
SELECT DISTINCT date_id, price_gold, price_oil, price_sp500
FROM daily_transactions;
```