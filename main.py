# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-05-28
@Path: /main.py
@Purpose: Unified entry point: RFID + Telegram Bot + Scheduled Reminders
"""

import threading

from medication_db import get_medication_info, init_db
from medication_scheduler import run_scheduler
from rfid_reader import read_rfid
from telegram_bot_server import message_queue, start_bot
from telegram_notifier import queue_medication_info


def handle_rfid():
    while True:
        tag_id = read_rfid()
        if not tag_id:
            continue
        print(f"RFID Tag ID: {tag_id}")
        med = get_medication_info(tag_id)
        print(f"Medication info: {med}")
        if not med:
            continue
        name, desc, usage, dosage, schedule = med
        queue_medication_info(message_queue, tag_id, name, desc, usage, dosage, schedule)

def main():
    init_db()
    threading.Thread(target=handle_rfid, daemon=True).start()
    threading.Thread(target=run_scheduler, daemon=True).start()
    start_bot()

if __name__ == "__main__":
    main()
