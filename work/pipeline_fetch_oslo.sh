#!/bin/bash
# Oslo: vent til hovedkøen er ferdig, deretter samme innhenting.
cd "$(dirname "$0")"
while pgrep -f pipeline_fetch.sh >/dev/null; do sleep 30; done
d=0301-oslo
(cd $d && ../../.venv/bin/python fetch_images.py scan-topo.json topo > raw/fetch-topo.log 2>&1
 ../../.venv/bin/python -W ignore shore_cells.py > raw/shore.log 2>&1
 ../../.venv/bin/python -c "
import json
c=json.load(open('cells.json'))
sel=[x for x in c if x['water_frac'] and 0.02<x['water_frac']<0.99]
json.dump([dict(id='d-'+x['cell'],bbox=[x['bbox'][0]-50,x['bbox'][1]-50,x['bbox'][2]+50,x['bbox'][3]+50],width=1320,height=1320,cell=x['cell']) for x in sel],open('detail-esri.json','w'),indent=1)
print(len(sel))" > raw/detail-count.txt
 ../../.venv/bin/python fetch_images.py detail-esri.json esri > raw/fetch-detail.log 2>&1
 ../../.venv/bin/python fetch_images.py scan-esri.json esri > raw/fetch-esri.log 2>&1
 echo "$d ferdig $(date -u +%H:%M:%S) detail=$(cat raw/detail-count.txt) errors=$(cat raw/fetch-*.log | grep -c ERROR)")
