"""
database_manager.py

Handles database connections and database operations
for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import sqlite3
from datetime import datetime


class DatabaseManager:
    """
    Handles all SQLite database operations.
    """

    def __init__(self, database_path="database/scanner.db"):
        self.database_path = database_path
        self.connection = None

    # ==========================================================
    # Context Manager
    # ==========================================================

    def __enter__(self):
        """Open database connection automatically."""
        self.connect()
        self.initialize_database()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close database connection automatically."""
        self.close()

    # ==========================================================
    # Connection Management
    # ==========================================================

    def connect(self):
        """
        Open SQLite connection.
        """

        if self.connection is None:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row

        return self.connection

    def close(self):
        """
        Close SQLite connection safely.
        """

        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # ==========================================================
    # Database Initialization
    # ==========================================================

    def initialize_database(self):
        """
        Create required database tables.
        """

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            scan_time TEXT NOT NULL,
            trend TEXT,
            signal TEXT,
            confidence INTEGER

        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            direction TEXT NOT NULL,
            confidence INTEGER NOT NULL,
            created_at TEXT NOT NULL

        )
        """)

        self.connection.commit()

    # ==========================================================
    # Save Operations
    # ==========================================================

    def save_scan(
        self,
        market,
        timeframe,
        trend,
        signal,
        confidence,
    ):
        """
        Save completed market scan.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO scans (
                market,
                timeframe,
                scan_time,
                trend,
                signal,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                market,
                timeframe,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                trend,
                signal,
                confidence,
            ),
        )

        self.connection.commit()

    def save_signal(self, signal):
        """
        Save generated trading signal.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO signals (
                market,
                timeframe,
                direction,
                confidence,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                signal.market,
                signal.timeframe,
                signal.direction,
                signal.confidence,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        self.connection.commit()

    # ==========================================================
    # Validation
    # ==========================================================

    def scan_exists(
        self,
        market,
        timeframe,
        scan_time,
    ):
        """
        Check whether a scan already exists.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM scans
            WHERE market = ?
            AND timeframe = ?
            AND scan_time = ?
            LIMIT 1
            """,
            (
                market,
                timeframe,
                scan_time,
            ),
        )

        return cursor.fetchone() is not None

    # ==========================================================
    # Retrieval
    # ==========================================================

    def get_latest_scan(self):
        """
        Return latest saved scan.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                market,
                timeframe,
                scan_time,
                trend,
                signal,
                confidence
            FROM scans
            ORDER BY id DESC
            LIMIT 1
            """
        )

        return cursor.fetchone()

    def get_all_scans(
        self,
        limit=20,
    ):
        """
        Return scan history.
        """

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                market,
                timeframe,
                scan_time,
                trend,
                signal,
                confidence
            FROM scans
            ORDER BY id DESC
            LIMIT 15
            """
        )

        return cursor.fetchall()

    # ==========================================================
    # Statistics
    # ==========================================================

    def get_database_statistics(self):
        """
        Return database statistics.
        """

        cursor = self.connection.cursor()

        statistics = {}

        cursor.execute("SELECT COUNT(*) FROM scans")
        statistics["total_scans"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM signals")
        statistics["total_signals"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM signals WHERE direction='BUY'"
        )
        statistics["buy_signals"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM signals WHERE direction='SELL'"
        )
        statistics["sell_signals"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM signals WHERE direction='WAIT'"
        )
        statistics["wait_signals"] = cursor.fetchone()[0]

        cursor.execute(
            "SELECT AVG(confidence) FROM signals"
        )

        average = cursor.fetchone()[0]

        statistics["average_confidence"] = (
            round(average, 2)
            if average is not None
            else 0
        )

        return statistics