# Custom Labels Detection App

This project consists of three main files:

1. **app.py**: This file contains the code for a Kivy application that allows users to upload images and detect custom labels using Amazon Rekognition's Custom Labels feature.

2. **local_image.py**: This file contains code to display and annotate images with detected custom labels. It supports both local image files and images stored in an Amazon S3 bucket.

3. **documentation.py**: This file provides utility functions for analyzing images using Amazon Rekognition's Custom Labels, both from local files and from Amazon S3 buckets. It also includes code for displaying the analyzed images with annotated labels.

## Usage

### 1. app.py

This file contains a Kivy application with two screens:

- **WelcomePage**: Displays a welcome message and a button to start exploring.
- **MainPage**: Allows users to upload an image, analyze it for custom labels, and display the detected labels.

To run the application, execute the `CustomLabelApp` class from `app.py`.

### 2. local_image.py

This file provides functions to display and annotate images with detected custom labels. It includes two main functions:

- **display_image**: Displays the image with bounding boxes and labels for detected custom labels.
- **show_custom_labels**: Calls Amazon Rekognition's `detect_custom_labels` API to detect custom labels in the image.

To use the functions, import the necessary modules and call the `display_image` or `show_custom_labels` function with the appropriate parameters.

### 3. documentation.py

This file contains utility functions for analyzing images using Amazon Rekognition's Custom Labels. It includes functions for analyzing images stored locally and in Amazon S3 buckets, as well as displaying the analyzed images with annotated labels.

To use the functions, import the necessary modules and call the `analyze_local_image` or `analyze_s3_image` function with the appropriate parameters.

## Prerequisites

Before running the application or using the utility functions, ensure you have:

- Python installed on your system.
- Necessary Python packages installed, including `kivy`, `boto3`, `PIL`, and `tkinter` (for `local_image.py`).
- AWS credentials configured on your system (for accessing Amazon Rekognition).

## References

- [Amazon Rekognition Custom Labels documentation](https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/detecting-custom-labels.html)
- [Kivy documentation](https://kivy.org/doc/stable/)
- [PIL (Python Imaging Library) documentation](https://pillow.readthedocs.io/en/stable/)
- [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
