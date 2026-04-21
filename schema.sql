-- ============================================
-- PATENT DATABASE SCHEMA
-- ============================================
-- Generated from PVGPATDIS dataset
-- 4 tables as required by assignment

-- Drop existing tables
DROP TABLE IF EXISTS patent_relationships;
DROP TABLE IF EXISTS patents;
DROP TABLE IF EXISTS inventors;
DROP TABLE IF EXISTS companies;

-- Table 1: patents
CREATE TABLE patents (
    patent_id TEXT PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    filing_date TEXT,
    year INTEGER
);

-- Table 2: inventors
CREATE TABLE inventors (
    inventor_id TEXT PRIMARY KEY,
    name TEXT,
    country TEXT
);

-- Table 3: companies (assignees)
CREATE TABLE companies (
    company_id TEXT PRIMARY KEY,
    name TEXT
);

-- Table 4: relationships
CREATE TABLE patent_relationships (
    patent_id TEXT,
    inventor_id TEXT,
    company_id TEXT,
    FOREIGN KEY (patent_id) REFERENCES patents(patent_id),
    FOREIGN KEY (inventor_id) REFERENCES inventors(inventor_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Indexes for performance
CREATE INDEX idx_patents_year ON patents(year);
CREATE INDEX idx_relationships_patent ON patent_relationships(patent_id);
CREATE INDEX idx_relationships_inventor ON patent_relationships(inventor_id);
CREATE INDEX idx_relationships_company ON patent_relationships(company_id);

-- ============================================
-- THE 7 REQUIRED QUERIES
-- ============================================

-- Q1: Top Inventors
-- SELECT i.name, COUNT(DISTINCT pr.patent_id) as patent_count
-- FROM inventors i
-- JOIN patent_relationships pr ON i.inventor_id = pr.inventor_id
-- GROUP BY i.name
-- ORDER BY patent_count DESC
-- LIMIT 10;

-- Q2: Top Companies
-- SELECT c.name, COUNT(DISTINCT pr.patent_id) as patent_count
-- FROM companies c
-- JOIN patent_relationships pr ON c.company_id = pr.company_id
-- GROUP BY c.name
-- ORDER BY patent_count DESC
-- LIMIT 10;

-- Q3: Top Countries
-- SELECT i.country, COUNT(DISTINCT pr.patent_id) as patent_count
-- FROM inventors i
-- JOIN patent_relationships pr ON i.inventor_id = pr.inventor_id
-- WHERE i.country != 'Unknown'
-- GROUP BY i.country
-- ORDER BY patent_count DESC
-- LIMIT 10;

-- Q4: Trends Over Time
-- SELECT year, COUNT(*) as patent_count
-- FROM patents
-- WHERE year > 2000
-- GROUP BY year
-- ORDER BY year;

-- Q5: JOIN Query (Combine all tables)
-- SELECT p.patent_id, p.title, i.name as inventor_name, c.name as company_name
-- FROM patents p
-- JOIN patent_relationships pr ON p.patent_id = pr.patent_id
-- JOIN inventors i ON pr.inventor_id = i.inventor_id
-- JOIN companies c ON pr.company_id = c.company_id
-- LIMIT 10;

-- Q6: CTE Query (WITH statement)
-- WITH inventor_stats AS (
--     SELECT i.name, COUNT(DISTINCT pr.patent_id) as patent_count
--     FROM inventors i
--     JOIN patent_relationships pr ON i.inventor_id = pr.inventor_id
--     GROUP BY i.name
-- )
-- SELECT name, patent_count,
--        ROUND(100.0 * patent_count / SUM(patent_count) OVER(), 2) as percentage
-- FROM inventor_stats
-- ORDER BY patent_count DESC
-- LIMIT 10;

-- Q7: Ranking Query (Window functions)
-- SELECT i.name, COUNT(DISTINCT pr.patent_id) as patent_count,
--        RANK() OVER (ORDER BY COUNT(DISTINCT pr.patent_id) DESC) as rank
-- FROM inventors i
-- JOIN patent_relationships pr ON i.inventor_id = pr.inventor_id
-- GROUP BY i.name
-- ORDER BY rank
-- LIMIT 10;
