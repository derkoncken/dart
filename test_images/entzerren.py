import cv2
import numpy as np
import matplotlib.pyplot as plt

def correct_perspective_with_angle(image):

    top_left = [697,1145]
    top_right = [2841,996]
    bottom_left = [404,2704]
    bottom_right = [3971,2181]

    offset = 500
    distance_nails = 2000
    target_top_left = [offset, offset]
    target_top_right = [offset + distance_nails, offset]
    target_bottom_left = [offset, offset + distance_nails]
    target_bottom_right = [offset + distance_nails, offset + distance_nails]

    result_size = (distance_nails + 2*offset, distance_nails + 2*offset)


    source_points = np.float32([
        top_left,
        top_right,
        bottom_left,
        bottom_right
    ])

    destination_points = np.float32([
    target_top_left,
    target_top_right,
    target_bottom_left,
    target_bottom_right,
    ])

    matrix = cv2.getPerspectiveTransform(source_points, destination_points)
    
    # Größere Zielbildgröße zur Vermeidung von Beschnitt
    
    corrected_image = cv2.warpPerspective(image, matrix, result_size)

    return corrected_image


def detect_circle_and_draw(image):
    # In Graustufen umwandeln
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Bild rauschunterdrücken
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Canny-Kantenerkennung durchführen
    canny_edges = cv2.Canny(blurred, 10, 50)
    
        
    cv2.imshow('Finales Bild', canny_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Canny-Kantenbild anzeigen (optional)
    cv2.imshow("Canny-Kanten", canny_edges)
    # Hough Kreiserkennung
    kreise = cv2.HoughCircles(canny_edges, 
                              cv2.HOUGH_GRADIENT, dp=2, minDist=30, 
                              param1=1, param2=300, minRadius=500, maxRadius=1000)

    # Wenn Kreise erkannt wurden
    if kreise is not None:
        # Die Kreise sind in der Form (x, y, Radius)
        kreise = np.round(kreise[0, :]).astype("int")
        
        # Kreise zeichnen
        for (x, y, r) in kreise:
            # Kreis zeichnen
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)  # grün
            # Mittelpunkt des Kreises markieren
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)  # rot
    
    cv2.imshow('Finales Bild', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





# Lade das Bild
image_path = "/home/robin/Documents/dart/test_images/init.jpg"
image = cv2.imread(image_path)


warped = correct_perspective_with_angle(image)

image = detect_circle_and_draw(warped)




