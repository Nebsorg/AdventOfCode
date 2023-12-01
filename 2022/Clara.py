from PIL import Image


hauteur = 700
largeur = 900

im = Image.new('RGB', (largeur, hauteur))
rouge=(255, 0,0)
blanc=(255,255,255)
bleu=(0,0,255) 
for y in range(hauteur):
    for x in range(largeur):
        if x<(largeur/3):
            im.putpixel((x,y), bleu)
        elif (x> largeur/3) and ( x<(largeur/3)*2):
                im.putpixel((x,y), blanc)
        else:
            im.putpixel((x,y), rouge)

im.save('testImg2.png')

