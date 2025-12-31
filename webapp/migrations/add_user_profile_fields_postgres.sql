-- Migration: Add profile fields to users table
-- Database: PostgreSQL
-- Run this with: psql -h <host> -U <user> -d <database> -f add_user_profile_fields_postgres.sql

BEGIN;

-- Add date_of_birth column
ALTER TABLE users ADD COLUMN IF NOT EXISTS date_of_birth DATE;

-- Add gender column
ALTER TABLE users ADD COLUMN IF NOT EXISTS gender VARCHAR(20);

-- Add country column
ALTER TABLE users ADD COLUMN IF NOT EXISTS country VARCHAR(100);

-- Add language column
ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(50);

-- Add profile_completed column
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_completed BOOLEAN DEFAULT FALSE;

COMMIT;
