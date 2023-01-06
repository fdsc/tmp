# Использование итоговой иллюстрации не допускается
# Автор илллюстрации https://author.today/u/alrtat

# filename = "/Arcs/Repos/tmp/blender/2023/Площадь/stone.py"
# exec(compile(open(filename).read(), filename, 'exec'))

import sys
import os

import bpy
import bmesh
from math import *
from mathutils import *
from random import *


Samples   = 1024
Prefilter = 'ACCURATE'
CountOfCarbage = 186*2
use_denoising = True
SegmentsOfCurves = 64

SimpleRendering = True

if SimpleRendering:
    Samples   = 64
    Prefilter = 'FAST'
    # Prefilter = 'NONE'
    CountOfCarbage = 64
    use_denoising  = False
    SegmentsOfCurves = 16


blend_dir = os.path.dirname("/Arcs/Repos/tmp/blender/2023/Площадь/")
if blend_dir not in sys.path:
   sys.path.append(blend_dir)


import MaterialProperties
global MatProps

MatProps = MaterialProperties.MaterialProperties()

MatProps.DeleteAllObjects()


StonesCollectionName = 'Камни'
# Перед созданием коллекции убираем выделение с объектов, чтобы они не добавились по ошибке
bpy.ops.object.select_all(action='DESELECT')
StonesCollection = bpy.data.collections.new(StonesCollectionName)
bpy.context.scene.collection.children.link(StonesCollection)

view_layer        = bpy.context.view_layer
# StonesCollection  = bpy.data.collections[0] # Зачем?

# bpy.data.scenes[0].collection.children.link(StonesCollection)
# view_layer.active_layer_collection.collection.objects.link(StonesCollection)


# Создаём плоскость, параллельную плоскости XY
def СоздатьТочкиКамня():

    vertices = []

    # Масштабный коэффициент
    k = 1
    
    def создатьЗаготовкуЭллипса(r1, r2, cnt):
        points = []
        
        signs = [-1, +1]
        step  = 2*pi / cnt

        # Уравнение эллипса
        # x = a cos α
        # y = b sin α
        # 1 = x^2/a^2 + y^2/b^2
        #for s1 in signs:
            # for s2 in signs:
        #    points.append([s1*r1,  0*r2, 0]);
        #    points.append([ 0*r1, s1*r2, 0]);
            
        #    points.append([ 0*r1, s1*r2, 0]);
        for i in range(cnt):
            points.append([r1 * cos(step*i),  r2 * sin(step*i), 0])
            
        edges = []
        cnt   = 0
        for p in points:
            if cnt > 0:
                edges.append((cnt-1, cnt));
            cnt += 1

        edges.append((cnt-1, 0));

        return [points, edges]
    
    # Создаём псевдо-эллипс
    def getPseudoEllipse(center, r1, r2):
        None

    [points, eds] = создатьЗаготовкуЭллипса(1, 2, SegmentsOfCurves)
    cnt    = 0
    cnte   = 0
    face   = ()
    faces  = []
    edges  = []
    for p in points:
        vertices.append(p);
        face = face + (cnt,)
        cnt += 1

    for ie in range(len(eds)):
        e = eds[ie]
        edges.append((e[0] + cnte, e[1] + cnte));
    cnte += len(eds)

    # faces.append(face)

    return (vertices, faces, edges)


def СоздатьКамень():
    [vertices, faces, edjes] = СоздатьТочкиКамня()

    name = 'Камень'
    [object, mesh] = MatProps.createObject(
        name=name, vertices=vertices, faces=faces, edjes=edjes, loc0=(0, 0, 0)
        )

    
СоздатьКамень()





for obj in bpy.data.objects:
	obj.display_type = 'SOLID'
    # obj.display_type = 'TEXTURED'

# Добавляем настройки рендера
bpy.data.scenes[0].render.engine = 'CYCLES'
bpy.data.scenes[0].cycles.preview_samples = 16
bpy.data.scenes[0].cycles.samples = Samples
# bpy.data.scenes[0].cycles.seed = 0
bpy.data.scenes[0].cycles.denoising_prefilter = Prefilter
bpy.data.scenes[0].cycles.use_denoising = use_denoising
# Эта штука позволяет сделать сцену более освещённой при рендеринге
bpy.data.scenes[0].cycles.volume_step_rate = 0.01


try:
	bpy.data.worlds["World"].node_tree.nodes.remove(bpy.data.worlds["World"].node_tree.nodes["Background"])
except:
	None
