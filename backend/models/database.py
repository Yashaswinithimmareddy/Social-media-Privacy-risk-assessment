"""
Social Media Privacy Risk Assessment Framework
Database Layer (SQLite)

Implements Privacy-by-Design and Data Minimization principles.
Stores strictly non-PII risk telemetry: assessment IDs, scores, finding types,
and actionable guidance. Never stores user names, emails, phones, or credentials.
"""

import sqlite3
import json
import os
from typing import Dict, Any, List, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "privacy_risk.db")

def get_db_connection(db_path: str = DB_FILE) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = DB_FILE) -> None:
    """Initializes the database schema if tables do not already exist."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 1. Master Assessments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            assessment_id TEXT PRIMARY KEY,
            overall_score REAL NOT NULL,
            risk_level TEXT NOT NULL,
            created_at TEXT NOT NULL,
            simulated_score REAL,
            points_reduced REAL
        )
    """)

    # 2. Category Scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_scores (
            category_score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id TEXT NOT NULL,
            category TEXT NOT NULL,
            category_name TEXT NOT NULL,
            score REAL NOT NULL,
            weight REAL NOT NULL,
            FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
        )
    """)

    # 3. Findings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id TEXT NOT NULL,
            category TEXT NOT NULL,
            finding_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technical_impact TEXT,
            FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
        )
    """)

    # 4. Recommendations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assessment_id TEXT NOT NULL,
            finding_type TEXT NOT NULL,
            category TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            step_by_step TEXT,
            priority TEXT NOT NULL,
            FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
        )
    """)

    # 5. Anonymized Responses Table (Key/Value tokens only, Zero PII)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses_anonymized (
            assessment_id TEXT PRIMARY KEY,
            responses_json TEXT NOT NULL,
            FOREIGN KEY (assessment_id) REFERENCES assessments (assessment_id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def save_assessment(assessment_result: Dict[str, Any], db_path: str = DB_FILE) -> str:
    """
    Saves assessment telemetry to SQLite database following Privacy by Design.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    aid = assessment_result["assessment_id"]
    overall_score = assessment_result["overall_score"]
    risk_level = assessment_result["risk_level"]
    created_at = assessment_result["created_at"]

    cursor.execute("""
        INSERT OR REPLACE INTO assessments (assessment_id, overall_score, risk_level, created_at)
        VALUES (?, ?, ?, ?)
    """, (aid, overall_score, risk_level, created_at))

    # Save category scores
    for cat_id, cat_info in assessment_result.get("category_scores", {}).items():
        cursor.execute("""
            INSERT INTO category_scores (assessment_id, category, category_name, score, weight)
            VALUES (?, ?, ?, ?, ?)
        """, (aid, cat_id, cat_info["name"], cat_info["score"], cat_info["weight"]))

    # Save findings
    for finding in assessment_result.get("findings", []):
        cursor.execute("""
            INSERT INTO findings (assessment_id, category, finding_type, severity, title, description, technical_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (aid, finding["category"], finding["finding_id"], finding["severity"],
              finding["title"], finding["description"], finding["technical_impact"]))

    # Save recommendations
    for rec in assessment_result.get("recommendations", []):
        cursor.execute("""
            INSERT INTO recommendations (assessment_id, finding_type, category, recommendation, step_by_step, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (aid, rec["finding_id"], rec["category"], rec["action"], rec["step_by_step"], rec["priority"]))

    # Save anonymized cleaned responses for simulation retrieval
    if "cleaned_responses" in assessment_result:
        cursor.execute("""
            INSERT OR REPLACE INTO responses_anonymized (assessment_id, responses_json)
            VALUES (?, ?)
        """, (aid, json.dumps(assessment_result["cleaned_responses"])))

    conn.commit()
    conn.close()
    return aid


def update_assessment_simulation(
    assessment_id: str, 
    simulated_score: float, 
    points_reduced: float, 
    db_path: str = DB_FILE
) -> None:
    """Updates simulation results on an existing assessment."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE assessments 
        SET simulated_score = ?, points_reduced = ?
        WHERE assessment_id = ?
    """, (simulated_score, points_reduced, assessment_id))
    conn.commit()
    conn.close()


