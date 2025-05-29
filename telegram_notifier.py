# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-05-28 14:34:07
@Path: /telegram_notifier.py
"""

import asyncio
import time
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import CHAT_ID
from medication_logger import get_logs_for_today, log_medication


def queue_medication_info(queue, tag_id, name, desc, usage, dosage, schedule):
    """
    Queue medication information for sending to Telegram.
    """
    print(f"Queuing medication info for {name} (ID: {tag_id})")
    queue.append(med_des_msg(name, desc, usage, dosage))
    print(f"Queue size: {len(queue)}")
    time.sleep(1)  # Simulate delay for processing
    print(f"Queue size: {len(queue)}")
    should_take = is_time_to_take(schedule) and not has_taken_this_hour(tag_id)
    print(f"Should take {name}: {should_take}")
    if should_take:
        queue.append(invitation_msg(tag_id, name, desc, usage, dosage, schedule))
        print(f"Queue size after adding invitation: {len(queue)}")
    else:
        print(f"Not time to take {name} yet. Current hour: {datetime.now().hour}, Scheduled: {schedule}")

def has_taken_this_hour(tag_id):
    """
    Check if the medication has already been logged during the current hour today.
    """
    logs = get_logs_for_today(tag_id)
    print(f"Logs for today for {tag_id}: {logs}")
    current_hour = datetime.now().hour
    for log in logs:
        log_hour = datetime.fromisoformat(log[4]).hour
        if log_hour == current_hour:
            return True
    return False

def is_time_to_take(schedule):
    """
    Check if it's time to take the medication based on schedule string.
    """
    now_hour = datetime.now().hour
    hours = [int(h.strip()) for h in schedule.split(",") if h.strip().isdigit()]
    print(f"Current hour: {now_hour}, Scheduled hours: {hours}")
    return now_hour in hours

def med_des_msg(name, desc, usage, dosage):
    """
    Format the medication message and optional buttons.
    """
    msg = f"💊 *{name}*\n_{desc}_\n\nUsage: {usage}\nDosage: {dosage}"
    return msg, None  # No buttons for this message

def invitation_msg(tag_id, name, desc, usage, dosage, schedule):
    """
    Format the medication message and optional buttons.
    """
    msg = f"💊 *{name}*\n_{desc}_\n\nUsage: {usage}\nDosage: {dosage}"
    buttons = [[
        InlineKeyboardButton("✅ Taken", callback_data=f"taken:{tag_id}"),
        InlineKeyboardButton("❌ Skipped", callback_data=f"skipped:{tag_id}")
    ]]
    return msg, buttons

def process_message_queue(bot, queue, loop):
    """
    Continuously check the queue and send messages using asyncio-safe method.
    """
    print("🟢 process_message_queue started.")
    while True:
        if queue:
            item = queue.pop(0)
            coroutine = _send_message(bot, msg=item[0], buttons=item[1])
            asyncio.run_coroutine_threadsafe(coroutine, loop)
        else:
            time.sleep(1)

async def _send_message(bot, msg, buttons=None):
    """
    Async message sender for Telegram.
    """

    try:
        print("📤 Sending Telegram message...")
        print(f"Message content: {msg}")
        print(f"Buttons: {buttons}, len(buttons): {len(buttons) if buttons else 'None'}")
        await bot.send_message(
            chat_id=CHAT_ID,
            text=msg,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )
    except Exception as e:
        print("Error sending message:", e)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle button callbacks for taken/skipped actions.
    """
    query = update.callback_query
    await query.answer()
    print("🔘 Callback received:", query.data)
    action, tag_id = query.data.split(":")
    print(f"🔘 Button pressed: {action} for tag {tag_id}")
    log_medication(tag_id, action)
    await query.edit_message_text(f"✅ Recorded as *{action}*.")
