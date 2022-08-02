import sys
import os

import bpy
import bmesh
from math import *
from mathutils import *
from random import *


blend_dir = os.path.dirname("/Arcs/Repos/tmp/blender/2022/ОктавияКолотилина/")
if blend_dir not in sys.path:
   sys.path.append(blend_dir)


import MaterialProperties
global MatProps

MatProps = MaterialProperties.MaterialProperties()


loc0 = (0, 0, 0)
size = (1, 1, 1)
vertices = []

# Точки сверху: +1
# Точки, дальние по оси y: +2
# Точки, смещённые по оси x: +4
for ix in range(2):
	for iy in range(2):
		for iz in range(2):
			loc = (loc0[0] + size[0]*ix, loc0[1] + size[1]*iy, loc0[2] + size[2]*iz)
			vertices.append(loc)

faces = []
faces.append((0, 1, 5, 4))
faces.append((0, 1, 3, 2))
faces.append((0, 2, 6, 4))
faces.append((7, 5, 1, 3))
faces.append((7, 5, 4, 6))
faces.append((7, 3, 2, 6))

MatProps.createObject("Cube", vertices, faces, [])
