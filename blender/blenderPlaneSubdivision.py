import bpy
import bmesh

# Создаём плоскость, параллельную плоскости XY
def newPlane_getVericies(loc, size, centerSize):
	
	[x, y, z]                  = loc
	[sizeX,       sizeY]       = size
	[centerSizeX, centerSizeY] = centerSize

	startCX = x + (sizeX - centerSizeX) / 2
	startCY = y + (sizeY - centerSizeY) / 2
	
	vertices = []
	
	for ix in range(2):
		for iy in range(2):
			vertices.append((x       + sizeX      *ix, y       + sizeY      *iy, z + 0))
			vertices.append((startCX + centerSizeX*ix, startCY + centerSizeY*iy, z + 0))
			
	return vertices

def newPlane_getFacesAndEdjes():

	faces = [
				(1, 3, 7, 5),
				(0, 1, 3, 2), (0, 1, 5, 4), (2, 3, 7, 6), (4, 5, 7, 6)
			]

	edjes = [
				(0, 2), (0, 4), (2, 6), (4, 6),
				(1, 3), (1, 5), (3, 7), (5, 7),
				(0, 1), (2, 3), (4, 5), (6, 7)
			]

	return faces, edjes


def getPlaneWithSubdivideCenter(loc, size, centerSize, subdivide=4):

	#Define vertices, faces, edges
	vertices       = newPlane_getVericies(loc, size, centerSize)
	[faces, edjes] = newPlane_getFacesAndEdjes()

	name = "Plane"

	#Define mesh and object
	mesh   = bpy.data.meshes.new(name)
	object = bpy.data.objects.new(name, mesh)

	#Set location and scene of object
	object.location = loc # bpy.context.scene.cursor_location
	#bpy.context.scene.objects.link(object)
	view_layer = bpy.context.view_layer
	view_layer.active_layer_collection.collection.objects.link(object)

	#Create mesh
	mesh.from_pydata(vertices, edjes, faces)
	mesh.update(calc_edges=False)


	object.select_set(True)
	view_layer.objects.active = object

	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.normals_make_consistent(inside=False)

	bm = bmesh.from_edit_mesh(mesh)
	for face in bm.faces:
		face.select = False

	bm.faces[0].select = True

	for i in range(subdivide):
		bpy.ops.mesh.subdivide()


	bpy.ops.object.mode_set(mode='OBJECT')

	# bpy.data.objects[name].select_set(True)
	object.select_set(True)
	view_layer.objects.active = object

	
	
loc = (0, 0, 0)
getPlaneWithSubdivideCenter(loc, (5, 5), (1, 1), 4)
