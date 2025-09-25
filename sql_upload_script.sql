-- Upload Sample Flight Data to Exasol
-- =====================================
-- Run this script in your Exasol database to create and populate the FLIGHTS table

-- Step 1: Create the FLIGHTS schema
CREATE SCHEMA IF NOT EXISTS FLIGHTS;

-- Step 2: Drop table if exists (for clean reload)
DROP TABLE IF EXISTS FLIGHTS.FLIGHTS;

-- Step 3: Create the FLIGHTS table
CREATE TABLE FLIGHTS.FLIGHTS (
    FLIGHT_DATE DATE,
    OP_CARRIER VARCHAR(10),
    FLIGHT_NUM DECIMAL(18,0),
    ORIGIN CHAR(3),
    DEST CHAR(3),
    CRS_DEP_TIME VARCHAR(10),
    DEP_DELAY DOUBLE,
    DEP_DEL15 DOUBLE,
    DISTANCE DOUBLE,
    DAY_OF_WEEK DECIMAL(1,0),
    MONTH DECIMAL(18,0),
    CANCELLED DOUBLE
);

-- Step 4: Insert sample data
INSERT INTO FLIGHTS.FLIGHTS VALUES
('2024-01-15', 'AA', 1234, 'LAX', 'JFK', '1430', 5.2, 0, 2475, 1, 1, 0),
('2024-01-15', 'UA', 5678, 'ORD', 'ATL', '0800', 25.8, 1, 606, 1, 1, 0),
('2024-01-15', 'DL', 9012, 'JFK', 'LAX', '1845', -3.1, 0, 2475, 1, 1, 0),
('2024-01-15', 'SW', 3456, 'ATL', 'ORD', '1200', 8.7, 0, 606, 1, 1, 0),
('2024-01-15', 'AS', 7890, 'SEA', 'SFO', '0630', 45.3, 1, 679, 1, 1, 0),
('2024-01-16', 'AA', 2345, 'DFW', 'LAX', '1015', 12.4, 0, 1235, 2, 1, 0),
('2024-01-16', 'UA', 6789, 'LAX', 'DEN', '1630', 18.9, 1, 862, 2, 1, 0),
('2024-01-16', 'DL', 0123, 'MIA', 'JFK', '0745', 2.1, 0, 1090, 2, 1, 0),
('2024-01-16', 'SW', 4567, 'PHX', 'LAS', '2100', -1.5, 0, 256, 2, 1, 0),
('2024-01-16', 'B6', 8901, 'BOS', 'LAX', '1320', 67.2, 1, 2611, 2, 1, 0),
('2024-01-17', 'AA', 3456, 'JFK', 'MIA', '0900', 15.6, 1, 1090, 3, 1, 0),
('2024-01-17', 'UA', 7890, 'DEN', 'ORD', '1445', 4.8, 0, 888, 3, 1, 0),
('2024-01-17', 'DL', 1234, 'ATL', 'LAX', '1130', 38.7, 1, 1946, 3, 1, 0),
('2024-01-17', 'SW', 5678, 'LAX', 'PHX', '1750', 7.3, 0, 370, 3, 1, 0),
('2024-01-17', 'AS', 9012, 'SFO', 'SEA', '1955', -2.8, 0, 679, 3, 1, 0),
('2024-01-18', 'AA', 4567, 'ORD', 'JFK', '0715', 29.4, 1, 740, 4, 1, 0),
('2024-01-18', 'UA', 8901, 'LAX', 'ORD', '1200', 11.2, 0, 1745, 4, 1, 0),
('2024-01-18', 'DL', 2345, 'JFK', 'ATL', '1425', 6.9, 0, 760, 4, 1, 0),
('2024-01-18', 'SW', 6789, 'ATL', 'MIA', '1800', 22.1, 1, 594, 4, 1, 0),
('2024-01-18', 'B6', 0123, 'LAX', 'JFK', '2030', 51.8, 1, 2475, 4, 1, 0),
('2024-01-19', 'AA', 5678, 'MIA', 'ATL', '0830', 3.7, 0, 594, 5, 1, 0),
('2024-01-19', 'UA', 9012, 'JFK', 'LAX', '1345', 35.6, 1, 2475, 5, 1, 0),
('2024-01-19', 'DL', 3456, 'LAX', 'ATL', '1610', 14.2, 0, 1946, 5, 1, 0),
('2024-01-19', 'SW', 7890, 'ORD', 'DEN', '1920', 8.9, 0, 888, 5, 1, 0),
('2024-01-19', 'AS', 1234, 'SEA', 'LAX', '0645', 19.7, 1, 954, 5, 1, 0),
('2024-01-20', 'AA', 6789, 'ATL', 'JFK', '1100', 42.3, 1, 760, 6, 1, 0),
('2024-01-20', 'UA', 0123, 'LAX', 'SEA', '1535', 7.1, 0, 954, 6, 1, 0),
('2024-01-20', 'DL', 4567, 'JFK', 'ORD', '1925', -0.8, 0, 740, 6, 1, 0),
('2024-01-20', 'SW', 8901, 'DEN', 'LAX', '1255', 26.5, 1, 862, 6, 1, 0),
('2024-01-20', 'B6', 2345, 'MIA', 'JFK', '0520', 33.9, 1, 1090, 6, 1, 0);

-- Step 5: Verify the data
SELECT 
    COUNT(*) as total_flights,
    COUNT(DISTINCT OP_CARRIER) as airlines,
    COUNT(DISTINCT ORIGIN) as origins,
    ROUND(AVG(DEP_DELAY), 2) as avg_delay,
    ROUND(SUM(DEP_DEL15) * 100.0 / COUNT(*), 2) as delay_rate_pct
FROM FLIGHTS.FLIGHTS;

-- Step 6: Show sample data
SELECT * FROM FLIGHTS.FLIGHTS LIMIT 5;

-- Success! Your FLIGHTS.FLIGHTS table is ready for the ML tutorial.