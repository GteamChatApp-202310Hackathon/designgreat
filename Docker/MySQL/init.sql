START TRANSACTION;

DROP DATABASE IF EXISTS designgreat;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE designgreat;
USE designgreat;
GRANT ALL PRIVILEGES ON designgreat.* TO 'testuser';

CREATE TABLE users (
  id varchar(255) NOT NULL,
  user_name varchar(255) UNIQUE NOT NULL,
  password varchar(100) NOT NULL,
  teacher_password varchar(100),
  email varchar(255) NOT NULL UNIQUE,
  role boolean NOT NULL DEFAULT FALSE,,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL
  PRIMARY KEY (id)
);

CREATE TABLE channels (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) NOT NULL,
  channel_name varchar(255) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE messages (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) NOT NULL,
  channels_id bigint UNSIGNED NOT NULL,
  pin_message boolean NOT NULL DEFAULT FALSE,
  message text,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (channels_id) REFERENCES channels(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user_reactions (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  message_id bigint UNSIGNED NOT NULL,
  reaction_id bigint UNSIGNED NOT NULL,
  user_id varchar(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,
  UNIQUE INDEX user_message_reaction_unique (user_id, message_id, reaction_id),
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (reaction_id) REFERENCES reactions(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE reactions (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  reaction_name varchar(255) NOT NULL,
  icon_name varchar(255) NOT NULL,
  image_path varchar(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL
);

-- データ挿入
INSERT INTO users(id, user_name, password, teacher_password, email, role) VALUES
('970af84c-dd40-47ff-af23-282b72b7cca8', 'GteamUser', SHA2('your-password-here', 256), '1234', 'test@gmail.com',TRUE);

SET @last_user_id = LAST_INSERT_ID();

INSERT INTO channels(user_id, channel_name, description) VALUES (@last_user_id, 'Gteam', 'Channel description here.');

SET @last_channel_id = LAST_INSERT_ID();

INSERT INTO messages(user_id, channels_id, pin_message, message) VALUES (@last_user_id,@last_channel_id, TRUE, 'Send test message.');

SET @last_message_id = LAST_INSERT_ID();

INSERT INTO reactions(reaction_name, icon_name, image_path) VALUES ('smile','testIcon', 'iconImagePath');

SET @last_reaction_id = LAST_INSERT_ID();

INSERT INTO user_reactions(message_id, reaction_id, user_id) VALUES (@last_message_id, @last_reaction_id, @last_user_id);

COMMIT;