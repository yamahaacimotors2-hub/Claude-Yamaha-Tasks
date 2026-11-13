"""MT-15 "Map loads under the wheel" - construction-beat proof v3 (Blender 5.x / bpy, Cycles CPU).

Usage:  python3 proof.py --cam H --frames 30-101 --out renders/H [--samples 14] [--mblur] [--blend scene.blend]
        blender -b -P proof.py -- --cam H --frames 30-101 --out renders/H

Locked map (SOP v2): one right-hand bend, WATER ON THE LEFT, tea stall and buildings on the
right. The bike keeps to the left lane (Bangladesh drives on the left), next to the waterside kerb.

Every module (kerb stone, rail post, lamp, stall part, facade) stores its distance `s` along
the route and is activated when the headlight contact point (s_bike + FRONT) reaches it:
    seat (drops into its slot) -> material (clay -> final) -> practical light on.
The bike only moves forward, so everything behind it stays built.

Cameras:  H = hero, low beside the front wheel (SOP shot S08)
          B = aerial (S09)      C = rear chase (S10)      D = kerb-side, no bike (diagnostic)
The bike is an UNBRANDED proxy. Only the front wheel, fork and fender are modelled with care,
because those are the only bike parts the hero shot shows.
"""
import argparse
import math
import random
import sys

import bpy
import bmesh  # must come after bpy when using the pip module
from mathutils import Matrix

# ---------------------------------------------------------------- parameters
FPS, NFRAMES = 24, 120
R = 70.0            # bend radius (m); the road bends to the right
SPEED = 8.0         # m/s (~29 km/h, normal riding speed)
S0 = 6.0            # bike start distance along route
FRONT = 6.0         # headlight contact point, metres ahead of the bike
HALF_ROAD = 3.5
WATER = +1          # lateral sign of the water side: +1 = left of travel
BUILT = -WATER      # stall and buildings on the other side
BIKE_LAT = WATER * 1.9          # left-lane riding line
WHEEL_R = 0.30
S_MIN, S_MAX = -14.0, 84.0
random.seed(7)


def s_bike(frame):
    return S0 + SPEED * (frame - 1) / FPS


def frame_for(s):
    """Frame at which the build front reaches distance s."""
    return 1 + (s - FRONT - S0) / SPEED * FPS


def route(s, lat=0.0, z=0.0):
    """World position at distance s along the route, lat metres to the LEFT of travel."""
    a = s / R
    return (R - R * math.cos(a) - lat * math.cos(a), R * math.sin(a) + lat * math.sin(a), z)


def heading(s):
    return -s / R       # rotation_z that points local +Y along the route (local +X = right)


