import bpy

def clear_scene():
    """Nukes everything in the current Blender scene and prevents memory leaks."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    for cam in bpy.data.cameras:
        bpy.data.cameras.remove(cam)
    for ng in bpy.data.node_groups:
        if ng.name.startswith("TubeGen_"):
            bpy.data.node_groups.remove(ng)
    print("🧹 SCENE BUILDER: Dark Void Cleared.")


def setup_world_lighting():
    """Sets render engine, dark void background, switches viewport to RENDERED."""
    # Blender 5.0 uses 'BLENDER_EEVEE'; Blender 4.2-4.x used 'BLENDER_EEVEE_NEXT'
    if (4, 2, 0) <= bpy.app.version < (5, 0, 0):
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    bpy.context.scene.render.fps = 60

    world = bpy.data.worlds.get("World")
    if world and world.use_nodes:
        bg_node = world.node_tree.nodes.get("Background")
        if bg_node:
            bg_node.inputs[0].default_value = (0.005, 0.005, 0.01, 1.0)

    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'RENDERED'
                            space.shading.use_scene_lights = True
                            space.shading.use_scene_world = True
        print("✅ Viewport → RENDERED mode activated.")
    except Exception:
        print("⚠️  Press Z → Rendered manually.")


def give_thickness(obj, thickness=0.015):
    """
    Converts 1D math lines into solid 3D tubes using Geometry Nodes.
    This preserves vertex animation (Shape Keys) unlike SKIN modifier.
    """
    mod = obj.modifiers.new(name="Neon_Tube", type='NODES')
    tree = bpy.data.node_groups.new(name=f"TubeGen_{obj.name}", type='GeometryNodeTree')
    mod.node_group = tree

    tree.interface.new_socket(name="Geometry", in_out='INPUT',  socket_type='NodeSocketGeometry')
    tree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')

    nodes = tree.nodes
    links = tree.links

    in_node  = nodes.new('NodeGroupInput')
    out_node = nodes.new('NodeGroupOutput')
    m2c      = nodes.new('GeometryNodeMeshToCurve')
    c2m      = nodes.new('GeometryNodeCurveToMesh')
    circle   = nodes.new('GeometryNodeCurvePrimitiveCircle')
    set_mat  = nodes.new('GeometryNodeSetMaterial')

    circle.inputs['Radius'].default_value = thickness
    circle.inputs['Resolution'].default_value = 8

    if obj.data.materials:
        set_mat.inputs['Material'].default_value = obj.data.materials[0]

    links.new(in_node.outputs[0],  m2c.inputs[0])
    links.new(m2c.outputs[0],      c2m.inputs[0])
    links.new(circle.outputs[0],   c2m.inputs[1])
    links.new(c2m.outputs[0],      set_mat.inputs[0])
    links.new(set_mat.outputs[0],  out_node.inputs[0])


def build_grid(material, size=5, step=1):
    """Builds the 2D wireframe grid on the XY plane."""
    verts, edges = [], []
    for y in range(-size, size + 1, step):
        v = len(verts)
        verts += [(-size, y, 0.0), (size, y, 0.0)]
        edges.append((v, v + 1))
    for x in range(-size, size + 1, step):
        v = len(verts)
        verts += [(x, -size, 0.0), (x, size, 0.0)]
        edges.append((v, v + 1))

    mesh = bpy.data.meshes.new("MathGrid_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new("MathGrid", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    give_thickness(obj, thickness=0.015)
    return obj


def build_arrow(name, color_mat, tip_coord):
    """Builds a thick 3D basis vector arrow floating above the grid."""
    x, y  = float(tip_coord[0]), float(tip_coord[1])
    z_lift = 0.1   # prevents Z-fighting with grid

    verts = [(0.0, 0.0, z_lift), (x, y, z_lift)]
    edges = [(0, 1)]

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(color_mat)
    give_thickness(obj, thickness=0.06)
    return obj


def setup_camera():
    """Top-down orthographic camera looking straight down -Z."""
    cam_data = bpy.data.cameras.new("Main_Cam")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = 14.0

    cam_obj = bpy.data.objects.new("Camera", cam_data)
    cam_obj.location = (0.0, 0.0, 10.0)
    cam_obj.rotation_euler = (0.0, 0.0, 0.0)

    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    return cam_obj
