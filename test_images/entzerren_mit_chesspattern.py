import cv2
import numpy as np

# Bild laden
image = cv2.imread("clear.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Deine Schachbrett-Pattern-Größe (innere Ecken, nicht Felder!)
pattern_size = (5, 4)

# Erkenne das Schachbrettmuster
found, corners = cv2.findChessboardCorners(gray, pattern_size, None)

if found:
    cv2.drawChessboardCorners(image, pattern_size, corners, found)

    # Äußere Ecken des Schachbretts wählen
    src_points = np.array([
        corners[0][0],      # Oben links
        corners[4][0],      # Oben rechts
        corners[-1][0],     # Unten rechts
        corners[-5][0]      # Unten links
    ], dtype=np.float32)

    # Zielpunkte: Wir strecken das Bild so, dass das Schachbrett gerade ist
    width = image.shape[1]  # Behalte die Originalbreite des Bildes
    height = image.shape[0]  # Behalte die Originalhöhe

    x_frame = 300
    y_frame = 300
    chess_size = 30

    obj_points = np.array([
        [x_frame, y_frame],
        [x_frame + chess_size, y_frame],
        [x_frame + chess_size, y_frame + chess_size],
        [x_frame, y_frame + chess_size]
    ], dtype=np.float32)

    # Berechne die Perspektivtransformation
    matrix = cv2.getPerspectiveTransform(src_points, obj_points)

    # Wende die Transformation auf das gesamte Bild an
    warped = cv2.warpPerspective(image, matrix, (2*x_frame + chess_size, 2*y_frame + chess_size))

    # Zeige das entzerrte Bild
    cv2.imshow("Entzerrtes Bild", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Schachbrettmuster nicht erkannt!")
