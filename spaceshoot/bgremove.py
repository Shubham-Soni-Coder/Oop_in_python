from rembg import remove
from PIL import Image
import io

def remove_background(input_image_path,output_image_path):
    
    # Open the input image
    with open(input_image_path, 'rb') as input_file:
        input_image = input_file.read()   
    # Remove background
    output_image = remove(input_image)
    
    # Save the output image
    with open(output_image_path, 'wb') as output_file:
        output_file.write(output_image)

if __name__ == "__main__":
    # Input and output image file paths
    input_path =  'assests/medkit.jpg' # Replace with your input image path
    output_path = 'assests/temp.png'# Output as PNG to retain transparency

    # Remove background
    remove_background(input_path,output_path)

    print(f'Background removed and saved at {output_path}')
