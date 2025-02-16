import cv2
import numpy as np
import math

# Bild laden
image = cv2.imread("/home/robin/Documents/dart/test_images/init.jpg")

# Bildgröße holen
(h, w) = image.shape[:2]

# Erste Transformation für die Perspektivkorrektur
angle = -60
theta = math.radians(angle)
shift_x = math.tan(theta) * h

pts1 = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]])
pts2 = np.float32([
    [shift_x, 0],
    [w - 1 - shift_x, 0],
    [0, h - 1],
    [w - 1, h - 1]
])

# Erste Transformation durchführen
matrix1 = cv2.getPerspectiveTransform(pts1, pts2)
perspective_image = cv2.warpPerspective(image, matrix1, (w, h))

# Zweite Transformation für die horizontale Streckung
stretch_factor = 0.2  # Anpassen je nach Bedarf

pts3 = np.float32([
    [w*0.2, h*0.2],    # Oben links
    [w*0.8, h*0.2],    # Oben rechts
    [w*0.2, h*0.8],    # Unten links
    [w*0.8, h*0.8]     # Unten rechts
])

pts4 = np.float32([
    [w*0.2*stretch_factor, h*0.2],     # Oben links
    [w*0.8*stretch_factor, h*0.2],     # Oben rechts
    [w*0.2*stretch_factor, h*0.8],     # Unten links
    [w*0.8*stretch_factor, h*0.8]      # Unten rechts
])

# Zweite Transformation durchführen
matrix2 = cv2.getPerspectiveTransform(pts3, pts4)
final_image = cv2.warpPerspective(perspective_image, matrix2, (int(w*stretch_factor), h))

# Ergebnis anzeigen
cv2.imshow('Finales Bild', final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()