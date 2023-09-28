DROP TABLE IF EXISTS deals;

DROP TABLE IF EXISTS places;

CREATE TABLE deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place TEXT NOT NULL,
    category TEXT NOT NULL,
    dates TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    title TEXT NOT NULL,
    notes TEXT,
    last_verified TEXT
);

CREATE TABLE places (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    _address TEXT,
    category TEXT,
    open_time TEXT,
    close_time TEXT,
    notes TEXT
);