# ---------------------------------------------------------------- materials
def principled(name, color=None, rough=None, metal=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    if color:
        b.inputs["Base Color"].default_value = (*color, 1)
    if rough is not None:
        b.inputs["Roughness"].default_value = rough
    if metal is not None:
        b.inputs["Metallic"].default_value = metal
    return m, m.node_tree, b


def make_materials():
    mats = {}
    CLAY = (0.20, 0.22, 0.27, 1)
    mats["clay"] = principled("clay", CLAY[:3], 0.9)[0]

    # module: clay until activated; object colour = final colour, object alpha = activation
    m, nt, b = principled("module", rough=0.6)
    info = nt.nodes.new("ShaderNodeObjectInfo")
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = CLAY
    nt.links.new(info.outputs["Alpha"], mix.inputs["Factor"])
    nt.links.new(info.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    mats["module"] = m

    # emitter: dark until activated, then glows in the object colour
    for name, strength in (("emit", 2.2), ("neon", 30.0)):
        m, nt, b = principled(name, (0.05, 0.05, 0.06))
        info = nt.nodes.new("ShaderNodeObjectInfo")
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = strength
        nt.links.new(info.outputs["Alpha"], mul.inputs[0])
        nt.links.new(info.outputs["Color"], b.inputs["Emission Color"])
        nt.links.new(mul.outputs[0], b.inputs["Emission Strength"])
        mats[name] = m

    # wet asphalt: a real glossy surface, puddles from a noise-driven roughness
    m, nt, b = principled("wet_road", (0.018, 0.018, 0.022))
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.35
    noise.inputs["Detail"].default_value = 3.0
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["From Min"].default_value = 0.42
    ramp.inputs["From Max"].default_value = 0.62
    ramp.inputs["To Min"].default_value = 0.04
    ramp.inputs["To Max"].default_value = 0.32
    coord = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(coord.outputs["Object"], noise.inputs["Vector"])
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Value"])
    nt.links.new(ramp.outputs["Result"], b.inputs["Roughness"])
    mats["wet_road"] = m

    mats["water"] = principled("water", (0.01, 0.012, 0.02), 0.03)[0]
    mats["slot"] = principled("slot", (0.004, 0.004, 0.005), 1.0)[0]
    mats["paint"] = principled("paint", (0.55, 0.55, 0.5), 0.5)[0]
    mats["proxy"] = principled("proxy", (0.05, 0.055, 0.06), 0.35)[0]       # unbranded graphite
    mats["tyre"] = principled("tyre", (0.012, 0.012, 0.012), 0.75)[0]
    mats["rim_cyan"] = principled("rim_cyan", (0.0, 0.50, 0.66), 0.28, 0.6)[0]
    mats["fork_gold"] = principled("fork_gold", (0.80, 0.55, 0.12), 0.22, 1.0)[0]
    mats["chrome"] = principled("chrome", (0.75, 0.76, 0.78), 0.12, 1.0)[0]
    mats["disc"] = principled("disc", (0.55, 0.56, 0.58), 0.30, 1.0)[0]
    mats["fender"] = principled("fender", (0.16, 0.17, 0.19), 0.35, 0.4)[0]

    m, nt, b = principled("headlamp")
    b.inputs["Emission Color"].default_value = (0.85, 0.93, 1, 1)
    b.inputs["Emission Strength"].default_value = 60
    mats["headlamp"] = m
    return mats


# ---------------------------------------------------------------- mesh helpers
def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def mesh_object(name, boxes, mat, loc=(0, 0, 0), rot_z=0.0):
    """One object made of several boxes; each box = ((cx, cy, cz), (sx, sy, sz)) in local space."""
    bm = bmesh.new()
    for (cx, cy, cz), (sx, sy, sz) in boxes:
        geom = bmesh.ops.create_cube(bm, size=1.0)
        for v in geom["verts"]:
            v.co.x, v.co.y, v.co.z = v.co.x * sx + cx, v.co.y * sy + cy, v.co.z * sz + cz
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    ob.location, ob.rotation_euler = loc, (0, 0, rot_z)
    return link(ob)


def matrix_object(name, matrices, mat):
    """One object made of unit cubes, each placed by its own 4x4 matrix (for rotated parts)."""
    bm = bmesh.new()
    for mtx in matrices:
        bmesh.ops.create_cube(bm, size=1.0, matrix=mtx)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    return link(bpy.data.objects.new(name, me))


def op_object(mat, smooth=True):
    """Finish an object just created with bpy.ops (torus / cylinder)."""
    ob = bpy.context.object
    ob.data.materials.append(mat)
    if smooth:
        ob.data.polygons.foreach_set("use_smooth", [True] * len(ob.data.polygons))
    return ob


def strip(name, lat_a, lat_b, z, mat, step=1.0):
    """Ground strip that follows the route between two lateral offsets."""
    bm = bmesh.new()
    prev, s = None, S_MIN
    while s <= S_MAX + 1e-6:
        cur = (bm.verts.new(route(s, lat_a, z)), bm.verts.new(route(s, lat_b, z)))
        if prev:
            bm.faces.new((prev[0], prev[1], cur[1], cur[0]))
        prev, s = cur, s + step
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    return link(bpy.data.objects.new(name, me))


# ---------------------------------------------------------------- activation
def key(ob, path, frame):
    ob.keyframe_insert(data_path=path, frame=round(frame))


def seat(ob, s, delay=0.0, drop=0.7, grow=False):
    """Physically seat a module when the build front reaches s."""
    f0 = frame_for(s) + delay
    if f0 <= 1:                       # already built behind the bike at the start
        ob.color[3] = 1.0
        return
    x, y, z = ob.location
    if grow:                          # poles/posts rise out of their socket
        ob.scale = (1, 1, 0.0); key(ob, "scale", f0)
        ob.scale = (1, 1, 1.08); key(ob, "scale", f0 + 6)
        ob.scale = (1, 1, 1.0); key(ob, "scale", f0 + 9)
    else:                             # stones/panels appear above the slot and drop in
        ob.scale = (0, 0, 0); key(ob, "scale", f0)
        ob.scale = (1, 1, 1); key(ob, "scale", f0 + 1)
        ob.location = (x, y, z + drop); key(ob, "location", f0 + 1)
        ob.location = (x, y, z); key(ob, "location", f0 + 6)
        ob.location = (x, y, z + 0.035); key(ob, "location", f0 + 8)
        ob.location = (x, y, z); key(ob, "location", f0 + 10)
    ob.color[3] = 0.0; key(ob, "color", f0 + 6)      # material arrives after it is seated
    ob.color[3] = 1.0; key(ob, "color", f0 + 13)


def glow(ob, s, delay):
    """Emitter that is installed, then switches on `delay` frames after the front reaches s."""
    f0 = frame_for(s) + delay
    if f0 <= 1:
        ob.color[3] = 1.0
        return
    ob.scale = (0, 0, 0); key(ob, "scale", f0 - 7)     # not there until it is installed
    ob.scale = (1, 1, 1); key(ob, "scale", f0 - 6)
    ob.color[3] = 0.0; key(ob, "color", f0)
    ob.color[3] = 1.0; key(ob, "color", f0 + 5)


def practical(name, loc, s, delay, watts, color, radius=0.12):
    """Real light source; reflections on the wet road can only appear once this is on."""
    ld = bpy.data.lights.new(name, "POINT")
    ld.color, ld.shadow_soft_size = color, radius
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    f0 = frame_for(s) + delay
    if f0 <= 1:
        ld.energy = watts
    else:
        ld.energy = 0.0; ld.keyframe_insert("energy", frame=round(f0))
        ld.energy = watts; ld.keyframe_insert("energy", frame=round(f0 + 5))
    return ob


# ---------------------------------------------------------------- bike proxy
def build_wheel(M, rig, y, with_disc):
    """Wheel that spins about its axle. Tyre ~0.30 m outer radius, cyan cast rim, 5 twin spokes."""
    spin = link(bpy.data.objects.new("wheel_spin", None))
    spin.parent, spin.location = rig, (0, y, WHEEL_R)
    side = (0, math.pi / 2, 0)       # turn Z-axis primitives so their axis is the axle (X)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.248, minor_radius=0.052,
                                     major_segments=48, minor_segments=14, rotation=side)
    parts = [op_object(M["tyre"])]
    bpy.ops.mesh.primitive_torus_add(major_radius=0.205, minor_radius=0.017,
                                     major_segments=48, minor_segments=10, rotation=side)
    parts.append(op_object(M["rim_cyan"]))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.214, depth=0.060, vertices=48, rotation=side)
    barrel = op_object(M["rim_cyan"])
    barrel.scale = (1, 1, 1)
    parts.append(barrel)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.200, depth=0.064, vertices=48, rotation=side)
    parts.append(op_object(M["tyre"]))           # dark well so the rim reads as a ring
    bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.11, vertices=24, rotation=side)
    parts.append(op_object(M["rim_cyan"]))       # hub
    spokes = []
    for k in range(5):
        for off in (-10, 10):
            ang = math.radians(k * 72 + off)
            spokes.append(Matrix.Rotation(ang, 4, "X") @ Matrix.Translation((0, 0, 0.122))
                          @ Matrix.Diagonal((0.070, 0.016, 0.165, 1)))
    parts.append(matrix_object("spokes", spokes, M["rim_cyan"]))
    if with_disc:                     # brake disc and ABS ring sit on the bike's right side
        bpy.ops.mesh.primitive_cylinder_add(radius=0.141, depth=0.005, vertices=48, rotation=side,
                                            location=(0.050, 0, 0))
        parts.append(op_object(M["disc"]))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.072, depth=0.004, vertices=40, rotation=side,
                                            location=(0.058, 0, 0))
        parts.append(op_object(M["disc"]))
    for p in parts:
        loc = tuple(p.location)
        p.parent = spin
        p.location = loc
    for f in range(1, NFRAMES + 1):   # roll forward without slipping
        spin.rotation_euler = (-(s_bike(f) - S0) / WHEEL_R, 0, 0)
        key(spin, "rotation_euler", f)
    return spin


