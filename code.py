import cv2
import boto3
from cvzone.HandTrackingModule import HandDetector

def launchos():
    myec2 = boto3.resource("ec2")
    response = myec2.create_instances(
        ImageId="ami-0da59f1af71ea4ad2",
        InstanceType="t2.micro",
        MaxCount=1,
        MinCount=1
    )
    print("EC2 instance launched:", response)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)  

while True:
    status, photo = cap.read()
    if not status:
        print("Failed to read from the camera")
        break

    hands, photo = detector.findHands(photo, draw=True)

    cv2.imshow("Myphoto", photo)

    if cv2.waitKey(1) == 13:  
        break

    if hands:
        hand = hands[0]
        lmlist = hand["lmList"]  
        fingerstatus = detector.fingersUp(hand) 
        if fingerstatus == [0, 1, 1, 0, 0]:
            print("Cheers")
        elif fingerstatus == [1, 1, 1, 1, 1]:
            print("All Up")
            launchos()
        elif fingerstatus == [1, 0, 0, 0, 0]:
            print("Thumbs up")
        else:
            print("IDK")

cv2.destroyAllWindows()
cap.release()
