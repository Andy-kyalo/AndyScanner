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

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
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

            self.connection = sqlite3.connect(
                self.database_path
            )

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
        Create required database tables and apply
        incremental schema migrations.
        """

        cursor = self.connection.cursor()

        # ------------------------------------------------------
        # Scans
        # ------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                market TEXT NOT NULL,

                timeframe TEXT NOT NULL,

                scan_time TEXT NOT NULL,

                trend TEXT,

                signal TEXT,

                confidence INTEGER

            )
            """
        )

        # ------------------------------------------------------
        # Signals
        # ------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                market TEXT NOT NULL,

                timeframe TEXT NOT NULL,

                direction TEXT NOT NULL,

                confidence INTEGER NOT NULL,

                created_at TEXT NOT NULL

            )
            """
        )

        self.connection.commit()

        # Apply incremental schema migrations.
        self.migrate_database()

    # ==========================================================
    # Database Migration
    # ==========================================================

    def migrate_database(self):
        """
        Apply incremental schema migrations safely.

        Existing scan records are preserved.

        New TradeSetup fields:

            entry
            stop_loss
            take_profit
            risk_reward
            setup_valid
        """

        cursor = self.connection.cursor()

        cursor.execute(
            "PRAGMA table_info(scans)"
        )

        columns = {
            row["name"]
            for row in cursor.fetchall()
        }

        migrations = {

            "entry": (
                "ALTER TABLE scans "
                "ADD COLUMN entry REAL"
            ),

            "stop_loss": (
                "ALTER TABLE scans "
                "ADD COLUMN stop_loss REAL"
            ),

            "take_profit": (
                "ALTER TABLE scans "
                "ADD COLUMN take_profit REAL"
            ),

            "risk_reward": (
                "ALTER TABLE scans "
                "ADD COLUMN risk_reward REAL"
            ),

            "setup_valid": (
                "ALTER TABLE scans "
                "ADD COLUMN setup_valid "
                "INTEGER DEFAULT 0"
            ),
        }

        for column, statement in migrations.items():

            if column not in columns:

                cursor.execute(statement)

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
        trade_setup=None,
    ):
        """
        Save a completed market scan.

        TradeSetup is optional for backward compatibility.

        When no TradeSetup is supplied:

            entry       = NULL
            stop_loss   = NULL
            take_profit = NULL
            risk_reward = NULL
            setup_valid = 0
        """

        cursor = self.connection.cursor()

        entry = None
        stop_loss = None
        take_profit = None
        risk_reward = None
        setup_valid = 0

        if trade_setup is not None:

            entry = trade_setup.entry

            stop_loss = trade_setup.stop_loss

            take_profit = trade_setup.take_profit

            risk_reward = trade_setup.risk_reward

            setup_valid = int(
                trade_setup.valid
            )

        cursor.execute(
            """
            INSERT INTO scans (

                market,
                timeframe,
                scan_time,
                trend,
                signal,
                confidence,

                entry,
                stop_loss,
                take_profit,
                risk_reward,
                setup_valid

            )
            VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )
            """,
            (
                market,
                timeframe,

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                trend,
                signal,
                confidence,

                entry,
                stop_loss,
                take_profit,
                risk_reward,
                setup_valid,
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

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
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
        Return the latest saved scan including
        TradeSetup information.
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

                confidence,

                entry,

                stop_loss,

                take_profit,

                risk_reward,

                setup_valid

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
        Return scan history including TradeSetup
        information.

        Parameters
        ----------
        limit:
            Maximum number of records to return.
        """

        if limit <= 0:

            return []

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

                confidence,

                entry,

                stop_loss,

                take_profit,

                risk_reward,

                setup_valid

            FROM scans

            ORDER BY id DESC

            LIMIT ?
            """,
            (
                limit,
            ),
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

        # ------------------------------------------------------
        # Total scans
        # ------------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM scans"
        )

        statistics["total_scans"] = (
            cursor.fetchone()[0]
        )

        # ------------------------------------------------------
        # Total signals
        # ------------------------------------------------------

        cursor.execute(
            "SELECT COUNT(*) FROM signals"
        )

        statistics["total_signals"] = (
            cursor.fetchone()[0]
        )

        # ------------------------------------------------------
        # BUY signals
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM signals
            WHERE direction = 'BUY'
            """
        )

        statistics["buy_signals"] = (
            cursor.fetchone()[0]
        )

        # ------------------------------------------------------
        # SELL signals
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM signals
            WHERE direction = 'SELL'
            """
        )

        statistics["sell_signals"] = (
            cursor.fetchone()[0]
        )

        # ------------------------------------------------------
        # WAIT signals
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM signals
            WHERE direction = 'WAIT'
            """
        )

        statistics["wait_signals"] = (
            cursor.fetchone()[0]
        )

        # ------------------------------------------------------
        # Average confidence
        # ------------------------------------------------------

        cursor.execute(
            """
            SELECT AVG(confidence)
            FROM signals
            """
        )

        average = cursor.fetchone()[0]

        statistics["average_confidence"] = (

            round(average, 2)

            if average is not None

            else 0

        )

        return statistics