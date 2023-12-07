import cv2
import numpy as np
import paho.mqtt.client as mqtt
import json
from tensorflow.keras.models import load_model

# Replace "broker_ip" with the actual IP address of your MQTT broker, in the final case the RPi
# BROKER_IP = "localhost"
BROKER_IP = "192.168.68.121"
MQTT_TOPIC = "Dyson-NST-at-codiax"

# Load your trained model
model = load_model("./models/workshop_model_v2_5CNN.h5")  # Replace with the path to your saved model

# Open the camera (0 corresponds to the default camera, you can change it if needed)
cap = cv2.VideoCapture(0)

# Set the frame dimensions
frame_width = 640
frame_height = 480

# Set the capture dimensions
cap.set(3, frame_width)
cap.set(4, frame_height)

# Set the ROI size
ROI_SIZE = 256
MODEL_INPUT_SIZE = (128, 128)

# Initialize the previous prediction value
previous_prediction = None

# Set the confidence threshold
confidence_threshold = 0.45

# MQTT setup
client = mqtt.Client()
client.connect(BROKER_IP, 1883, 60)  # 60 is the keep-alive interval in seconds

def on_publish(client, userdata, mid):
    print(f"Published MQTT message: {MQTT_TOPIC} {message} ----- confidence : {confidence_levels:.3f}")

client.on_publish = on_publish

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    # Draw a bounding box on the frame
    top_left = (int((frame_width - ROI_SIZE) / 2), int((frame_height - ROI_SIZE) / 2))
    bottom_right = (top_left[0] + ROI_SIZE, top_left[1] + ROI_SIZE)
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Get the region of interest (ROI)
    roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Resize the ROI to 256x256
    roi = cv2.resize(roi, (ROI_SIZE, ROI_SIZE))

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Display the frame with bounding box
    cv2.imshow('Frame with ROI', frame)

    # Preprocess the grayscale ROI for model input
    processed_roi = cv2.resize(gray_roi, MODEL_INPUT_SIZE)
    processed_roi = processed_roi / 255.0
    processed_roi = np.expand_dims(processed_roi, axis=(0, -1))  # Add batch and channel dimensions

    # Make a prediction using the model
    prediction = model.predict(processed_roi, verbose=0)

    # Get the predicted class and confidence levels
    predicted_class = np.argmax(prediction)
    confidence_levels = np.max(prediction)
    prediction_text = f"Prediction: Class {predicted_class}"
    cv2.putText(gray_roi, prediction_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(gray_roi, f"Confidence: {confidence_levels:.3f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Grayscale ROI with Prediction', gray_roi)

    # Publish on MQTT if the prediction changes and is over the confidence threshold
    if previous_prediction is None or predicted_class != previous_prediction:
        if confidence_levels > confidence_threshold:
            message = {"speed": 2*int(predicted_class)}
            try:
                client.publish(MQTT_TOPIC, json.dumps(message))
            except Exception as e:
                print(f"Error publishing MQTT message: {e}")

            previous_prediction = predicted_class

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
