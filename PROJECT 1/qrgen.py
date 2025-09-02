import qrcode
import os



re=input("Student(1) or Teacher(2) : ")
if re.lower()=="1":
    name=input("Enter your name : ")
    roll=input("Enter your roll number : ")
    dep=input("Enter your department : ")
    sem=input("Enter your semester : ")
elif re.lower()=="2":
    name=input("Enter your name : ")
    roll=input("Enter your ID number : ")
    dep=input("Enter your faculty name : ")


myqr=qrcode.make(roll)
if not os.path.exists("qr_codes-S"):
        os.makedirs("qr_codes-S")
if not os.path.exists("qr_codes-T"):
        os.makedirs("qr_codes-T")
if re=="1":
    myqr.save(f"qr_codes-S/{roll}.png")
    print(f"✅ Student QR Code saved at qr_codes-S/{roll}.png")
elif re=="2":
    myqr.save(f"qr_codes-T/{roll}.png")
    print(f"✅ Teacher QR Code saved at qr_codes-T/{roll}.png")