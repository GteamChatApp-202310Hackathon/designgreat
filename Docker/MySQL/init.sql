START TRANSACTION;

DROP DATABASE IF EXISTS designgreat;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE designgreat;
USE designgreat;
GRANT ALL PRIVILEGES ON designgreat.* TO 'testuser';

CREATE TABLE users (
  id varchar(255) UNIQUE NOT NULL,
  user_name varchar(255) UNIQUE NOT NULL,
  password varchar(100) NOT NULL,
  teacher_password varchar(100),
  email varchar(255) NOT NULL UNIQUE,
  role boolean NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  PRIMARY KEY (id)
);

CREATE TABLE channels (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) UNIQUE NOT NULL,
  channel_name varchar(255) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE messages (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) UNIQUE NOT NULL,
  channel_id bigint UNSIGNED NOT NULL,
  pin_message boolean NOT NULL DEFAULT FALSE,
  message text,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE reactions (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) UNIQUE NOT NULL,
  message_id bigint UNSIGNED NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- データ挿入
INSERT INTO users(id, user_name, password, teacher_password, email, role) VALUES
('970af84c-dd40-47ff-af23-282b72b7cca8', 'GteamUser', SHA2('your-password-here', 256), '1234', 'test@gmail.com',TRUE);

SET @last_user_id = '970af84c-dd40-47ff-af23-282b72b7cca8';

INSERT INTO channels(user_id, channel_name, description) VALUES (@last_user_id, 'Gteam', 'Channel description here.');

SET @last_channel_id = (SELECT LAST_INSERT_ID());

INSERT INTO messages(user_id, channel_id, pin_message, message) VALUES (@last_user_id,@last_channel_id, TRUE, 'Send test message.');

SET @last_message_id = (SELECT LAST_INSERT_ID());

INSERT INTO reactions(user_id, message_id) VALUES (@last_user_id, @last_message_id);

COMMIT;