def build_bike(M):
    rig = link(bpy.data.objects.new("bike_rig", None))
    FRONT_Y, REAR_Y, RAKE = 0.66, -0.66, math.radians(26)
    build_wheel(M, rig, FRONT_Y, with_disc=True)
    build_wheel(M, rig, REAR_Y, with_disc=False)

    # upside-down fork: thick gold upper tubes, slim bright sliders down to the axle
    for x in (-0.085, 0.085):
        for mat, radius, lo, hi in ((M["chrome"], 0.0185, 0.00, 0.30), (M["fork_gold"], 0.027, 0.26, 0.78)):
            mid, length = (lo + hi) / 2, hi - lo
            bpy.ops.mesh.primitive_cylinder_add(
                radius=radius, depth=length, vertices=20, rotation=(RAKE, 0, 0),
                location=(x, FRONT_Y - mid * math.sin(RAKE), WHEEL_R + mid * math.cos(RAKE)))
            tube = op_object(mat)
            loc = tuple(tube.location)
            tube.parent = rig
            tube.location = loc
        clamp = mesh_object("axle_clamp", [((x, FRONT_Y, WHEEL_R), (0.05, 0.07, 0.09))], M["proxy"])
        clamp.parent = rig

    # short front fender hugging the tyre
    arc = []
    for deg in range(28, 150, 9):
        a = math.radians(deg)
        arc.append(Matrix.Translation((0, FRONT_Y, WHEEL_R)) @ Matrix.Rotation(a, 4, "X")
                   @ Matrix.Translation((0, 0.335, 0)) @ Matrix.Diagonal((0.135, 0.012, 0.058, 1)))
    fender = matrix_object("front_fender", arc, M["fender"])
    fender.parent = rig

    body = mesh_object("proxy_bike", [
        ((0, -0.10, 0.62), (0.26, 0.70, 0.34)),     # frame / engine block (kept clear of the fork)
        ((0, 0.10, 0.92), (0.34, 0.44, 0.20)),      # tank
        ((0, -0.38, 0.84), (0.26, 0.60, 0.10)),     # seat
        ((0, 0.40, 1.05), (0.70, 0.06, 0.06)),      # handlebar
        ((0, 0.46, 0.96), (0.24, 0.16, 0.14)),      # headlamp housing
        ((0, -0.20, 1.22), (0.42, 0.34, 0.66)),     # rider torso
        ((0, 0.02, 1.66), (0.26, 0.30, 0.28)),      # helmet
        ((0.17, -0.15, 0.62), (0.14, 0.50, 0.14)),  # legs
        ((-0.17, -0.15, 0.62), (0.14, 0.50, 0.14)),
    ], M["proxy"])
    body.parent = rig
    lamp_face = mesh_object("proxy_headlamp", [((0, 0.545, 0.96), (0.16, 0.02, 0.08))], M["headlamp"])
    lamp_face.parent = rig

    hl = bpy.data.lights.new("headlight", "SPOT")
    hl.energy, hl.spot_size, hl.spot_blend, hl.color = 11000, math.radians(84), 0.30, (0.85, 0.93, 1)
    hl.shadow_soft_size = 0.05
    hl_ob = link(bpy.data.objects.new("headlight", hl))
    hl_ob.location = (0, 0.58, 0.96)
    # spot shines down local -Z; tilt so the centre of the beam lands FRONT metres ahead
    hl_ob.rotation_euler = (math.radians(90) - math.atan2(0.96, FRONT), 0, 0)
    hl_ob.parent = rig

    # soft fill on the waterside of the front wheel so the cyan rim and gold fork read at dusk
    # (a lighting cheat, the same thing a film crew would do with a small panel)
    fl = bpy.data.lights.new("wheel_fill", "AREA")
    fl.energy, fl.size, fl.color = 22, 0.6, (1.0, 0.92, 0.85)
    fl_ob = link(bpy.data.objects.new("wheel_fill", fl))
    fl_ob.location = (-1.1, 0.75, 0.65)
    fl_ob.rotation_euler = (0, math.radians(-78), 0)      # faces +X, toward the wheel
    fl_ob.parent = rig
    fl_ob.visible_glossy = False      # lights the wheel, but must not show up in the wet road

    for f in range(1, NFRAMES + 1):
        sb = s_bike(f)
        rig.location, rig.rotation_euler = route(sb, BIKE_LAT), (0, 0, heading(sb))
        key(rig, "location", f)
        key(rig, "rotation_euler", f)
    return rig


