-- Create tables manually
-- Run as: psql -h localhost -U fabe -d goal_breaker -f create_tables.sql

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

CREATE INDEX IF NOT EXISTS ix_goals_id ON goals (id);
CREATE INDEX IF NOT EXISTS ix_goals_description ON goals (description);
CREATE INDEX IF NOT EXISTS ix_subtasks_id ON subtasks (id);
