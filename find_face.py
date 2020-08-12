import face_recognition
import os
from PIL import Image


# Load the jpg file into a numpy array
image_path = os.path.abspath("known_faces_the100/lincoln.jpg")
img = face_recognition.load_image_file(image_path)

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(img)

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_img = img[top:bottom, left:right]
    pil_image = Image.fromarray(face_img)
    pil_image.show()