# ---------------------------------------------------------------- scene
def build_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, NFRAMES, FPS
    M = make_materials()

    # dusk sky: violet zenith to coral horizon, kept dim so practicals and the beam read
    w = bpy.data.worlds.new("dusk")
    w.use_nodes = True
    nt = w.node_tree
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.0
    cr.color_ramp.elements[0].color = (0.75, 0.30, 0.22, 1)
    cr.color_ramp.elements[1].position = 0.35
    cr.color_ramp.elements[1].color = (0.10, 0.06, 0.22, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], nt.nodes["Background"].inputs["Color"])
    nt.nodes["Background"].inputs["Strength"].default_value = 0.22
    sc.world = w

    # ground: wet road, clay promenade then water (left), clay ground for the town (right)
    strip("road", -HALF_ROAD, HALF_ROAD, 0.0, M["wet_road"])
    strip("ground_built", BUILT * HALF_ROAD, BUILT * 60.0, 0.0, M["clay"], step=2.0)
    strip("promenade", WATER * HALF_ROAD, WATER * 4.9, 0.0, M["clay"])
    strip("bank", WATER * 4.9, WATER * 4.9001, -0.3, M["clay"])
    bpy.ops.mesh.primitive_plane_add(size=1400, location=(0, 0, -0.6))
    bpy.context.object.data.materials.append(M["water"])

    # static guides: empty kerb slots and lane dashes (these exist before anything is built)
    s = S_MIN + 1
    while s < S_MAX - 1:
        for lat in (HALF_ROAD + 0.16, -HALF_ROAD - 0.16):
            mesh_object("slot", [((0, 0, 0.004), (0.46, 0.92, 0.004))], M["slot"],
                        route(s, lat), heading(s))
        if int(s) % 4 == 0:
            mesh_object("dash", [((0, 0, 0.003), (0.12, 1.6, 0.003))], M["paint"],
                        route(s, 0.0), heading(s))
        s += 1.0

    # --- kerb stones: one per metre, both sides
    s = S_MIN + 1
    while s < S_MAX - 1:
        for lat in (HALF_ROAD + 0.16, -HALF_ROAD - 0.16):
            ob = mesh_object("curb", [((0, 0, 0.13), (0.42, 0.94, 0.26))], M["module"],
                             route(s, lat), heading(s))
            ob.color = (0.62, 0.60, 0.55, 0)
            seat(ob, s)
        s += 1.0

    # --- waterside railing: posts every 2 m, rails follow one beat later
    s = S_MIN + 1
    while s < S_MAX - 2:
        post = mesh_object("rail_post", [((0, 0, 0.55), (0.16, 0.16, 1.1))], M["module"],
                           route(s, WATER * 4.5), heading(s))
        post.color = (0.50, 0.49, 0.46, 0)
        seat(post, s, delay=3, grow=True)
        rail = mesh_object("rail", [((0, 1.0, 0.95), (0.06, 1.86, 0.06)),
                                    ((0, 1.0, 0.55), (0.06, 1.86, 0.06))], M["module"],
                           route(s, WATER * 4.5), heading(s + 1.0))
        rail.color = (0.16, 0.17, 0.19, 0)
        seat(rail, s + 2.0, delay=6, drop=0.35)
        s += 2.0

    # --- street lamps (town-side kerb): pole rises, THEN the light comes on
    s = -8.0
    while s < S_MAX - 4:
        # local +X is the right of travel; the arm reaches over the road
        pole = mesh_object("lamp_pole", [((0, 0, 2.6), (0.10, 0.10, 5.2)),
                                         ((BUILT * 0.7, 0, 5.15), (1.5, 0.08, 0.08))], M["module"],
                           route(s, BUILT * (HALF_ROAD + 0.7)), heading(s))
        pole.color = (0.12, 0.13, 0.15, 0)
        seat(pole, s, delay=4, grow=True)
        head_lat = BUILT * (HALF_ROAD - 0.75)
        head = mesh_object("lamp_head", [((0, 0, 0), (0.5, 0.22, 0.08))], M["emit"],
                           route(s, head_lat, 5.08), heading(s))
        head.color = (1.0, 0.62, 0.28, 0)
        glow(head, s, delay=16)
        practical("lamp_light", route(s, head_lat, 4.9), s, 16, 900, (1.0, 0.62, 0.30), 0.2)
        s += 12.0

    # --- buildings (town side): grey clay masses exist first; facade, shutter, windows arrive
    palette = [(0.62, 0.42, 0.26), (0.30, 0.42, 0.46), (0.66, 0.50, 0.34), (0.44, 0.30, 0.34)]
    FACE = 6.4                      # distance of the facades from the road centre
    s, i = -9.0, 0
    while s < S_MAX - 6:
        width, depth, height = 8.2, 8.0, random.choice((7.0, 9.5, 12.0, 15.0))
        mass = mesh_object("bldg", [((0, 0, height / 2), (depth, width, height))], M["module"],
                           route(s, BUILT * (FACE + depth / 2)), heading(s))
        mass.color = (*palette[i % 4], 0)
        f = frame_for(s) + 4
        if f <= 1:
            mass.color[3] = 1
        else:
            mass.color[3] = 0; key(mass, "color", f)
            mass.color[3] = 1; key(mass, "color", f + 10)
        face = route(s, BUILT * (FACE - 0.06))
        shutter = mesh_object("shutter", [((0, 0, 1.4), (0.10, 4.6, 2.8))], M["module"],
                              face, heading(s))
        shutter.color = (0.20, 0.22, 0.24, 0)
        seat(shutter, s, delay=6, drop=1.2)
        wins = []
        for floor in range(1, int(height // 3)):
            for col in (-2.6, 0.0, 2.6):
                if random.random() < 0.7:
                    wins.append(((0, col, 1.6 + floor * 3.0), (0.08, 1.3, 1.5)))
        if wins:
            w_ob = mesh_object("windows", wins, M["emit"], face, heading(s))
            w_ob.color = (*random.choice(((1.0, 0.70, 0.36), (0.75, 0.85, 1.0))), 0)
            glow(w_ob, s, delay=18)
        if i % 3 == 1:        # cyan sign over the shutter
            sign = mesh_object("neon_cyan", [((0, 0, 3.25), (0.08, 3.8, 0.16))], M["neon"],
                               route(s, BUILT * (FACE - 0.16)), heading(s))
            sign.color = (0.0, 0.85, 1.0, 0)
            glow(sign, s, delay=20)
            practical("neon_cyan_light", route(s, BUILT * 5.6, 3.2), s, 20, 260, (0.0, 0.85, 1.0), 0.6)
        if i % 3 == 2:        # magenta vertical sign
            sign = mesh_object("neon_magenta", [((0, 3.6, 5.5), (0.10, 0.16, 4.2))], M["neon"],
                               route(s, BUILT * (FACE - 0.18)), heading(s))
            sign.color = (1.0, 0.05, 0.65, 0)
            glow(sign, s, delay=22)
            practical("neon_magenta_light", route(s + 3.6, BUILT * 5.6, 5.5), s, 22, 260,
                      (1.0, 0.05, 0.65), 0.6)
        s, i = s + 9.0, i + 1

    # --- tea stall on the town-side pavement: posts -> roof -> counter -> stools -> bulb
    ST = 36.0
    for n, (dy, dl) in enumerate(((-1.4, 4.2), (1.4, 4.2), (-1.4, 5.9), (1.4, 5.9))):
        p = mesh_object("stall_post", [((0, 0, 1.15), (0.09, 0.09, 2.3))], M["module"],
                        route(ST + dy, BUILT * dl), heading(ST))
        p.color = (0.30, 0.20, 0.12, 0)
        seat(p, ST, delay=n * 2, grow=True)
    roof = mesh_object("stall_roof", [((0, 0, 2.36), (2.3, 3.3, 0.10))], M["module"],
                       route(ST, BUILT * 5.05), heading(ST))
    roof.color = (0.10, 0.22, 0.50, 0)
    seat(roof, ST, delay=10, drop=0.9)
    counter = mesh_object("stall_counter", [((0, 0, 0.5), (0.6, 2.6, 1.0))], M["module"],
                          route(ST, BUILT * 5.3), heading(ST))
    counter.color = (0.36, 0.24, 0.14, 0)
    seat(counter, ST, delay=13, drop=0.5)
    for n, dy in enumerate((-0.9, 0.0, 0.9)):
        st = mesh_object("stool", [((0, 0, 0.22), (0.30, 0.30, 0.44))], M["module"],
                         route(ST + dy, BUILT * 4.45), heading(ST))
        st.color = (0.70, 0.08, 0.06, 0)
        seat(st, ST, delay=16 + n * 2, drop=0.4)
    bulb = mesh_object("stall_bulb", [((0, 0, 0), (0.10, 0.10, 0.10))], M["emit"],
                       route(ST, BUILT * 5.0, 2.1), heading(ST))
    bulb.color = (1.0, 0.72, 0.36, 0)
    glow(bulb, ST, delay=24)
    practical("stall_light", route(ST, BUILT * 5.0, 2.0), ST, 24, 220, (1.0, 0.72, 0.36), 0.08)

    # --- far shore across the water stays unbuilt grey clay
    for n in range(30):
        s_far = -60 + n * 9.0
        h = 8 + random.random() * 30
        mesh_object("far_clay", [((0, 0, h / 2 - 0.6), (14, 14, h))], M["clay"],
                    route(s_far, WATER * (150 + random.random() * 70)), random.random())

    build_bike(M)

    # --- cameras: same world, same direction of travel, water always on the left
    def camera(name, lens):
        cd = bpy.data.cameras.new(name)
        cd.lens, cd.sensor_width, cd.clip_start, cd.clip_end = lens, 36, 0.05, 2000
        ob = link(bpy.data.objects.new(name, cd))
        tgt = link(bpy.data.objects.new(name + "_target", None))
        con = ob.constraints.new("TRACK_TO")
        con.target, con.track_axis, con.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
        return ob, tgt

    cam_h, tgt_h = camera("H", 18)      # hero: low beside the front wheel, looking along the beam
    cam_b, tgt_b = camera("B", 35)      # aerial
    cam_c, tgt_c = camera("C", 24)      # rear chase
    cam_d, tgt_d = camera("D", 20)      # kerb-side diagnostic, no bike in frame
    for f in range(1, NFRAMES + 1):
        sb = s_bike(f)
        # H sits between the bike and the waterside kerb, just behind the front axle.
        # Wheel and fork fill the right edge; slots, seating stones and rail posts are ahead-left.
        cam_h.location = route(sb - 0.40, BIKE_LAT + WATER * 0.52, 0.30)
        tgt_h.location = route(sb + 6.5, BIKE_LAT + WATER * 0.70, -0.45)
        # B looks down the route from behind: built strip at the bottom, grey road at the top
        cam_b.location = route(sb - 24.0, 0.0, 28.0)
        tgt_b.location = route(sb + 6.0, 0.0, 0.0)
        # C chases from behind in the bike's lane
        cam_c.location = route(sb - 8.0, BIKE_LAT + BUILT * 0.9, 1.7)
        tgt_c.location = route(sb + 10.0, WATER * 0.6, 0.9)
        cam_d.location = route(sb + 0.5, WATER * 2.5, 0.45)
        tgt_d.location = route(sb + 8.0, WATER * 4.4, 0.50)
        for ob in (cam_h, tgt_h, cam_b, tgt_b, cam_c, tgt_c, cam_d, tgt_d):
            key(ob, "location", f)
    return sc


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--cam", default="H")
    ap.add_argument("--frames", default="30-101")
    ap.add_argument("--out", default="renders/H")
    ap.add_argument("--samples", type=int, default=14)
    ap.add_argument("--scale", type=int, default=100)
    ap.add_argument("--mblur", action="store_true", help="motion blur (spinning spokes need it)")
    ap.add_argument("--blend", default="")
    a = ap.parse_args(argv)

    sc = build_scene()
    sc.camera = bpy.data.objects[a.cam]
    r = sc.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = 540, 960, a.scale
    r.image_settings.file_format = "PNG"
    r.use_persistent_data = True
    r.use_motion_blur = a.mblur
    r.motion_blur_shutter = 0.5
    cy = sc.cycles
    cy.samples, cy.use_denoising, cy.use_adaptive_sampling = a.samples, True, True
    cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = 4, 2, 3
    cy.caustics_reflective = cy.caustics_refractive = False
    sc.view_settings.exposure = 0.6
    if a.blend:
        bpy.ops.wm.save_as_mainfile(filepath=a.blend)
    frames = []
    for part in a.frames.split(","):
        lo, _, hi = part.partition("-")
        frames += range(int(lo), int(hi or lo) + 1)
    for f in frames:
        sc.frame_set(f)
        r.filepath = f"{a.out}/f{f:04d}.png"
        bpy.ops.render.render(write_still=True)
        print(f"FRAME_DONE {a.cam} {f}", flush=True)


if __name__ == "__main__":
    main()
