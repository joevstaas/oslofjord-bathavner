import json
from pathlib import Path
P=Path(__file__).parent
(P/"details.json").write_text(json.dumps([dict(id="detail-oppegard",bbox=[262200,6639650,262800,6640250],width=1500,height=1500)]))
