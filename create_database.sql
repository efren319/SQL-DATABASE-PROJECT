-- Create tables
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY,
    department TEXT UNIQUE NOT NULL,
    allocated REAL NOT NULL,
    spent REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    budget REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    comment TEXT NOT NULL
);

-- Seed initial data (only if tables are empty; check in Python to avoid duplicates)
INSERT OR IGNORE INTO budget (department, allocated, spent) VALUES
('Department of Education', 500000, 300000),
('Department of Health', 700000, 450000),
('Infrastructure Project A', 1000000, 600000),
('Infrastructure Project B', 800000, 200000);

INSERT OR IGNORE INTO projects (name, status, budget) VALUES
('School Renovation', 'In Progress', 500000),
('Hospital Upgrade', 'Completed', 700000),
('Road Construction', 'Planning', 1000000),
('Bridge Repair', 'In Progress', 800000);