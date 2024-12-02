-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS game_archive 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 데이터베이스 사용
USE game_archive;

-- User_table
CREATE TABLE IF NOT EXISTS User_table (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(10) NOT NULL,
    password VARCHAR(10) NOT NULL,
    email VARCHAR(15) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login DATETIME
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Content_table
CREATE TABLE IF NOT EXISTS Content_table (
    content_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    description VARCHAR(200)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Comment_table
CREATE TABLE IF NOT EXISTS Comment_table (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (content_id) REFERENCES Content_table(content_id),
    FOREIGN KEY (user_id) REFERENCES User_table(user_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Question_table
CREATE TABLE IF NOT EXISTS Question_table (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(45) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User_table(user_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Answer_table
CREATE TABLE IF NOT EXISTS Answer_table (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES Question_table(question_id),
    FOREIGN KEY (user_id) REFERENCES User_table(user_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Guide_table 
CREATE TABLE IF NOT EXISTS Guide_table (
    guide_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    game_title VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    game_name VARCHAR(50),
    name VARCHAR(50), 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User_table(user_id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- News_table
CREATE TABLE IF NOT EXISTS News_table (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    news_title VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    auth VARCHAR(20),
    image_url VARCHAR(255), 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;