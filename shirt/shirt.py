import sys
import os
from PIL import Image, ImageOps

def main():
    # The correct command-line arguments
    if len(sys.argv) != 3:
        sys.exit("This is how to use: python shirt.py input_image output_image")

    input_image = sys.argv[1]
    output_image = sys.argv[2]

    # File extensions
    valid_extensions = (".jpg", ".jpeg", ".png")
    input_path = os.path.splitext(input_image)[1].lower()
    output_path = os.path.splitext(output_image)[1].lower()

    if input_path not in valid_extensions or output_path not in valid_extensions:
        sys.exit("Input and Output must be jpg, jpeg or png")

    if input_path != output_path:
        sys.exit("Both files must be the same jpg, jpeg or png")

    # Try opening the image if there is one.
    try:
        input_img = Image.open(input_image)
    except FileNotFoundError:
        sys.exit("Input does not existo")

    shirt = Image.open("shirt.png") # speaks for itself

    # resizing, cropping, to match the shirt
    resize_image = ImageOps.fit(input_img, shirt.size)

    # overlaying to achieve a good fit
    resize_image.paste(shirt, shirt)

    # saving it!
    resize_image.save(output_image)

if __name__ == "__main__":
    main()
