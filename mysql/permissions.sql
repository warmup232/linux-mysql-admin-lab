-- Create application user
CREATE USER 'app_user'@'localhost'
IDENTIFIED BY 'DB password';

-- Grant limited permissions
GRANT SELECT, INSERT, UPDATE, DELETE
ON company_db.*
TO 'app_user'@'localhost';

-- Verify permissions
SHOW GRANTS FOR 'app_user'@'localhost';
