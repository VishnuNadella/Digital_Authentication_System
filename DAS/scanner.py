import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pyperclip
import gspread

gc = gspread.service_account(filename = "dastest_cred.json")

sh =  gc.open_by_key("1nW4f8seohxA24AS7vWTsrvCawztF7HXe6dFHMt-T0v8")

def status(sheet, data_1, data_2, data_3, y, frame, c):
    wks = sh.get_worksheet(sheet)
    data_set = wks.get_all_values()
    col = 1
    whole_col = wks.col_values(2)
    uqn_ID = data_1
    f = open("Entries.txt", "a")
    for row in data_set:
        if row[1] == uqn_ID:
            if row[c] == "FALSE":
                for i in range(100):
                    cv2.imshow("Approved",frame)
                    cv2.putText(frame, data_1, (0,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                    cv2.putText(frame, data_2, (0,y + 25), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                    cv2.putText(frame, data_3, (0,y + 50), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
                    inp = cv2.waitKey(10)
                    if inp == ord('k'):
                        break
                wks.update_cell(col, c + 1, "TRUE")

                wrt_str = "send: " + data_2 + " with ID: " + data_1 + "\n"

                f.write(wrt_str)
                print(f"----------------send: {data_2} with ID: {data_1}")
            elif row[c] == "TRUE":
                cv2.putText(frame, "DUPLICATE QR CODE", (50, 150), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)
        elif uqn_ID not in whole_col:
            cv2.putText(frame, "No User Exists in Database", (50, 150), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,255), 2)

        col += 1
    f.close()

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img)
    for obj in barcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        string = str(barcodeData)
        data_1, data_2, data_3 = string.strip().split("\n")
        pyperclip.copy(data_1) # copies to clipboard
        
        if int(data_3[:5]) == 20951:
            status(1, data_1, data_2, data_3, y, frame, 7)
        elif int(data_3[:5]) == 21955:
            status(2, data_1, data_2, data_3, y, frame, 6)
        elif int(data_3[:5]) == 21951:
            status(0, data_1, data_2, data_3, y, frame, 7)
        else:
            cv2.putText(frame, "The provided roll number dosent exist", (0, 500), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0), 2)


cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, None, fx = 1, fy = 1)
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break