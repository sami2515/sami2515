#!/usr/bin/env python3
"""Create polished GitHub project cards; use only genuine site screenshots when supplied."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
p=argparse.ArgumentParser()
p.add_argument('--screenshots',default='site-screenshots')
p.add_argument('--out',default='assets')
a=p.parse_args()
folder=Path(a.screenshots); out=Path(a.out);out.mkdir(exist_ok=True,parents=True)
regular='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def ft(n,heavy=False):return ImageFont.truetype(bold if heavy else regular,n)
for key in ['testtayar','assurex']:
    source=folder/f'{key}.png'
    if not source.exists():
        print('No verified screenshot for',key,'—existing card kept')
        continue
    background = '#DBFBE8' if key=='testtayar' else '#191C33'
    titlecolor = '#113C32' if key=='testtayar' else '#F5F4FF'
    subcolor = '#386D62' if key=='testtayar' else '#C5C1E4'
    stroke = '#BEDDCB' if key=='testtayar' else '#5D587F'
    canvas=Image.new('RGB',(1380,532),background)
    d=ImageDraw.Draw(canvas)
    d.line([(0,429),(1380,429)],fill=stroke,width=2)
    d.line([(638,0),(638,532)],fill=stroke,width=2)
    d.text((57,51),'01  /  LIVE PLATFORM' if key=='testtayar' else '02  /  AI CLAIM ENGINE',font=ft(19,True),fill=subcolor)
    d.text((57,182),'TestTayar.pk' if key=='testtayar' else 'AssureX',font=ft(70 if key=='testtayar' else 81,True),fill=titlecolor)
    d.text((60,291),'Typing tests · MCQs · daily drills' if key=='testtayar' else 'Warranty claims powered by AI',font=ft(22),fill=subcolor)
    d.text((59,471),'OPEN LIVE WEBSITE  ↗',font=ft(22,True),fill=titlecolor)
    ss=Image.open(source).convert('RGB')
    # Actual screenshot, not a fake: resize to a contained browser window on the right.
    area=(700,62,1322,404)
    aw,ah=area[2]-area[0],area[3]-area[1]
    # cover the screenshot area without letterboxing and cut if necessary
    ratio=max(aw/ss.width,ah/ss.height)
    nw,nh=round(ss.width*ratio),round(ss.height*ratio)
    ss=ss.resize((nw,nh),Image.Resampling.LANCZOS)
    ss=ss.crop(((nw-aw)//2,(nh-ah)//2,(nw-aw)//2+aw,(nh-ah)//2+ah))
    shadow=Image.new('RGBA',(aw+32,ah+40),(0,0,0,0)); sh=ImageDraw.Draw(shadow)
    sh.rounded_rectangle((13,13,aw+13,ah+13),radius=19,fill=(0,0,0,62))
    shadow=shadow.filter(ImageFilter.GaussianBlur(13))
    canvas.paste(shadow,(area[0]-14,area[1]-10),shadow)
    mask=Image.new('L',(aw,ah),0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,aw-1,ah-1),radius=18,fill=255)
    canvas.paste(ss,(area[0],area[1]),mask)
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((area[0],area[1],area[2],area[3]),radius=18,outline=stroke,width=3)
    d.rectangle((0,0,1379,531),outline=stroke,width=2)
    path=out/f'{key}.png'
    canvas.save(path,optimize=True)
    print('updated',path,'from REAL screenshot',source)
