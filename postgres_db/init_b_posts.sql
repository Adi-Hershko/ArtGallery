CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the 'posts' table
CREATE TABLE IF NOT EXISTS posts (
    post_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) REFERENCES users(username) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    path_to_image VARCHAR(255) NOT NULL,
    path_to_thumbnail VARCHAR(255) NOT NULL,
    insertion_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);