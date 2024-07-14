from PIL import Image, ImageDraw, ImageFont
from database import equation

def create_equation(number):
    image = Image.open("Equation/white_bg.png")  # Open the background image within the function
    font = ImageFont.truetype("arial.ttf", 100)
    drawer = ImageDraw.Draw(image)
    drawer.text((240, 190), f"{list(equation.keys())[number]}", font=font, fill='black')
    image.save('Equation/new_img.png')

# Example call to test the function
# create_equation(0)  # This would create an image with the first equation in the dictionary

