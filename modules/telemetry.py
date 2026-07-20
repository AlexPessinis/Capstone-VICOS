# modules/telemetry.py

#NOTICE: THIS IS MOCK DATA UNTIL I CAN ACTUALLY CONNECT TO THE CAR

import time
from modules.mock_obd import get_mock_data
from modules.database import init_db
from modules.database import insert_telemetry
from modules.config import TELEMETRY_INTERVAL

def start_telemetry():
    init_db()
    while True:
        data = get_mock_data()
        insert_telemetry(data)
        time.sleep(TELEMETRY_INTERVAL)
