-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    password BYTEA NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);
