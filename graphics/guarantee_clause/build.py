import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(7)
W,H=1080,1350
G='/usr/share/fonts/truetype/sand-box/google/Crimson Text/'
def f(n,s): return ImageFont.truetype(G+n,s)
BOLD='CrimsonText-Bold.ttf'; REG='CrimsonText-Regular.ttf'; IT='CrimsonText-Italic.ttf'
RED=(140,20,25); GOLD=(184,140,52); INK=(45,30,20)
# parchment
im=Image.new('RGB',(W,H),(236,222,190)); px=im.load()
for y in range(H):
    for x in range(W):
        n=random.randint(-10,10); dx=(x-W/2)/(W/2); dy=(y-H/2)/(H/2); v=int(38*(dx*dx+dy*dy))
        r,g,b=px[x,y]; px[x,y]=(r+n-v,g+n-v,b+n-int(v*1.2))
im=im.filter(ImageFilter.GaussianBlur(0.8)); d=ImageDraw.Draw(im)
# prairie grass texture at bottom
for i in range(1400):
    x=random.randint(0,W); h=random.randint(30,120); lean=random.randint(-25,25)
    d.line([(x,H),(x+lean,H-h)],fill=(176,150,95),width=2)
# capitol silhouette (Nebraska State Capitol: wide base, tall tower, dome, sower)
cx=W//2; base=H-90; sil=(150,115,70)
d.rectangle([cx-330,base-110,cx+330,base],fill=sil)
d.rectangle([cx-230,base-150,cx+230,base-110],fill=sil)
d.rectangle([cx-70,base-330,cx+70,base-150],fill=sil)
for k in range(-50,60,25): d.rectangle([cx+k-6,base-310,cx+k+6,base-170],fill=(165,130,85))
d.rectangle([cx-55,base-365,cx+55,base-330],fill=sil)
d.pieslice([cx-55,base-415,cx+55,base-315],180,360,fill=sil)
d.rectangle([cx-3,base-440,cx+3,base-410],fill=sil); d.ellipse([cx-9,base-452,cx+9,base-434],fill=sil)
d.rectangle([0,base,W,H],fill=(176,150,95))
# borders
d.rectangle([24,24,W-24,H-24],outline=RED,width=10); d.rectangle([44,44,W-44,H-44],outline=GOLD,width=3)
def c(y,t,font,fill):
    w=d.textlength(t,font=font); d.text(((W-w)/2,y),t,font=font,fill=fill)
c(80,'DID YOU KNOW?',f(BOLD,58),GOLD)
d.line([(W/2-200,160),(W/2+200,160)],fill=GOLD,width=3)
c(185,"It's NOT your job",f(BOLD,92),RED)
c(290,'to prove our elections',f(BOLD,70),INK)
c(370,'are free and fair.',f(BOLD,70),INK)
c(480,'The Guarantee Clause puts that on the government.',f(IT,40),INK)
c(545,'"The United States shall guarantee to every State in this',f(REG,32),INK)
c(585,'Union a Republican Form of Government."',f(REG,32),INK)
c(625,'U.S. Constitution, Article IV, Section 4',f(IT,28),RED)
c(690,'Executive Order 14399, March 31, 2026 (91 FR 17125):',f(BOLD,30),RED)
c(730,'"The Federal Government has an unavoidable duty',f(IT,32),INK)
c(770,'under Article II ... to enforce Federal law."',f(IT,32),INK)
im.save('Guarantee_Clause.png')
