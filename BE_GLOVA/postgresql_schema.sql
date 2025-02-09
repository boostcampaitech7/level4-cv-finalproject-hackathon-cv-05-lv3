CREATE TABLE public.clova_answers (
    answer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    answer_text JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE public.user_questions (
    question_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    question_text JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
