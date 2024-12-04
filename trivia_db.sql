CREATE TABLE trivia_questions (
    id SERIAL PRIMARY KEY,             -- Auto-incrementing ID
    question TEXT NOT NULL,            -- The question text
    options JSONB NOT NULL,            -- Options stored in JSONB format
    answer TEXT NOT NULL,              -- The correct answer
    difficulty VARCHAR(50) NOT NULL    -- Difficulty level: easy, medium, or hard
);

INSERT INTO trivia_questions (question, options, answer, difficulty)
VALUES 
('What is the capital of France?', '["Berlin", "Madrid", "Paris", "Rome"]', 'Paris', 'Easy'),
('Who wrote "Romeo and Juliet"?', '["Mark Twain", "Charles Dickens", "William Shakespeare", "Jane Austen"]', 'William Shakespeare', 'Medium'),
('What is 2 + 2?', '["3", "4", "5", "6"]', '4', 'Easy'),
('What is the capital of India?', '["Rajasthan", "Delhi", "Karnataka", "Nepal"]', 'Delhi', 'Medium'),
('What is 5 * 5?', '["15", "20", "25", "30"]', '25', 'Hard'),
('What is the square root of 144?', '["10", "12", "14", "16"]', '12', 'Hard'),
('Who developed the theory of relativity?', '["Newton", "Einstein", "Galileo", "Tesla"]', 'Einstein', 'Hard')
