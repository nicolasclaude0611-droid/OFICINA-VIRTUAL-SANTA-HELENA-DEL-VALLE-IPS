import sys, numpy as np, cv2
from PIL import Image, ImageFilter, ImageChops, ImageEnhance
hel=Image.open(sys.argv[1]).convert('RGBA'); hat=Image.open(sys.argv[2]).convert('RGBA')
cx,cy,ancho,giro,curva=map(float,sys.argv[4:9])
PAD=220; S=720
# 1) curvar el gorro: los extremos del ala bajan (se "envuelve" en la cabeza)
h=np.array(hat).astype(np.float32); hh,hw=h.shape[:2]
mx,my=np.meshgrid(np.arange(hw),np.arange(hh))
t=(mx-hw*0.62)/(hw*0.38)                       # 0 en el centro del ala, ±1 en sus extremos
dy=curva*np.clip(t,-1.6,1.2)**2*np.clip((my/hh-0.45)/0.55,0,1)
h=cv2.remap(h,mx.astype(np.float32),(my-dy).astype(np.float32),cv2.INTER_LINEAR,borderValue=(0,0,0,0))
hat=Image.fromarray(np.clip(h,0,255).astype('uint8'),'RGBA')
# 2) armonizar color con la ilustración (un poco menos saturado y blanco más cálido)
rgb=hat.convert('RGB'); rgb=ImageEnhance.Color(rgb).enhance(0.9); rgb=ImageEnhance.Brightness(rgb).enhance(0.97)
r,g,b=rgb.split(); b=b.point(lambda v:int(v*0.96)); rgb=Image.merge('RGB',(r,g,b)); rgb.putalpha(hat.split()[-1]); hat=rgb
# 3) colocar
ax0,ax1,ay=0.245*hw,0.995*hw,0.80*hh
k=ancho/(ax1-ax0); a=np.deg2rad(giro)
R=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])*k
T=np.array([cx,cy+PAD])-R@np.array([(ax0+ax1)/2,ay])
M=np.hstack([R,T[:,None]]).astype(np.float32)
lay=cv2.warpAffine(np.array(hat).astype(np.float32),M,(S,S+PAD),flags=cv2.INTER_LANCZOS4,borderValue=(0,0,0,0))
lay=Image.fromarray(np.clip(lay,0,255).astype('uint8'),'RGBA')
can=Image.new('RGBA',(S,S+PAD),(0,0,0,0)); can.alpha_composite(hel,(0,PAD))
# 4) sombra del ala sobre el pelo y la frente (solo dentro de Helenita)
ha=lay.split()[-1]
sh=ha.transform(ha.size,Image.AFFINE,(1,0,0,0,1,-9)).filter(ImageFilter.GaussianBlur(7))
sh=ImageChops.subtract(sh,ha.filter(ImageFilter.MaxFilter(3)))
sh=ImageChops.multiply(sh,can.split()[-1]).point(lambda v:int(v*0.42))
dark=Image.new('RGBA',can.size,(60,25,15,0)); dark.putalpha(sh); can.alpha_composite(dark)
can.alpha_composite(lay)
bb=can.split()[-1].getbbox(); can.crop(bb).save(sys.argv[3]); print(can.crop(bb).size)
