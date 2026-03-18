-- Create tables manually
-- Run as: psql -h localhost -U app_user -d data_store -f create_tables.sql

CREATE TABLE IF NOT EXISTS goals (
    id SERIAL NOT NULL,
    description VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS subtasks (
    id SERIAL NOT NULL,
    goal_id INTEGER,
    description VARCHAR,
    complexity_score INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(goal_id) REFERENCES goals (id)
);

CREATE INDEX IF NOT EXISTS ix_goals_description ON goals (description);
