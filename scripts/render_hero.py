from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random
W,H=1000,450
root=Path(__file__).resolve().parents[1]/"assets"
random.seed(42)
stars=[(random.randrange(W),random.randrange(H),random.randrange(1,4),random.random()*6.28) for _ in range(145)]
font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
small="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def glow(canvas, draw_fn, blur, color=(143,56,255), strength=0.75):
    layer=Image.new("RGBA",(W,H));d=ImageDraw.Draw(layer);draw_fn(d)
    halo=layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(halo)
    canvas.alpha_composite(layer)
frames=[]
for frame in range(30):
    t=frame*2*math.pi/30
    im=Image.new("RGBA",(W,H),(7,5,17,255))
    d=ImageDraw.Draw(im,"RGBA")
    for radius in range(340,40,-14):
        alpha=int(1.5+(340-radius)/340*9)
        d.ellipse((710-radius,220-radius,710+radius,220+radius),fill=(91,25,175,alpha))
    for x,y,r,phase in stars:
        v=int(85+150*(0.5+0.5*math.sin(t+phase)))
        d.ellipse((x-r/2,y-r/2,x+r/2,y+r/2),fill=(195,157,255,v))
    cx,cy=745,222
    def ring(dr):
        dr.ellipse((cx-193,cy-83,cx+193,cy+83),outline=(148,74,255,135),width=5)
        dr.ellipse((cx-175,cy-68,cx+175,cy+68),outline=(217,161,255,180),width=2)
    glow(im,ring,17)
    d=ImageDraw.Draw(im,"RGBA")
    for radius in range(113,70,-3):
        alpha=max(2,int((113-radius)*0.6))
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=(110,38,224,alpha))
    d.ellipse((cx-88,cy-88,cx+88,cy+88),fill=(60,24,120,255),outline=(181,111,255,255),width=3)
    for k in range(20):
        xx=cx-75+k*8
        width=math.sqrt(max(0,88**2-(xx-cx)**2))
        if width>5:
            d.line((xx,cy-width+12*math.sin(k*.7+t*.35),xx+5,cy+width*.55),fill=(118+k*3,60+k*2,192+k*2,38),width=5)
    d.arc((cx-193,cy-83,cx+193,cy+83),5,175,fill=(225,165,255,235),width=5)
    x=cx+193*math.cos(t);y=cy+83*math.sin(t)
    def satellite(dr):dr.ellipse((x-8,y-8,x+8,y+8),fill=(239,192,255,255))
    glow(im,satellite,14)
    d=ImageDraw.Draw(im)
    d.text((45,42),"OTHMANE TAHIRI  /  BRAND DESIGNER",font=ImageFont.truetype(small,17),fill=(188,142,255))
    for i,(line,size) in enumerate([("I BUILD",57),("VISUAL",66),("IDENTITIES",52),("THAT PEOPLE",43),("REMEMBER.",55)]):
        d.text((43,94+i*57),line,font=ImageFont.truetype(font,size),fill=(249,241,255) if i in (1,2) else (203,155,255),stroke_width=0)
    d.rounded_rectangle((43,401,393,424),radius=8,fill=(64,25,107))
    d.text((58,404),"DESIGNING WHAT PEOPLE REMEMBER",font=ImageFont.truetype(small,12),fill=(224,196,255))
    frames.append(im.convert("RGB"))
frames[0].save(root/"animated-hero.gif",save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=2)
print("Generated",root/"animated-hero.gif")
