# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-05-28 15:16:50
@Path: /medication_scheduler.py
"""


import sqlite3
import time
from datetime import datetime

import schedule

from telegram_bot_server import message_queue
from telegram_notifier import queue_medication_info

DB_NAME = "medication_tracker.db"

def get_all_medications():
    """
    Fetch all medications with their schedule from the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT tag_id, name, schedule FROM medications")
    rows = cursor.fetchall()
    conn.close()
    return rows

def check_and_remind():
    current_hour = datetime.now().hour
    medications = get_all_medications()
    print(medications)

    for tag_id, name, schedule_str in medications:
        if not schedule_str:
            continue
        try:
            hours = [int(h.strip()) for h in schedule_str.split(",")]
            if current_hour in hours:
                queue_medication_info(message_queue, tag_id, name, desc, usage, dosage, schedule_str)
        except ValueError:
            print(f"Invalid schedule format for {name}: {schedule_str}")

def run_scheduler():
    schedule.every(1).minutes.do(check_and_remind)
    print("Scheduler started with `schedule` module. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
