"""
identify a chosen person through webcam. 
"""
import face_recognition
import os
import cv2

# too slow, doesn't draw box around face

KNOWN_FACES_DIR = "known_faces"
TOLERANCE = 0.6         # can have multiple tolerances, same person is likely to have a few ids
                        # new face yet on the same frame, the face couldn't have changed, her's a new encoding for that face
                        # bc it was apparently it was a hard to recognize example, make it more robust over time
FRAME_THICKNESS = 2
FONT_THICKNESS = 1
MODEL = "cnn"
color = [0, 255, 0]       # can dynamically do it based on identity

known_faces = []
known_names = []                        
# can have a dict to map id to name

print("loading known faces")

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
    
        img = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        
        # returns  list of face encodings for each img
        encoding = face_recognition.face_encodings(img)

        # want face at index 0 bc there should only be one face in identity img
        if len(encoding) != 0:
            known_faces.append(encoding[0])  
            known_names.append(name)

#open webcam
video = cv2.VideoCapture(0)   
process_this_frame = True

print("processing webcam")


while True:
    ret, img = video.read()
    #try:
    #Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_RGB2BGR) 
    
    if process_this_frame:
        locations = face_recognition.face_locations(rgb_small_frame, model = MODEL)
        encodings = face_recognition.face_encodings(rgb_small_frame, locations)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
            # list of bool of matches, check what index is it true then check the known_faces list to find the identity match
            match = None  
            if True in results:  #seeing face a lot
                match = known_names[results.index(True)]
                print(f"Match found: {match}")

                for (top, right, bottom, left) in locations:
                    # change back to original size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(img, (left, top), (right, bottom), color, 2)

                    cv2.rectangle(img, (left, bottom + 25),
                        (right, bottom), color, cv2.FILLED)

                    cv2.putText(img, match, (left+6, bottom+18),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    cv2.imshow("", img) 
    process_this_frame = not process_this_frame 
    if cv2.waitKey(1) and 0xFF == ord("q"):
        break
   

# Release video
video.release()
cv2.destroyAllWindows()
