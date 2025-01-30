import cv2
import numpy as np

def apply_canny_edge(image_path, threshold1=40, threshold2=220):
    # Bild laden
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        return
    
    # Bildgröße anpassen
    image = cv2.resize(image, (800, 600))
    
    # Canny Edge Detection anwenden
    edges = cv2.Canny(image, threshold1, threshold2)
    edges = cv2.resize(edges, (800, 600))
    
    # Originalbild und Kanten anzeigen
    cv2.imshow('Originalbild', image)
    cv2.imshow('Canny Edge Detection', edges)
    
    # Fenstergröße anpassen
    cv2.resizeWindow('Originalbild', 600, 400)
    cv2.resizeWindow('Canny Edge Detection', 600, 400)
    
    # Warten auf eine Taste und Fenster schließen
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return edges

# Beispielaufruf
if __name__ == "__main__":
    image_path = "test_images/init.jpg"  # Bildpfad anpassen
    apply_canny_edge(image_path)
