import argparse
import io
import os
import time

import boto3
import cv2
import libcamera
from dotenv import load_dotenv
from loguru import logger
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput

# * Load environment variables
load_dotenv()
os.environ["LIBCAMERA_LOG_LEVELS"] = "4"
endpointUrl = os.getenv("ENDPOINT_URL")
accessKey = os.getenv("ACCESS_KEY")
secretAccessKey = os.getenv("SECRET_ACCESS_KEY")

# * Constants
recordingInterval = 7
cascadePath = "/usr/share/opencv4/haarcascades/haarcascade_upperbody.xml"

# *Setup AWS S3 client with specified credentials and endpoint
s3 = boto3.client(
    service_name="s3",
    endpoint_url=endpointUrl,
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretAccessKey,
    region_name="auto",
)

# * Initialize and configure the camera with image flipping for correct orientation
picam2 = Picamera2()
videoConfig = picam2.create_video_configuration(main={"format": "XRGB8888"})
videoConfig["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam2.configure(videoConfig)
picam2.start()

# * Setup video recording with H264 encoding
encoder = H264Encoder()

# * Load the upper body detector using OpenCV's pre-trained Haar cascade model
bodyDetector = cv2.CascadeClassifier(cascadePath)


def detectBodies():
    # * Captures an image from the camera, converts it to grayscale, and detects bodies.
    # * Returns True if any bodies are detected, otherwise False.
    im = (
        picam2.capture_array()
    )  # ? Capture the next camera image from the stream named as its first argument
    grey = cv2.cvtColor(
        im, cv2.COLOR_BGR2GRAY
    )  # ? Convert the captured image to grayscale
    bodies = bodyDetector.detectMultiScale(grey, 1.1, 5)  # * Detect bodies in the image
    return len(bodies) > 0  # * Return True if any bodies are detected, otherwise False


def main():
    # * Setup argparse to handle command line arguments
    parser = argparse.ArgumentParser(
        description="Control video recording and storage options."
    )
    parser.add_argument(
        "--local", action="store_true", help="If set, store videos locally only."
    )
    args = parser.parse_args()

    logger.info("Initializing...")
    time.sleep(2)  # * Short delay to stabilize camera
    logger.info("Initialization complete")

    recording = False
    startTime = None

    while True:
        try:
            bodyDetected = detectBodies()
            currentTime = time.time()

            if bodyDetected and not recording:
                # * Generate a unique filename for each recording session
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                outputFilename = f"output_{timestamp}.mp4"
                output = FfmpegOutput(outputFilename)

                # * Start recording if a body is detected and not already recording
                picam2.start_recording(encoder, output, quality=Quality.LOW)
                startTime = currentTime
                recording = True
                logger.info(f"Body detected, started recording to {outputFilename}")

            if recording:
                if bodyDetected:
                    # * Update the timer if body is still detected
                    startTime = currentTime
                elif currentTime - startTime >= recordingInterval:
                    # * Stop recording if no body is detected for x seconds
                    picam2.stop_recording()
                    logger.info("Recording stopped")
                    recording = False

                    # *  Read the recorded video file
                    with open(outputFilename, "rb") as file:
                        fileContent = file.read()

                    if not args.local:
                        # *  Upload the video file to S3
                        s3.upload_fileobj(
                            io.BytesIO(fileContent), "detection", outputFilename
                        )
                        logger.info(f"Uploaded {outputFilename} to S3 successfully")

                        # * Delete the local file after uploading
                        os.remove(outputFilename)
                        logger.info(f"Deleted local file {outputFilename} after upload")
                    else:
                        logger.info(f"Stored {outputFilename} locally")

                    # * Reinitialize camera configuration for detection
                    picam2.stop()
                    picam2.configure(videoConfig)
                    picam2.start()
                    logger.debug("Camera reinitialized for detection")

            # * Sleep for a short duration before checking again
            time.sleep(1)

        except Exception as e:
            logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
