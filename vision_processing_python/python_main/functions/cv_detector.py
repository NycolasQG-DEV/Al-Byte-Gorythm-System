from cvzone.FaceDetectionModule import FaceDetector
from cvzone.HandTrackingModule import HandDetector
import math
import config

#instancia que tem como função Identificar os rostos
class FaceDetectorWrapper:
    def __init__(self):
        self.detector = FaceDetector(minDetectionCon=config.DETECTION_CONFIDENCE_THRESHOLD, modelSelection=1)

    def detect_faces(self, img):
        img, bboxs = self.detector.findFaces(img, draw=False)
        return img, bboxs

#instancia que tem como função detectar a mão e dedos
class HandDetectorWrapper:
    def __init__(self):
        self.detector = HandDetector(detectionCon=config.DETECTION_CONFIDENCE_THRESHOLD, maxHands=2)

    def detect_hands(self, img):
        hands, img = self.detector.findHands(img, draw=False)
        return img, hands

    def measure_distance_between_index_fingers(self, hands):
        if len(hands) == 2:
            # Posição dos dedos indicadores das duas mãos
            index1 = hands[0]['lmList'][8][:2]  # Dedo indicador da primeira mão
            index2 = hands[1]['lmList'][8][:2]  # Dedo indicador da segunda mão

            # Calcular a distância entre os dedos indicadores
            distance = math.hypot(index2[0] - index1[0], index2[1] - index1[1])
            midpoint = ((index1[0] + index2[0]) // 2, (index1[1] + index2[1]) // 2)

            return distance, midpoint
        return None, None
