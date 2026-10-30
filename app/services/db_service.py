"""
Database Service for Smart Resume Skill-Gap & Career Predictor
Dual-mode:
- Connects to Neon PostgreSQL in production when DATABASE_URL is set.
- Automatically falls back to SQLite locally without requiring external drivers.
"""
import os
import json
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

class DatabaseService:
    def __init__(self):
        self.is_postgres = False
        self.db_url = DATABASE_URL
        self._init_db()

    def _get_pg_connection(self):
        # Fix Render/Heroku postgres:// -> postgresql://
        url = self.db_url
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        
        try:
            import psycopg2
            # Neon requires sslmode=require if not in query
            if "sslmode" not in url:
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}sslmode=require"
            return psycopg2.connect(url)
        except Exception:
            return None

    def _get_sqlite_connection(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "resumepredictor.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_connection(self):
        if self.db_url and ("postgres" in self.db_url):
            pg_conn = self._get_pg_connection()
            if pg_conn:
                self.is_postgres = True
                return pg_conn
        
        self.is_postgres = False
        return self._get_sqlite_connection()

    def _init_db(self):
        """
        Creates the assessments table if it doesn't already exist.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.is_postgres:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS assessments (
                    id VARCHAR(64) PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    candidate_name VARCHAR(255),
                    target_role VARCHAR(255),
                    overall_match_score REAL,
                    salary_median INTEGER,
                    fit_tier VARCHAR(100),
                    matched_skills TEXT,
                    missing_skills TEXT,
                    payload JSONB
                );
                """
            else:
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS assessments (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    candidate_name TEXT,
                    target_role TEXT,
                    overall_match_score REAL,
                    salary_median INTEGER,
                    fit_tier TEXT,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    payload TEXT
                );
                """

            cursor.execute(create_table_sql)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[DB] Database initialization warning (falling back gracefully): {e}")

    def save_assessment(self, analysis_data: Dict[str, Any]) -> str:
        """
        Saves analysis result to database and returns a shareable assessment ID.
        """
        assessment_id = uuid.uuid4().hex[:12]
        profile = analysis_data.get("profile", {})
        fit = analysis_data.get("fit_analysis", {})
        salary = analysis_data.get("salary_prediction", {})
        
        cand_name = profile.get("candidate_name") or "Anonymous Candidate"
        target_role = fit.get("target_role") or "Benchmark Role"
        score = float(fit.get("overall_match_score") or 0.0)
        salary_med = int(salary.get("median") or 0)
        tier = fit.get("match_tier") or "Evaluated"
        matched = json.dumps(fit.get("matched_skills") or [])
        missing = json.dumps(fit.get("missing_skills") or [])
        payload_str = json.dumps(analysis_data)

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.is_postgres:
                insert_sql = """
                INSERT INTO assessments 
                (id, candidate_name, target_role, overall_match_score, salary_median, fit_tier, matched_skills, missing_skills, payload)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(insert_sql, (assessment_id, cand_name, target_role, score, salary_med, tier, matched, missing, payload_str))
            else:
                insert_sql = """
                INSERT INTO assessments 
                (id, candidate_name, target_role, overall_match_score, salary_median, fit_tier, matched_skills, missing_skills, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """
                cursor.execute(insert_sql, (assessment_id, cand_name, target_role, score, salary_med, tier, matched, missing, payload_str))

            conn.commit()
            cursor.close()
            conn.close()
            return assessment_id
        except Exception as e:
            print(f"[DB Error] Save assessment failed: {e}")
            return assessment_id

    def get_assessment(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a saved assessment by ID.
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.is_postgres:
                query_sql = "SELECT payload FROM assessments WHERE id = %s;"
                cursor.execute(query_sql, (assessment_id,))
            else:
                query_sql = "SELECT payload FROM assessments WHERE id = ?;"
                cursor.execute(query_sql, (assessment_id,))

            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                raw_payload = row[0]
                if isinstance(raw_payload, str):
                    return json.loads(raw_payload)
                return raw_payload
            return None
        except Exception as e:
            print(f"[DB Error] Get assessment failed: {e}")
            return None

db_service = DatabaseService()
