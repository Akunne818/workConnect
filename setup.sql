-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS workConnect_dev_db;
CREATE USER IF NOT EXISTS 'workConnect_dev'@'localhost' IDENTIFIED BY 'workConnect_dev_pwd';
GRANT ALL PRIVILEGES ON `workConnect_dev_db`.* TO 'workConnect_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'workConnect_dev'@'localhost';
FLUSH PRIVILEGES;
