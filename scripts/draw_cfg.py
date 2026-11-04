"""Explicitly laid out CFG; no inferred graph or generated test names.
Run with Python 3 and Pillow to rebuild cfg.png.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ROOT = Path(__file__).resolve().parents[1]
im = Image.new('RGB', (2900, 3150), 'white')
d = ImageDraw.Draw(im)
fontpath = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n): return ImageFont.truetype(fontpath, n)
f, small, title = font(27), font(23), font(48)
ink, blue = '#182f42', '#165d94'
def text(x,y,s,ft=f): d.text((x,y),s,font=ft,fill=ink)
def arrow(points, label, xy):
    d.line(points,fill=blue,width=4)
    (x0,y0),(x1,y1)=points[-2:]
    a=math.atan2(y1-y0,x1-x0)
    d.polygon([(x1,y1),(x1-16*math.cos(a-.45),y1-16*math.sin(a-.45)),(x1-16*math.cos(a+.45),y1-16*math.sin(a+.45))],fill=blue)
    text(*xy,label,small)
def box(x,y,w,h,label):
    d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill='#edf5fa',outline=ink,width=3)
    b=d.textbbox((0,0),label,font=f)
    text(x+(w-b[2])/2,y+(h-32)/2,label)
def node(n,y,label):
    d.polygon([(600,y),(900,y+60),(600,y+120),(300,y+60)],fill='#fff4d9',outline=ink,width=3)
    b=d.textbbox((0,0),label,font=f)
    text(600-b[2]/2,y+42,label)
    text(205,y+3,'N'+str(n))
p='scholarship_'
text(90,50,'scholarship() control flow graph',title)
text(90,125,'Each || and && operand is a separate decision. T / F = condition outcome.')
text(90,175,'Edge labels are exact JUnit method names. Repeated EXIT boxes denote the same exit.')
box(380,245,440,70,'N0  Entry')
arrow([(600,315),(600,370)],'E0  '+p+'negativeGpa_throws',(930,300))
ys={n:370+(n-1)*245 for n in range(1,10)}
labels=['gpa < 0','gpa > 4','credits < 0','hasViolation','gpa >= 3.8','credits >= 15','gpa >= 3.4','credits >= 12','gpa >= 3.0']
for n,label in enumerate(labels,1): node(n,ys[n],label)
# Each row has a true outcome; N5/N7 continue to the next operand.
true_names={1:'negativeGpa_throws',2:'gpaAboveFour_throws',3:'negativeCredits_throws',4:'violation_returns0',5:'highGpaEnoughCredits_returns100',6:'highGpaEnoughCredits_returns100',7:'middleGpaEnoughCredits_returns70',8:'middleGpaEnoughCredits_returns70',9:'threeGpa_returns50'}
false_names={1:'gpaAboveFour_throws',2:'negativeCredits_throws',3:'violation_returns0',4:'lowGpa_returns0',5:'middleGpaEnoughCredits_returns70',6:'highGpaTooFewFor100_returns70',7:'threeGpa_returns50',8:'middleGpaTooFewFor70_returns50',9:'lowGpa_returns0'}
edge=1
for n in range(1,10):
    y=ys[n]
    if n not in (5,7):
        result={1:'throw IllegalArgumentException',2:'throw IllegalArgumentException',3:'throw IllegalArgumentException',4:'return 0',6:'return 100',8:'return 70',9:'return 50'}[n]
        box(1870,y+22,850,76,'R'+str(n)+'  '+result+'  -> EXIT')
        arrow([(900,y+60),(1870,y+60)],f'E{edge} T  '+p+true_names[n],(950,y+18)); edge+=1
        dest=ys[n+1] if n<9 else y+245
        arrow([(600,y+120),(600,dest)],f'E{edge} F  '+p+false_names[n],(650,y+162)); edge+=1
    else:
        arrow([(600,y+120),(600,ys[n+1])],f'E{edge} T  '+p+true_names[n],(650,y+155)); edge+=1
        dest=ys[n+2]+60
        lane = 80 if n == 5 else 140
        arrow([(300,y+60),(lane,y+60),(lane,dest),(300,dest)],f'E{edge} F  '+p+false_names[n],(950,y+15)); edge+=1
# Bypass labels above share a horizontal guide with their source to make the edge association explicit.
for n in (5,7):
    y=ys[n]
    d.line([(300,y+60),(285,y+60)],fill=blue,width=4)
    text(950,y+60,'False edge follows the LEFT bypass',small)
box(380,ys[9]+245,440,70,'R10 return 0 -> EXIT')
text(90,2910,'Validation precedes hasViolation: invalid input always throws, even with a violation.')
text(90,2970,'The left bypasses show short circuit evaluation of the scholarship && conditions.')
text(90,3030,'Layout and edge mapping prepared explicitly with AI assistance; source: scripts/draw_cfg.py.',small)
im.save(ROOT/'cfg.png')

# Editable diagrams.net document with the same explicitly positioned nodes and edges.
import xml.etree.ElementTree as ET
mx = ET.Element('mxfile', host='app.diagrams.net')
page = ET.SubElement(mx, 'diagram', name='scholarship CFG', id='scholarship')
model = ET.SubElement(page, 'mxGraphModel', grid='1', page='1', pageWidth='2900', pageHeight='3150')
graph = ET.SubElement(model, 'root')
ET.SubElement(graph, 'mxCell', id='0')
ET.SubElement(graph, 'mxCell', id='1', parent='0')
def vertex(key, label, x, y, width, height, diamond=False):
    style = ('rhombus;' if diamond else 'rounded=1;') + 'whiteSpace=wrap;html=0;fontSize=24;'
    cell = ET.SubElement(graph, 'mxCell', id=key, value=label, style=style, vertex='1', parent='1')
    ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(width), height=str(height), attrib={'as':'geometry'})
vertex('N0', 'N0 Entry', 380, 245, 440, 70)
for n, label in enumerate(labels, 1):
    vertex(f'N{n}', f'N{n}  {label}', 300, ys[n], 600, 120, True)
returns={1:'throw IllegalArgumentException',2:'throw IllegalArgumentException',3:'throw IllegalArgumentException',4:'return 0',6:'return 100',8:'return 70',9:'return 50'}
for n, label in returns.items():
    vertex(f'R{n}', f'R{n}  {label} -> EXIT', 1870, ys[n]+22, 850, 76)
vertex('R10', 'R10 return 0 -> EXIT', 380, ys[9]+245, 440, 70)
def edge(number, source, target, label, lane=None):
    style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;endArrow=block;fontSize=20;labelBackgroundColor=#ffffff;'
    if lane is not None: style+='exitX=0;exitY=0.5;entryX=0;entryY=0.5;'
    elif target.startswith('R') and target!='R10': style+='exitX=1;exitY=0.5;entryX=0;entryY=0.5;'
    else: style+='exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
    cell=ET.SubElement(graph,'mxCell',id=f'E{number}',value=f'E{number}  {label}',style=style,edge='1',parent='1',source=source,target=target)
    geo=ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'})
    if lane is not None:
        pts=ET.SubElement(geo,'Array',attrib={'as':'points'})
        for y in (ys[int(source[1:])]+60,ys[int(target[1:])]+60):
            ET.SubElement(pts,'mxPoint',x=str(lane),y=str(y))
edge(0,'N0','N1',p+'negativeGpa_throws')
number=1
for n in range(1,10):
    edge(number,f'N{n}',f'N{n+1}' if n in (5,7) else f'R{n}','T '+p+true_names[n]); number+=1
    dest=f'N{n+2}' if n in (5,7) else (f'N{n+1}' if n<9 else 'R10')
    edge(number,f'N{n}',dest,'F '+p+false_names[n],(80 if n==5 else 140) if n in (5,7) else None); number+=1
ET.indent(mx)
ET.ElementTree(mx).write(ROOT/'cfg.drawio',encoding='utf-8',xml_declaration=True)
