
# import cv2
# from pyzbar.pyzbar import decode
# import webbrowser


# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# while True:
#     sucsess, frame = cam.read()
#     if not sucsess:
#         print("❌ Failed to grab frame")
#         break

    
#     for code in decode(frame):
#         code_data = code.data.decode("utf-8")
#         code_type = code.type
#         print(f"✅ Detected {code_type}: {code_data}")

       
#         (x, y, w, h) = code.rect
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         cv2.putText(frame, code_data, (x, y - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#         if code_data.startswith(f"https://") or code_data.startswith(f"http://"):
#             webbrowser.open(code_data)
#         else:
#             print("❌ Not a valid URL")


#         cv2.imshow("QR/Barcode Scanner", frame)
#         cv2.waitKey(1)
#         cam.release()
#         cv2.destroyAllWindows()
#         exit()   
#     cv2.imshow("QR / Barcode Scanner", frame)

  
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()

import cv2
from pyzbar.pyzbar import decode
import sqlite3
import datetime
import os

# ----------------- Database Setup -----------------
db_path = os.path.abspath("qr_data.db")
print(f"📂 Using database: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS qr_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qr_data TEXT NOT NULL,
    scan_time TEXT NOT NULL
)
""")
conn.commit()
print("✅ Table ready")

# ----------------- Camera Setup -----------------
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

found = False

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    for code in decode(frame):
        code_data = code.data.decode("utf-8")
        print(f"✅ QR Detected: {code_data}")

        # Draw box around QR
        (x, y, w, h) = code.rect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, code_data, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Insert into database
        scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO qr_entries (qr_data, scan_time) VALUES (?, ?)", (code_data, scan_time))
        conn.commit()
        print("📥 Data saved to database")

        found = True

    cv2.imshow("QR Scanner", frame)

    if found:  # Stop after first detection
        cv2.waitKey(2000)
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
conn.close()

