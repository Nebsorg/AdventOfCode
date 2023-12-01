from PIL import Image


hauteur = 704
largeur = 904

im = Image.new('RGB', (largeur, hauteur))
noir = (0,0,0)
blanc = (255,255,255)

largeur_case = int(largeur / 8)
hauteur_case = int(hauteur / 8)

for y in range(hauteur):
    for x in range(largeur):
        if (int(y/hauteur_case))%2 == 0:
            ## on va ecrire une ligne du damier, qui commence par un carré noir
            if (int(x/largeur_case))%2 == 0:
                couleur = noir
            else:
                couleur = blanc
        else:
            ## on va ecrire une ligne du damier, qui commence par un carré blanc
            if (int(x/largeur_case))%2 == 0:
                couleur = blanc
            else:
                couleur = noir
       
        
        im.putpixel((x,y), couleur)

im.save('testImg3.png')