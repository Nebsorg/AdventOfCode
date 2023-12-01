from PIL import Image

height = 600
width = 900

im = Image.new('RGB', (width, height))

distancemax = (width**2+height**2)**0.5

for x in range(width):
    for y in range(height):
        distancePoint = (x**2+y**2)**0.5

        ratio = distancePoint/distancemax

        valeur = 255-int(ratio*255)
        im.putpixel((x,y), (255, valeur, valeur))

im.save('testImg.png')