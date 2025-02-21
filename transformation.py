import cv2
import numpy as np

def detect_dartboard(image_path, output_size=500, show_result=True):
    print("Lade Bild...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"Fehler: Bild konnte nicht geladen werden ({image_path})")
        return None, None, None
    
    print("Konvertiere zu Graustufen...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    print("Wende Gaussian Blur an...")
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite("debug_blurred.jpg", blurred)  # Speichert das unscharfe Bild für Debugging
    
    print("Führe Hough-Kreis-Transformation durch...")
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                               param1=1, param2=10, minRadius=30, maxRadius=3000)
    
    if circles is None or len(circles[0]) == 0:
        print("Keine Dartscheibe erkannt! Prüfe debug_blurred.jpg für Probleme.")
        return None, None, None
    print("Anzahl der Kreise: " + str(len(circles)))
    print("Wähle größten erkannten Kreis...")
    circles = np.uint16(np.around(circles))
    largest_circle = max(circles[0], key=lambda c: c[2])
    cx, cy, r = largest_circle
    print(f"Erkannter Kreis - Mittelpunkt: ({cx}, {cy}), Radius: {r}")
    
    src_pts = np.float32([
        [cx - r, cy],
        [cx + r, cy],
        [cx, cy - r],
        [cx, cy + r]
    ])
    
    dst_pts = np.float32([
        [0, output_size // 2],
        [output_size, output_size // 2],
        [output_size // 2, 0],
        [output_size // 2, output_size]
    ])
    
    print("Berechne Homographie-Matrix...")
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
    print("Führe Perspektivtransformation durch...")
    warped = cv2.warpPerspective(image, matrix, (output_size, output_size))
    
    angle = np.arctan2(src_pts[2][1] - src_pts[3][1], src_pts[2][0] - src_pts[3][0])
    angle_degrees = np.degrees(angle)
    print(f"Entzerrungswinkel: {angle_degrees:.2f} Grad")
    
    if show_result:
        print("Zeige das entzerrte Bild an...")
        cv2.imshow("Entzerrtes Bild", warped)
        cv2.waitKey(0)  # Warten auf Tastendruck, um Blockieren zu vermeiden
        cv2.destroyAllWindows()
    
    print("Fertig.")
    return warped, matrix, angle_degrees

# Beispielaufruf
warped, matrix, angle = detect_dartboard("test_images/init_canny_edges.jpg")
