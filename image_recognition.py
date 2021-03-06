"""
identify a chosen person within images. 
"""
import face_recognition
import os
import cv2

KNOWN_FACES_DIR = "known_faces"
UNKNOWN_FACES_DIR = "unknown_faces"
TOLERANCE = 0.6
FRAME_THICKNESS = 2
FONT_THICKNESS = 1
MODEL = "cnn"
color = [0, 255, 0]       # can dynamically do it based on identity

known_faces_encodings = []
known_names = []


def load_known_faces(KNOWN_FACES_DIR):
    """[will load each image in the directory, encode it, add encoding to a list of known face encodings, 
    and add nae to list of known names]

    Args:
        KNOWN_FACES_DIR ([str]): [name of directory for the images of person/people trying to recognize]
    """
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            img = face_recognition.load_image_file(
                f"{KNOWN_FACES_DIR}/{name}/{filename}")

            # returns  list of face encodings for each img
            encoding = face_recognition.face_encodings(img)
            if len(encoding) != 0:
                # want face at index 0 bc there should only be one face in identity img
                known_faces_encodings.append(encoding[0])
                known_names.append(name)  #name of jpg


def draw_rectangle(locations, img, match):
    """[will draw a rectangle with person's name for each image in locations]

    Args:
        locations ([list]): [A list of tuples of found face locations in css (top, right, bottom, left) order]
        img ([array]): [image contents as numpy array]
        match ([str]): [name of person recognized]

    """
    for (top, right, bottom, left) in locations:
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)

        cv2.rectangle(img, (left, bottom + 25),
                (right, bottom), color, cv2.FILLED)

        cv2.putText(img, match, (left+6, bottom+18),
                cv2.FONT_HERSHEY_DUPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)


def display_image(filename, img):
    """[will display the image window]

    Args:
        filename ([str]): [name of image file currently on]
        img ([array]): [image contents]
    """
    cv2.imshow(filename, img)
    cv2.waitKey(1000)
    cv2.destroyWindow(filename)


def process_unknown_faces(UNKNOWN_FACES_DIR):
    for filename in os.listdir(UNKNOWN_FACES_DIR):

        img = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
        # list of face locations for every face in img
        locations = face_recognition.face_locations(img, model=MODEL)
        encodings = face_recognition.face_encodings(img, locations)
    
        # for opencv use
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # in our example, will only have 1 encoding, 1 location bc only 1 face in unknown imgs
        for face_encoding, face_location in zip(encodings, locations):
            # list of bool of matches, check what index is it true, then check the known_faces list to find the identity match
            results = face_recognition.compare_faces(
                known_faces_encodings, face_encoding, TOLERANCE)

            match = None
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match found: {match}")

                draw_rectangle(locations, img, match)
            
        display_image(filename, img)


print("loading known faces")
load_known_faces(KNOWN_FACES_DIR)

print("processing unknown faces")
process_unknown_faces(UNKNOWN_FACES_DIR)
