'''
Tool History Layout
---

| General           | Workpiece Data      | Process Data           | Tool Data                |
| ---               | ---                 | ---                    | ---                      |
| RefNr             | Workpiece Material  | Cutting Speed vC       | Cutting Edge Diameter DC |
| Date of Experiment|                     | Spindle Speed n        | Coating Material         |
| Name of Experiment|                     | Feed Rate vf           | Tool Material            |
| Workpiece ID      |                     | Feed Rate per Tooth fz | No. Teeth Z              |
| Process ID        |                     | Number Cuts nC         | Helix Angle              |
| Tool ID           |                     | Cutting Length lC      | Overall Length L         |


Image and Mask Data Layout
---

Two databases with this layout: one for images and one for masks. Referencing between them with the same Image Nr.

Training Images and Masks:


'''
from header import *

TOOL_HISTORY_PATH = join(CWD, 'data', 'toolHistory.db')
IMAGES_DB_PATH = join(CWD, 'data', 'images.db')


CONN_TH = sql.connect(TOOL_HISTORY_PATH)
CONN_IMG_DB = sql.connect(IMAGES_DB_PATH)

