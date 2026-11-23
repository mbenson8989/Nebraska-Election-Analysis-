import csv
from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
def f(s): return ImageFont.truetype(F,s)
RED=(208,2,27); GRAY=(120,120,120); BLK=(0,0,0); WHT=(255,255,255)
R=[r for r in csv.DictReader(open('/workspace/nebraska-elections/spec_check/residual_votes_20261119/computed.csv')) if int(r['reg_dem_2026'])<int(r['reg_dem_2022'])]
for r in R: r['g']=float(r['gap'])
top=sorted(R,key=lambda r:-r['g'])[:10]
n=lambda x:f'{int(x):,}'
def ctext(d,y,t,font,fill,W=1080):
    w=d.textlength(t,font=font); d.text(((W-w)/2,y),t,font=font,fill=fill)
def fitfont(d,t,size,maxw):
    while d.textlength(t,font=f(size))>maxw: size-=2
    return f(size)
def arrow(d,cx,top_,h,w,up,col):
    sw=w*0.42; hh=h*0.42
    if up: pts=[(cx,top_),(cx+w/2,top_+hh),(cx+sw/2,top_+hh),(cx+sw/2,top_+h),(cx-sw/2,top_+h),(cx-sw/2,top_+hh),(cx-w/2,top_+hh)]
    else: pts=[(cx,top_+h),(cx+w/2,top_+h-hh),(cx+sw/2,top_+h-hh),(cx+sw/2,top_),(cx-sw/2,top_),(cx-sw/2,top_+h-hh),(cx-w/2,top_+h-hh)]
    d.polygon(pts,fill=col,outline=BLK,width=4)
rows=[]
for i,r in enumerate(top,1):
    c=r['county']; rd22,rd26=int(r['reg_dem_2022']),int(r['reg_dem_2026']); d22,d26=int(r['D_2022']),int(r['D_2026'])
    rows.append((i,c,rd22,rd26,d22,d26,round(r['g']),100*r['g']/float(r['race_votes_2026']),float(r['dG_r']),r['population']))
    im=Image.new('RGB',(1080,1350),WHT); d=ImageDraw.Draw(im)
    d.rectangle([0,0,1080,210],fill=BLK)
    ctext(d,28,f'#{i} OF 93 NEBRASKA COUNTIES',f(34),(255,210,210))
    ctext(d,78,c.upper()+' COUNTY',fitfont(d,c.upper()+' COUNTY',100,1000),WHT)
    # reg block
    arrow(d,130,270,170,130,False,GRAY)
    d.text((240,262),'REGISTERED DEMOCRATS',font=f(40),fill=BLK)
    d.text((240,312),f'{n(rd22)} \u2192 {n(rd26)}',font=fitfont(d,f'{n(rd22)} \u2192 {n(rd26)}',84,800),fill=BLK)
    d.text((240,408),f'{n(rd26-rd22)}  (2022 \u2192 2026)',font=f(44),fill=GRAY)
    # vote block
    arrow(d,130,540,220,150,True,RED)
    d.text((240,540),'DEMOCRATIC VOTES',font=f(40),fill=RED)
    d.text((240,585),'FOR GOVERNOR',font=f(40),fill=RED)
    d.text((240,640),f'{n(d22)} \u2192 {n(d26)}*',font=fitfont(d,f'{n(d22)} \u2192 {n(d26)}*',84,800),fill=RED)
    d.text((240,738),f'+{n(d26-d22)}*  (+{100*(d26-d22)/d22:.0f}%*)',font=f(48),fill=RED)
    # residual band
    d.rectangle([0,860,1080,1150],fill=RED)
    ctext(d,885,'VOTES NOT EXPLAINED BY REGISTRATION',f(42),WHT)
    ctext(d,945,f'+{n(round(r["g"]))}*',f(150),WHT)
    ctext(d,1110,f'{100*r["g"]/float(r["race_votes_2026"]):.1f}% of the 2026 governor vote*',f(30),WHT) if False else None
    ctext(d,1170,f'That is {100*r["g"]/float(r["race_votes_2026"]):.1f}% of the 2026* governor race.',f(36),BLK)
    ctext(d,1235,'Fewer Democrats registered. More Democratic votes.',f(34),BLK)
    ctext(d,1295,'Source: Nebraska Secretary of State. *2026 unofficial.',f(26),GRAY)
    im.save(f'{i:02d}_{c.replace(" ","_")}.png')
# summary
im=Image.new('RGB',(1080,1350),WHT); d=ImageDraw.Draw(im)
d.rectangle([0,0,1080,200],fill=BLK)
ctext(d,30,'TEN NEBRASKA COUNTIES',f(64),WHT)
ctext(d,115,'Fewer Democrats registered. More Democratic votes.',f(36),(255,210,210))
ctext(d,225,'Votes not explained by registration, 2022 \u2192 2026*',f(34),BLK)
mx=max(r[6] for r in rows); y=290
for (i,c,rd22,rd26,d22,d26,g,pct,dg,pop) in rows:
    d.text((40,y+8),f'{i}. {c}',font=f(36),fill=BLK)
    L=int(480*g/mx); d.rectangle([370,y,370+max(L,6),y+56],fill=RED)
    d.text((370+max(L,6)+14,y+8),f'+{g:,}*',font=f(36),fill=BLK)
    y+=88
ctext(d,1180,'Each county: registered Democrats fell, Democratic votes for governor rose.',f(28),BLK)
ctext(d,1225,'Residual = 2026 Dem votes \u2212 2022 Dem votes \u00d7 (2026 Dem reg \u00f7 2022 Dem reg)',f(26),GRAY)
ctext(d,1295,'Source: Nebraska Secretary of State. *2026 unofficial.',f(26),GRAY)
im.save('00_Summary_Top10.png')
with open('top10_flip.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['rank','county','reg_dem_2022','reg_dem_2026','dem_votes_2022','dem_votes_2026*','residual_votes*','residual_pct_of_race*','deltaG*','population'])
    for r in rows: w.writerow([r[0],r[1],r[2],r[3],r[4],r[5],r[6],f'{r[7]:.2f}',f'{r[8]:.2f}',r[9]])
