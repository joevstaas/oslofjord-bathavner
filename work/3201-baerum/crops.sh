# bruk: crops.sh out img x0,y0,x1,y1 [img x0,...]  -> qa/cc-<out>.jpg (2x2 eller 1x2)
out=$1; shift; n=0; files=()
while [ $# -gt 1 ]; do ../../.venv/bin/python -W ignore view.py $1 700 $2 >/dev/null; cp qa/view-$1.jpg qa/_c$n.jpg; files+=(qa/_c$n.jpg); n=$((n+1)); shift 2; done
../../.venv/bin/python -c "
import sys
from PIL import Image
ims=[Image.open(f) for f in sys.argv[2:]]
W=max(i.width for i in ims);H=max(i.height for i in ims);c=2 if len(ims)>1 else 1;r=(len(ims)+1)//2
can=Image.new('RGB',(c*W+10,r*H+10),'white')
for k,im in enumerate(ims): can.paste(im,((k%2)*(W+10),(k//2)*(H+10)))
can.save('qa/cc-'+sys.argv[1]+'.jpg',quality=85)" $out "${files[@]}"
