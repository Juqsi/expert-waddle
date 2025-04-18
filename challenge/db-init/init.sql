CREATE DATABASE IF NOT EXISTS ctf;
USE ctf;

CREATE TABLE IF NOT EXISTS user (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(512) NOT NULL,
    isAdmin BOOLEAN NOT NULL DEFAULT FALSE
    );

SET @salt = UUID();
SET @hash = SHA2(CONCAT(@salt, 'meredith8outfit0GORDY*dale'), 256);

INSERT INTO user (username, password, isAdmin)
VALUES (
           'testuser',
           CONCAT(@salt, ':', @hash),
           FALSE
       );
