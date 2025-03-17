-- Enable the uuid-ossp extension if it's not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE certifications (
    id UUID PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    passing_score INTEGER NOT NULL DEFAULT 70
);

CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    certification_id UUID NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR NOT NULL CHECK (question_type IN ('multiple_choice', 'single_choice')),
    answer_choices JSONB NOT NULL,
    correct_answer JSONB NOT NULL,
    FOREIGN KEY (certification_id) REFERENCES certifications(id) ON DELETE CASCADE
);

CREATE TABLE exam_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    certification_id UUID NOT NULL,
    num_questions INTEGER NOT NULL CHECK (num_questions > 0),
    time_limit INTEGER NOT NULL CHECK (time_limit >= 0),
    exam_date TIMESTAMPTZ DEFAULT NOW(),
    score INTEGER NOT NULL CHECK (score >= 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (certification_id) REFERENCES certifications(id) ON DELETE CASCADE,
    passed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE exam_attempt_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_attempt_id UUID NOT NULL,
    question_id UUID NOT NULL,
    user_answer JSONB NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (exam_attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

