# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-05-27 21:58:46
@Path: /rfid_reader.py
"""


def read_rfid():
    """
    Simulates or reads an RFID tag ID.
    Replace the input() simulation with actual RFID reader code if hardware is available.
    """
    try:
        # Simulate RFID input for testing
        tag_id = input("Scan RFID tag or enter tag ID: ")
        return tag_id.strip()
    except KeyboardInterrupt:
        print("\nExiting RFID reader.")
        return None