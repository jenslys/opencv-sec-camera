# Security Camera System

This project sets up a security camera system using a Raspberry Pi, AWS S3, and OpenCV for body detection. The system captures video when a body is detected, stores the video locally or uploads it to an S3 bucket, and deletes the local video file after uploading.

## Features
- Real-time body detection using OpenCV's pre-trained Haar cascade model.
- Video recording with H264 encoding.
- Option to store videos locally or upload them to AWS S3.
- Automatic deletion of local files after successful upload to S3.
- Logging with Loguru for debugging and monitoring.

## Prerequisites
- Raspberry Pi with a camera module.
- Python 3.6 or later.
- AWS S3 account and relevant credentials.
- Haar cascade model file for body detection.


## Demo
Link to demo: [Security Camera System Demo](https://youtu.be/YV6XeBje7cA)

[![Security Camera System Demo](https://img.youtube.com/vi/YV6XeBje7cA/0.jpg)](https://youtu.be/YV6XeBje7cA)

## Setup

1. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**

    Create a `.env` file in the project directory and add the following environment variables:

    ```ini
    ENDPOINT_URL=<your_s3_endpoint_url>
    ACCESS_KEY=<your_aws_access_key>
    SECRET_ACCESS_KEY=<your_aws_secret_access_key>
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
- When a body is detected, video recording starts and continues until no bodies are detected for a specified interval (default 7 seconds).
- If the `--local` flag is not set, recorded videos are uploaded to the specified S3 bucket and deleted locally after a successful upload.

## File Description

- **main.py**: The main script that sets up the camera, detects bodies, and handles video recording and uploading.
- **.env**: Environment file storing AWS credentials and endpoint URL.


## Acknowledgements

- OpenCV for providing the Haar cascade model for body detection.
- Loguru for advanced logging.
- AWS for providing scalable storage solutions.
