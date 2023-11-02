DROP DATABASE IF EXISTS designgreat;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE designgreat;
USE designgreat;
GRANT ALL PRIVILEGES ON designgreat.* TO 'testuser';

CREATE TABLE roles (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  role_name varchar(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE TABLE users (
  id varchar(255) NOT NULL,
  user_name varchar(255) UNIQUE NOT NULL,
  password varchar(100) NOT NULL,
  teacher_password varchar(100),
  email varchar(255) NOT NULL UNIQUE,
  role_id bigint UNSIGNED NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE channels (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) NOT NULL,
  channel_name varchar(255) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE TABLE messages (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id varchar(255) NOT NULL,
  channels_id bigint UNSIGNED NOT NULL,
  message text,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (channels_id) REFERENCES channels(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE pin_messages (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  message_id bigint UNSIGNED NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user_reactions (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  message_id bigint UNSIGNED NOT NULL,
  reaction_id bigint UNSIGNED NOT NULL,
  user_id varchar(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE icons (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  icon_name varchar(255) NOT NULL,
  image_path varchar(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE TABLE reactions (
  id bigint UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  reaction_name varchar(255) NOT NULL,
  icon_id bigint UNSIGNED NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  FOREIGN KEY (icon_id) REFERENCES icons(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- データ挿入
INSERT INTO roles(role_name) VALUES ('teacher');
INSERT INTO users(id, user_name, password, teacher_password, email, role_id) VALUES
('970af84c-dd40-47ff-af23-282b72b7cca8', 'GteamUser', '37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '1234', 'test@gmail.com', 1);
INSERT INTO channels(user_id, channel_name, description) VALUES ('970af84c-dd40-47ff-af23-282b72b7cca8', 'Gteam', 'hogehogehoge');
INSERT INTO messages(user_id, channels_id, message) VALUES ('970af84c-dd40-47ff-af23-282b72b7cca8', 1, 'Send test message.');
INSERT INTO pin_messages(message_id) VALUES (1);
INSERT INTO user_reactions(message_id, reaction_id, user_id) VALUES (1, 1, '970af84c-dd40-47ff-af23-282b72b7cca8');
INSERT INTO icons(icon_name, image_path) VALUES ('testIcon', 'iconImagePath');
INSERT INTO reactions(reaction_name, icon_id) VALUES ('smile', 1);
