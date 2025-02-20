from app.services.vector_store_pg import PostgresVectorStore
from app.core.config import settings
from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo=f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")

vector_store = PostgresVectorStore(pool)

with vector_store.pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            text TEXT,
            document_name TEXT,
            document_id TEXT,
            paragraph_id INT,
            document_hash TEXT,
            embedding vector(1536)
        );
        """)
    conn.commit()
    
    # with conn.cursor() as cur:
    #     cur.execute(
    #     """
    #         -- Users Table (Personal Profile)
    #         CREATE TABLE users (
    #             user_id SERIAL PRIMARY KEY,
    #             first_name VARCHAR(50) NOT NULL,
    #             last_name VARCHAR(50) NOT NULL,
    #             date_of_birth DATE NOT NULL,
    #             gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    #             phone VARCHAR(20),
    #             email VARCHAR(100) UNIQUE NOT NULL,
    #             address TEXT,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );

    #         -- Medical Records Table (Stores All Uploaded Documents)
    #         CREATE TABLE medical_records (
    #             record_id SERIAL PRIMARY KEY,
    #             user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    #             record_type VARCHAR(50) CHECK (record_type IN ('Diagnosis', 'Prescription', 'Lab Report', 'Imaging', 'Consultation', 'Other')),
    #             description TEXT,
    #             document_url VARCHAR(255),
    #             uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );

    #         -- Diagnoses Table (Tracks Medical Conditions)
    #         CREATE TABLE diagnoses (
    #             diagnosis_id SERIAL PRIMARY KEY,
    #             user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    #             doctor_name VARCHAR(100) NOT NULL,  -- Just store the doctor's name as text
    #             condition VARCHAR(255) NOT NULL,
    #             severity VARCHAR(50),
    #             diagnosis_date DATE NOT NULL,
    #             notes TEXT,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );

    #         -- Prescriptions Table (Tracks Medications)
    #         CREATE TABLE prescriptions (
    #             prescription_id SERIAL PRIMARY KEY,
    #             user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    #             doctor_name VARCHAR(100) NOT NULL,  -- Just store the doctor's name as text
    #             medication VARCHAR(255) NOT NULL,
    #             dosage VARCHAR(50) NOT NULL,
    #             frequency VARCHAR(50) NOT NULL,
    #             start_date DATE NOT NULL,
    #             end_date DATE,
    #             instructions TEXT,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );

    #         -- Lab Results Table (Stores Test Results)
    #         CREATE TABLE lab_results (
    #             lab_id SERIAL PRIMARY KEY,
    #             user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    #             test_name VARCHAR(255) NOT NULL,
    #             result_value TEXT,
    #             reference_range VARCHAR(100),
    #             test_date DATE NOT NULL,
    #             notes TEXT,
    #             document_url VARCHAR(255),
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );

    #         -- Vaccination Records Table
    #         CREATE TABLE vaccinations (
    #             vaccination_id SERIAL PRIMARY KEY,
    #             user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    #             vaccine_name VARCHAR(255) NOT NULL,
    #             dose VARCHAR(50),
    #             vaccination_date DATE NOT NULL,
    #             notes TEXT,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         );

          
    #     """)
    # conn.commit()
    
    
    
    
    
    conn.close()
vector_store.pool.close()