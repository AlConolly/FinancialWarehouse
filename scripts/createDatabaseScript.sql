CREATE TABLE COMPANY (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    hq_address VARCHAR(255)
);

CREATE TABLE STOCK (
    id INT PRIMARY KEY,
    symbol VARCHAR(50),
    price NUMBER(10,2),
    volume INT,
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES COMPANY(id)
);

CREATE TABLE DATE_RECORD (
    id INT PRIMARY KEY,
    date_column DATE,
    day INT GENERATED ALWAYS AS (EXTRACT(DAY FROM date_column)) VIRTUAL,
    month INT GENERATED ALWAYS AS (EXTRACT(MONTH FROM date_column)) VIRTUAL,
    quarter INT GENERATED ALWAYS AS (TRUNC((EXTRACT(MONTH FROM date_column))-1)/3 + 1) VIRTUAL,
    year INT GENERATED ALWAYS AS (EXTRACT(YEAR FROM date_column)) VIRTUAL
);

CREATE TABLE INDEX_FUND (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    volume INT
);

CREATE TABLE COMMODITY (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    volume INT
);

CREATE TABLE BOND (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    amount NUMBER(10, 2)
);

CREATE TABLE DAILY_TRANSACTIONS (
    stock_id INT,
    date_id INT,
    commodity_id INT,
    index_fund_id INT,
    bond_id INT,
    price NUMBER(10, 2),
    price_sp500 NUMBER(10, 2),
    price_gold NUMBER(10, 2),
    CONSTRAINT FK_STOCK FOREIGN KEY (stock_id) REFERENCES STOCK(id),
    CONSTRAINT FK_DATE FOREIGN KEY (date_id) REFERENCES DATE_RECORD(id),
    CONSTRAINT FK_COMMODITY FOREIGN KEY (commodity_id) REFERENCES COMMODITY(id),
    CONSTRAINT FK_BOND FOREIGN KEY (bond_id) REFERENCES BOND(id),
    CONSTRAINT FK_INDEX_FUND FOREIGN KEY (index_fund_id) REFERENCES INDEX_FUND(id)
);

SELECT table_name
FROM user_tables;