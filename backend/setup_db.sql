-- Run this as postgres superuser to grant permissions
-- psql -h localhost -U postgres -d app_database -f setup_db.sql

-- Ensure the application user exists before granting permissions
CREATE USER IF NOT EXISTS app_user;

GRANT ALL PRIVILEGES ON DATABASE app_database TO app_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO app_user;
GRANT CREATE ON SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO app_user;
