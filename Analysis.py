import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
import os

def display_image(bucket, photo, response):
    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    # Convert the image to RGB mode
    image = image.convert('RGB')

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 1000)
            draw.text((left,top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            

            points = (
                (left,top),
                (left + width, top),
                (left + width, top + height),
                (left , top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)

    # Save the modified image locally
    local_image_path = os.path.join(os.getcwd(), 'annotated_image.jpg')
    image.save(local_image_path)

    # Open the image using VSCode's built-in image viewer
    os.system(f'code {local_image_path}')

def show_custom_labels(model, bucket, photo, min_confidence):
    client = boto3.client('rekognition')

    # Call DetectCustomLabels
    response = client.detect_custom_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MinConfidence=min_confidence,
        ProjectVersionArn=model
    )


    return response

def main():
    bucket = 'custom-labels-console-us-east-1-82a87b81e9'
    photo = 'الكعبة-المشرفة.jpg'
    model = 'arn:aws:rekognition:us-east-1:905418420890:project/Tuwaiq_LandMarks_KSA/version/Tuwaiq_LandMarks_KSA.2024-02-10T17.08.49/1707574130097'
    min_confidence = 95

    # Detect custom labels
    response = show_custom_labels(model, bucket, photo, min_confidence)

    # Display the image with detected labels
    display_image(bucket, photo, response)

if __name__ == "__main__":
    main()