def get_assessment(assessment_id: str, db_path: str = DB_FILE) -> Optional[Dict[str, Any]]:
    """Retrieves complete assessment details by ID."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assessments WHERE assessment_id = ?", (assessment_id,))
    assessment_row = cursor.fetchone()
    if not assessment_row:
        conn.close()
        return None

    # Retrieve categories
    cursor.execute("SELECT * FROM category_scores WHERE assessment_id = ?", (assessment_id,))
    cat_rows = cursor.fetchall()
    category_scores = {}
    for r in cat_rows:
        category_scores[r["category"]] = {
            "category_id": r["category"],
            "name": r["category_name"],
            "score": r["score"],
            "weight": r["weight"]
        }

    # Retrieve findings
    cursor.execute("SELECT * FROM findings WHERE assessment_id = ?", (assessment_id,))
    finding_rows = cursor.fetchall()
    findings = []
    for r in finding_rows:
        findings.append({
            "finding_id": r["finding_type"],
            "category": r["category"],
            "severity": r["severity"],
            "title": r["title"],
            "description": r["description"],
            "technical_impact": r["technical_impact"]
        })

    # Retrieve recommendations
    cursor.execute("SELECT * FROM recommendations WHERE assessment_id = ?", (assessment_id,))
    rec_rows = cursor.fetchall()
    recommendations = []
    for r in rec_rows:
        recommendations.append({
            "finding_id": r["finding_type"],
            "category": r["category"],
            "action": r["recommendation"],
            "step_by_step": r["step_by_step"],
            "priority": r["priority"]
        })

    # Retrieve responses
    cursor.execute("SELECT responses_json FROM responses_anonymized WHERE assessment_id = ?", (assessment_id,))
    resp_row = cursor.fetchone()
    responses = json.loads(resp_row["responses_json"]) if resp_row else {}

    conn.close()

    return {
        "assessment_id": assessment_row["assessment_id"],
        "overall_score": assessment_row["overall_score"],
        "risk_level": assessment_row["risk_level"],
        "created_at": assessment_row["created_at"],
        "simulated_score": assessment_row["simulated_score"],
        "points_reduced": assessment_row["points_reduced"],
        "category_scores": category_scores,
        "findings": findings,
        "recommendations": recommendations,
        "cleaned_responses": responses
    }


def delete_assessment(assessment_id: str, db_path: str = DB_FILE) -> bool:
    """Enforces Right to Erasure / GDPR Article 17 Data Deletion."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_dashboard_stats(db_path: str = DB_FILE) -> Dict[str, Any]:
    """Computes aggregated, privacy-safe analytics across historical assessments."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total, AVG(overall_score) AS avg_score FROM assessments")
    summary = cursor.fetchone()
    total_assessments = summary["total"] if summary else 0
    avg_score = round(summary["avg_score"], 1) if summary and summary["avg_score"] else 0.0

    # Risk level distribution
    cursor.execute("""
        SELECT risk_level, COUNT(*) as count 
        FROM assessments 
        GROUP BY risk_level
    """)
    level_counts = {r["risk_level"]: r["count"] for r in cursor.fetchall()}

    # Category averages
    cursor.execute("""
        SELECT category, category_name, AVG(score) as avg_score 
        FROM category_scores 
        GROUP BY category, category_name
    """)
    category_averages = [
        {"category": r["category"], "name": r["category_name"], "avg_score": round(r["avg_score"], 1)}
        for r in cursor.fetchall()
    ]

    # Top recurring findings
    cursor.execute("""
        SELECT title, severity, COUNT(*) as frequency 
        FROM findings 
        GROUP BY title, severity 
        ORDER BY frequency DESC 
        LIMIT 5
    """)
    top_findings = [
        {"title": r["title"], "severity": r["severity"], "frequency": r["frequency"]}
        for r in cursor.fetchall()
    ]

    # Recent assessments
    cursor.execute("""
        SELECT assessment_id, overall_score, risk_level, created_at 
        FROM assessments 
        ORDER BY created_at DESC 
        LIMIT 8
    """)
    recent = [
        {"assessment_id": r["assessment_id"], "overall_score": r["overall_score"], 
         "risk_level": r["risk_level"], "created_at": r["created_at"]}
        for r in cursor.fetchall()
    ]

    conn.close()

    return {
        "total_assessments": total_assessments,
        "average_risk_score": avg_score,
        "risk_distribution": {
            "LOW": level_counts.get("LOW", 0),
            "MODERATE": level_counts.get("MODERATE", 0),
            "HIGH": level_counts.get("HIGH", 0),
            "CRITICAL": level_counts.get("CRITICAL", 0)
        },
        "category_averages": category_averages,
        "top_findings": top_findings,
        "recent_assessments": recent
    }
