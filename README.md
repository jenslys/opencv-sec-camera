# Security Camera System

This project sets up a security camera system using a Raspberry Pi, AWS S3, and OpenCV for body detection. The system captures video when a body is detected, stores the video locally or uploads it to an S3 bucket, sends a notification via Pushover, and deletes the local video file after uploading.

*This was made as part of the course "SSS3000R-1" at USN.*

## Features
- Real-time body detection using OpenCV's pre-trained Haar cascade model.
- Video recording with H264 encoding.
- Option to store videos locally or upload them to AWS S3.
- Automatic deletion of local files after successful upload to S3.
- Sending notifications with video links using Pushover.
- Logging with Loguru for debugging and monitoring.

## Prerequisites
- Raspberry Pi with a camera module.
- Python 3.6 or later.
- AWS S3 account and relevant credentials.
- Haar cascade model file for body detection.
- Pushover account and API token.

## Demo
Link to demo: [Security Camera System Demo](https://youtu.be/YV6XeBje7cA)

## Setup

1. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**

    Create a `.env` file in the project directory and add the following environment variables:

    ```ini
    R2_ENDPOINT_URL=<your_s3_endpoint_url>
    R2_ACCESS_KEY=<your_aws_access_key>
    R2_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
    R2_PUBLIC_URL=<your_public_bucket_url>
    PUSHOVER_APP_TOKEN=<your_pushover_app_token>
    PUSHOVER_USER_KEY=<your_pushover_user_key>
    ```

3. **Configure AWS S3**

    Ensure you have an S3 bucket named `detection` or modify the code to suit your bucket name.

4. **Run the script**

    ```bash
    python main.py [--local]
    ```

    Use the `--local` flag to store videos locally without uploading to S3.

## Usage

- The system initializes the camera and waits for body detection.
- When a body is detected, video recording starts and continues until no bodies are detected. Additionally, it has a 7-second buffer before stopping the recording in case the body moves out of the frame.
- If the `--local` flag is not set, recorded videos are uploaded to the specified S3 bucket and deleted locally after a successful upload.
- After uploading the video to S3, a notification is sent using the Pushover API with a link to the video.

## File Description

- **main.py**: The main script that sets up the camera, detects bodies, and handles video recording, uploading, and notifications.
- **.env**: Environment file storing AWS credentials, Pushover credentials, and endpoint URLs.


## Acknowledgements

- OpenCV for providing the Haar cascade model for body detection.
- Loguru for advanced logging.
- AWS for providing scalable storage solutions.
- Pushover for providing notification services.
