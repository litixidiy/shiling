import cv2
def take_pic():
    cap = cv2.VideoCapture(0)

    while(True):
        cv2.waitKey(1)
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF!=255:
            cv2.imwrite("test.jpg",frame)

            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
