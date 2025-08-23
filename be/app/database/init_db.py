import mysql.connector
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def init_database():
    """Initialize the database if it doesn't exist"""
    # Connect to MySQL server without specifying a database
    connection = None
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Handle empty password case
            connection_params = {
                'host': DB_HOST,
                'port': DB_PORT,
                'user': DB_USER
            }
            if DB_PASSWORD:
                connection_params['password'] = DB_PASSWORD
            
            connection = mysql.connector.connect(**connection_params)
            break
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            retry_count += 1
            if retry_count < max_retries:
                print(f"Retrying in 5 seconds... (Attempt {retry_count}/{max_retries})")
                time.sleep(5)
            else:
                print("Failed to connect to MySQL after multiple attempts")
                return False
    
    if not connection:
        return False
    
    cursor = connection.cursor()
    
    try:
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database '{DB_NAME}' created or already exists")
        
        # Use the database
        cursor.execute(f"USE {DB_NAME}")
        
        # Create tables if they don't exist
        # This is a fallback in case SQLAlchemy doesn't create them
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
            password_reset_token VARCHAR(255) NULL,
            password_reset_token_expiry DATETIME NULL
        )
        """)
        
        # Conversations table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)
        
        # Messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            conversation_id VARCHAR(36) NOT NULL,
            content TEXT NOT NULL,
            type VARCHAR(10) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        )
        """)
        
        # User documents table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            conversation_id VARCHAR(36) NULL,
            document_id VARCHAR(255) NULL,
            filename VARCHAR(255) NOT NULL,
            file_size BIGINT NULL,
            status VARCHAR(50) NULL DEFAULT 'processing',
            s3_key VARCHAR(255) NULL,
            s3_url VARCHAR(255) NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
        )
        """)
        
        # Contact messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        connection.commit()
        print("Tables created or already exist")
        return True
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
        
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    init_database()