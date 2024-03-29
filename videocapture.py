import cv2
import numpy as np
# import onnxruntime as ort
from tensorflow import keras

def center_crop(frame):
    h, w, _ = frame.shape
    start = abs(h - w) // 2
    if h > w:
        return frame[start: start + w]
    return frame[:, start: start + h]


def main():
    # constants
    index_to_letter = list('ABCDEFGHIKLMNOPQRSTUVWXY')
    mean = 0.485 * 255.
    std = 0.229 * 255.

    # # create runnable session with exported model
    # ort_session = ort.InferenceSession("signlanguage.onnx")

    model = keras.models.load_model('model.h5')

    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # preprocess data
        frame = center_crop(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        x = cv2.resize(frame, (28, 28))
        # x = (x - mean) / std

        x = x.reshape(1, 28, 28, 1).astype(np.float32)
        x = x / 255

        pred = model.predict(x)

        try:
            cv2.putText(frame, index_to_letter[np.argmax(pred[0])], (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), thickness=2)
        except:
            cv2.putText(frame, "W", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0,
                        (0, 255, 0), thickness=2)
        cv2.imshow("Sign Language Translator", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()