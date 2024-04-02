CREATE TABLE COMPANY (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100),
    hq_address VARCHAR(255),
    sector VARCHAR(100),
    date_added DATE,
    founded DATE,
    symbol VARCHAR(50)
);

CREATE TABLE STOCK (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company_id INT,
    market_cap NUMBER(10, 2),
    exchange_market VARCHAR(100),
    yield NUMBER(10, 2),
    FOREIGN KEY (company_id) REFERENCES COMPANY(id)
);

CREATE TABLE DATE_RECORD (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_column DATE,
    day INT GENERATED ALWAYS AS (EXTRACT(DAY FROM date_column)) VIRTUAL,
    month INT GENERATED ALWAYS AS (EXTRACT(MONTH FROM date_column)) VIRTUAL,
    quarter INT GENERATED ALWAYS AS (TRUNC((EXTRACT(MONTH FROM date_column))-1)/3 + 1) VIRTUAL,
    year INT GENERATED ALWAYS AS (EXTRACT(YEAR FROM date_column)) VIRTUAL
);

CREATE TABLE INDEX_FUND (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255),
    management_company VARCHAR(255),
    net_asset_value NUMBER(10, 2),
    yield NUMBER(10, 2),
    type VARCHAR(100)
);

CREATE TABLE COMMODITY (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255),
    unit_of_measure VARCHAR(100),
    type VARCHAR(100)
);

CREATE TABLE BOND (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255),
    issuer VARCHAR(255),
    yield NUMBER(10, 2),
    type VARCHAR(100)
);

CREATE TABLE CURRENCY (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(100),
    code VARCHAR(10),
    exhange_rate NUMBER(10, 2)
);

CREATE TABLE DAILY_TRANSACTIONS (
    stock_id INT,
    date_id INT,
    commodity_id INT,
    bond_id INT,
    index_fund_id INT,
    currency_id INT,
    price NUMBER(10, 2),
    symbol VARCHAR(50),
    volume INT,
    open_price NUMBER(10, 2),
    high_price NUMBER(10, 2),
    low_price NUMBER(10, 2),
    price_sp500 NUMBER(10, 2),
    price_gold NUMBER(10, 2),
    price_oil NUMBER(10, 2),
    avg_price_over_time NUMBER(10, 2),
    CONSTRAINT FK_STOCK FOREIGN KEY (stock_id) REFERENCES STOCK(id),
    CONSTRAINT FK_DATE FOREIGN KEY (date_id) REFERENCES DATE_RECORD(id),
    CONSTRAINT FK_COMMODITY FOREIGN KEY (commodity_id) REFERENCES COMMODITY(id),
    CONSTRAINT FK_BOND FOREIGN KEY (bond_id) REFERENCES BOND(id),
    CONSTRAINT FK_INDEX_FUND FOREIGN KEY (index_fund_id) REFERENCES INDEX_FUND(id),
    CONSTRAINT FK_CURRENCY FOREIGN KEY (currency_id) REFERENCES CURRENCY(id)
);

SELECT table_name
FROM user_tables;
