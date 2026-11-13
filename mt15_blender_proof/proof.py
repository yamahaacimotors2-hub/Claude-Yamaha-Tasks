"""MT-15 "Map loads under the wheel" - 5s construction-beat proof (Blender 5.x / bpy, Cycles CPU).

Usage:  python3 proof.py --cam A --frames 1-120 --out renders/A [--samples 32] [--blend scene.blend]
        blender -b -P proof.py -- --cam A --frames 1-120 --out renders/A

One lakeside bend. A simple UNBRANDED proxy bike rides the route. Every module (curb stone,
rail post, lamp, stall part, facade) stores its distance `s` along the route and is activated
when the headlight contact point (s_bike + FRONT) reaches it:
    seat (drops into its slot) -> material (clay -> final) -> practical light on.
The bike only moves forward, so everything behind it stays built.
"""
import argparse
import math
import random
import sys

import bpy
import bmesh  # must come after bpy when using the pip module

# ---------------------------------------------------------------- parameters
FPS, NFRAMES = 24, 120
R = 70.0            # bend radius (m); the lake is inside the bend, on the rider's right
SPEED = 8.0         # m/s (~29 km/h, normal riding speed)
S0 = 6.0            # bike start distance along route
FRONT = 6.0         # headlight contact point, metres ahead of the bike
HALF_ROAD = 3.5
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
    return -s / R       # rotation_z that points local +Y along the route


# ---------------------------------------------------------------- helpers
def principled(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m, m.node_tree, m.node_tree.nodes["Principled BSDF"]


def make_materials():
    mats = {}
    CLAY = (0.20, 0.22, 0.27, 1)

    m, nt, b = principled("clay")
    b.inputs["Base Color"].default_value = CLAY
    b.inputs["Roughness"].default_value = 0.9
    mats["clay"] = m

    # module: clay until activated; object colour = final colour, object alpha = activation
    m, nt, b = principled("module")
    info = nt.nodes.new("ShaderNodeObjectInfo")
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = CLAY
    nt.links.new(info.outputs["Alpha"], mix.inputs["Factor"])
    nt.links.new(info.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.6
    mats["module"] = m

    # emitter: dark until activated, then glows in the object colour
    for name, strength in (("emit", 2.2), ("neon", 30.0)):
        m, nt, b = principled(name)
        info = nt.nodes.new("ShaderNodeObjectInfo")
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.inputs[1].default_value = strength
        nt.links.new(info.outputs["Alpha"], mul.inputs[0])
        nt.links.new(info.outputs["Color"], b.inputs["Emission Color"])
        nt.links.new(mul.outputs[0], b.inputs["Emission Strength"])
        b.inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1)
        mats[name] = m

    # wet asphalt: real glossy surface, puddles from a noise-driven roughness
    m, nt, b = principled("wet_road")
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
    b.inputs["Base Color"].default_value = (0.018, 0.018, 0.022, 1)
    mats["wet_road"] = m

    m, nt, b = principled("water")
    b.inputs["Base Color"].default_value = (0.01, 0.012, 0.02, 1)
    b.inputs["Roughness"].default_value = 0.03
    mats["water"] = m

    m, nt, b = principled("slot")
    b.inputs["Base Color"].default_value = (0.004, 0.004, 0.005, 1)
    b.inputs["Roughness"].default_value = 1.0
    mats["slot"] = m

    m, nt, b = principled("paint")
    b.inputs["Base Color"].default_value = (0.55, 0.55, 0.5, 1)
    b.inputs["Roughness"].default_value = 0.5
    mats["paint"] = m

    m, nt, b = principled("proxy")       # unbranded graphite placeholder
    b.inputs["Base Color"].default_value = (0.05, 0.055, 0.06, 1)
    b.inputs["Roughness"].default_value = 0.35
    mats["proxy"] = m

    m, nt, b = principled("headlamp")
    b.inputs["Emission Color"].default_value = (0.85, 0.93, 1, 1)
    b.inputs["Emission Strength"].default_value = 60
    mats["headlamp"] = m
    return mats


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
    bpy.context.scene.collection.objects.link(ob)
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
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def key(ob, path, frame):
    ob.keyframe_insert(data_path=path, frame=round(frame))


def seat(ob, s, delay=0.0, drop=0.7, grow=False):
    """Physically seat a module when the build front reaches s. Returns the frame it lands."""
    f0 = frame_for(s) + delay
    if f0 <= 1:                       # already built behind the bike at the start
        ob.color[3] = 1.0
        return 1
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
    return f0 + 10


def glow(ob, s, delay):
    """Emitter that switches on `delay` frames after the front reaches s."""
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
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    bpy.context.scene.collection.objects.link(ob)
    f0 = frame_for(s) + delay
    if f0 <= 1:
        ld.energy = watts
    else:
        ld.energy = 0.0; ld.keyframe_insert("energy", frame=round(f0))
        ld.energy = watts; ld.keyframe_insert("energy", frame=round(f0 + 5))
    return ob


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

    # ground: wet road, clay sidewalk (left), clay promenade (right), lake inside the bend
    strip("road", -HALF_ROAD, HALF_ROAD, 0.0, M["wet_road"])
    strip("ground_left", HALF_ROAD, 60.0, 0.0, M["clay"], step=2.0)
    strip("promenade", -4.9, -HALF_ROAD, 0.0, M["clay"])
    strip("bank", -4.9, -4.9001, -0.3, M["clay"])
    bpy.ops.mesh.primitive_plane_add(size=900, location=(0, 0, -0.6))
    bpy.context.object.data.materials.append(M["water"])

    # static guides: empty curb slots and lane dashes (these exist before anything is built)
    slots, dashes = [], []
    s = S_MIN + 1
    while s < S_MAX - 1:
        for lat in (HALF_ROAD + 0.16, -HALF_ROAD - 0.16):
            ob = mesh_object("slot", [((0, 0, 0.004), (0.46, 0.92, 0.004))], M["slot"],
                             route(s, lat), heading(s))
            slots.append(ob)
        if int(s) % 4 == 0:
            dashes.append(mesh_object("dash", [((0, 0, 0.003), (0.12, 1.6, 0.003))], M["paint"],
                                      route(s, 0.0), heading(s)))
        s += 1.0

    # --- curb stones: one per metre, both sides
    s = S_MIN + 1
    while s < S_MAX - 1:
        for lat in (HALF_ROAD + 0.16, -HALF_ROAD - 0.16):
            ob = mesh_object("curb", [((0, 0, 0.13), (0.42, 0.94, 0.26))], M["module"],
                             route(s, lat), heading(s))
            ob.color = (0.62, 0.60, 0.55, 0)
            seat(ob, s)
        s += 1.0

    # --- lakeside railing (rider's right): posts every 2 m, rails follow one beat later
    s = S_MIN + 1
    while s < S_MAX - 2:
        post = mesh_object("rail_post", [((0, 0, 0.55), (0.16, 0.16, 1.1))], M["module"],
                           route(s, -4.5), heading(s))
        post.color = (0.50, 0.49, 0.46, 0)
        seat(post, s, delay=3, grow=True)
        rail = mesh_object("rail", [((0, 1.0, 0.95), (0.06, 1.86, 0.06)),
                                    ((0, 1.0, 0.55), (0.06, 1.86, 0.06))], M["module"],
                           route(s, -4.5), heading(s + 1.0))
        rail.color = (0.16, 0.17, 0.19, 0)
        seat(rail, s + 2.0, delay=6, drop=0.35)
        s += 2.0

    # --- street lamps (left kerb): pole rises, head seats, THEN the light comes on
    s = -8.0
    while s < S_MAX - 4:
        pole = mesh_object("lamp_pole", [((0, 0, 2.6), (0.10, 0.10, 5.2)),
                                         ((-0.7, 0, 5.15), (1.5, 0.08, 0.08))], M["module"],
                           route(s, HALF_ROAD + 0.7), heading(s))
        pole.color = (0.12, 0.13, 0.15, 0)
        seat(pole, s, delay=4, grow=True)
        head = mesh_object("lamp_head", [((0, 0, 0), (0.5, 0.22, 0.08))], M["emit"],
                           route(s, HALF_ROAD - 0.75, 5.08), heading(s))
        head.color = (1.0, 0.62, 0.28, 0)
        glow(head, s, delay=16)
        practical("lamp_light", route(s, HALF_ROAD - 0.75, 4.9), s, 16, 900, (1.0, 0.62, 0.30), 0.2)
        s += 12.0

    # --- buildings (left): grey clay masses exist first; facade, shutter and windows arrive
    palette = [(0.62, 0.42, 0.26), (0.30, 0.42, 0.46), (0.66, 0.50, 0.34), (0.44, 0.30, 0.34)]
    s, i = -9.0, 0
    while s < S_MAX - 6:
        width, depth, height = 8.2, 8.0, random.choice((7.0, 9.5, 12.0, 15.0))
        lat = 6.4 + depth / 2
        mass = mesh_object("bldg", [((0, 0, height / 2), (depth, width, height))], M["module"],
                           route(s, lat), heading(s))
        mass.color = (*palette[i % 4], 0)
        f = frame_for(s) + 4
        if f <= 1:
            mass.color[3] = 1
        else:
            mass.color[3] = 0; key(mass, "color", f)
            mass.color[3] = 1; key(mass, "color", f + 10)
        face = route(s, 6.4 - 0.06)
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
                               route(s, 6.4 - 0.16), heading(s))
            sign.color = (0.0, 0.85, 1.0, 0)
            glow(sign, s, delay=20)
            practical("neon_cyan_light", route(s, 5.6, 3.2), s, 20, 260, (0.0, 0.85, 1.0), 0.6)
        if i % 3 == 2:        # magenta vertical sign
            sign = mesh_object("neon_magenta", [((0, 3.6, 5.5), (0.10, 0.16, 4.2))], M["neon"],
                               route(s, 6.4 - 0.18), heading(s))
            sign.color = (1.0, 0.05, 0.65, 0)
            glow(sign, s, delay=22)
            practical("neon_magenta_light", route(s + 3.6, 5.6, 5.5), s, 22, 260, (1.0, 0.05, 0.65), 0.6)
        s, i = s + 9.0, i + 1

    # --- tea stall on the left sidewalk: posts -> roof -> counter -> stools -> bulb
    ST = 36.0
    for n, (dy, dl) in enumerate(((-1.4, 4.2), (1.4, 4.2), (-1.4, 5.9), (1.4, 5.9))):
        p = mesh_object("stall_post", [((0, 0, 1.15), (0.09, 0.09, 2.3))], M["module"],
                        route(ST + dy, dl), heading(ST))
        p.color = (0.30, 0.20, 0.12, 0)
        seat(p, ST, delay=n * 2, grow=True)
    roof = mesh_object("stall_roof", [((0, 0, 2.36), (2.3, 3.3, 0.10))], M["module"],
                       route(ST, 5.05), heading(ST))
    roof.color = (0.10, 0.22, 0.50, 0)
    seat(roof, ST, delay=10, drop=0.9)
    counter = mesh_object("stall_counter", [((0, 0, 0.5), (0.6, 2.6, 1.0))], M["module"],
                          route(ST, 5.3), heading(ST))
    counter.color = (0.36, 0.24, 0.14, 0)
    seat(counter, ST, delay=13, drop=0.5)
    for n, dy in enumerate((-0.9, 0.0, 0.9)):
        st = mesh_object("stool", [((0, 0, 0.22), (0.30, 0.30, 0.44))], M["module"],
                         route(ST + dy, 4.45), heading(ST))
        st.color = (0.70, 0.08, 0.06, 0)
        seat(st, ST, delay=16 + n * 2, drop=0.4)
    bulb = mesh_object("stall_bulb", [((0, 0, 0), (0.10, 0.10, 0.10))], M["emit"],
                       route(ST, 5.0, 2.1), heading(ST))
    bulb.color = (1.0, 0.72, 0.36, 0)
    glow(bulb, ST, delay=24)
    practical("stall_light", route(ST, 5.0, 2.0), ST, 24, 220, (1.0, 0.72, 0.36), 0.08)

    # --- far shore stays unbuilt grey clay
    for n in range(26):
        a = math.radians(-35 + n * 5.5)
        d = 190 + random.random() * 60
        h = 8 + random.random() * 30
        mesh_object("far_clay", [((0, 0, h / 2 - 0.6), (14, 14, h))], M["clay"],
                    (R + d * math.sin(a) * 0.9, 40 + d * math.cos(a), 0), random.random())

    # --- unbranded proxy bike + rider (placeholder for the validated product asset)
    rig = bpy.data.objects.new("bike_rig", None)
    sc.collection.objects.link(rig)
    body = mesh_object("proxy_bike", [
        ((0, 0.05, 0.62), (0.26, 1.05, 0.34)),      # frame / engine block
        ((0, 0.28, 0.90), (0.34, 0.50, 0.22)),      # tank
        ((0, -0.38, 0.84), (0.26, 0.60, 0.10)),     # seat
        ((0, 0.66, 0.30), (0.12, 0.60, 0.60)),      # front wheel (boxy stand-in)
        ((0, -0.66, 0.30), (0.14, 0.60, 0.60)),     # rear wheel
        ((0, 0.62, 0.72), (0.10, 0.12, 0.70)),      # fork
        ((0, 0.52, 1.05), (0.70, 0.06, 0.06)),      # handlebar
        ((0, -0.20, 1.22), (0.42, 0.34, 0.66)),     # rider torso
        ((0, 0.02, 1.66), (0.26, 0.30, 0.28)),      # helmet
        ((0.17, -0.15, 0.62), (0.14, 0.50, 0.14)),  # legs
        ((-0.17, -0.15, 0.62), (0.14, 0.50, 0.14)),
    ], M["proxy"])
    body.parent = rig
    lamp_face = mesh_object("proxy_headlamp", [((0, 0.80, 0.98), (0.16, 0.03, 0.09))], M["headlamp"])
    lamp_face.parent = rig
    hl = bpy.data.lights.new("headlight", "SPOT")
    hl.energy, hl.spot_size, hl.spot_blend, hl.color = 26000, math.radians(84), 0.30, (0.85, 0.93, 1)
    hl.shadow_soft_size = 0.05
    hl_ob = bpy.data.objects.new("headlight", hl)
    hl_ob.location = (0, 0.84, 0.98)
    # spot shines down local -Z; tilt so the centre of the beam lands FRONT metres ahead
    hl_ob.rotation_euler = (math.radians(90) - math.atan2(0.98, FRONT), 0, 0)
    hl_ob.parent = rig
    sc.collection.objects.link(hl_ob)
    for f in range(1, NFRAMES + 1):
        sb = s_bike(f)
        rig.location, rig.rotation_euler = route(sb), (0, 0, heading(sb))
        key(rig, "location", f)
        key(rig, "rotation_euler", f)

    # --- cameras: same world, same direction of travel, lake always on the rider's right
    def camera(name, lens):
        cd = bpy.data.cameras.new(name)
        cd.lens, cd.sensor_width, cd.clip_end = lens, 36, 2000
        ob = bpy.data.objects.new(name, cd)
        sc.collection.objects.link(ob)
        tgt = bpy.data.objects.new(name + "_target", None)
        sc.collection.objects.link(tgt)
        con = ob.constraints.new("TRACK_TO")
        con.target, con.track_axis, con.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
        return ob, tgt

    cam_a, tgt_a = camera("A", 18)      # low tracking shot: the build front holds one screen position
    cam_b, tgt_b = camera("B", 35)      # aerial
    cam_c, tgt_c = camera("C", 24)
    cam_d, tgt_d = camera("D", 20)      # low kerb-side view WITH the beam: stones seat lit by the headlight      # rear chase
    for f in range(1, NFRAMES + 1):
        t, sb = (f - 1) / FPS, s_bike(f)
        u = (f - 1) / (NFRAMES - 1)
        # A rides just inside the lakeside kerb, 10 m -> 9 m ahead of the bike, looking back at it.
        # Empty slots slide away from the lens and get filled where the beam lands.
        cam_a.location = route(sb + 10.0 - 1.0 * u, -3.3, 0.45 + 0.35 * u)
        tgt_a.location = route(sb + 3.5, -2.9, 0.85)
        # B looks down the route from behind: built strip at the bottom, grey road at the top
        cam_b.location = route(sb - 24.0, 2.0, 28.0)
        tgt_b.location = route(sb + 6.0, 0.0, 0.0)
        # C chases from behind; lake stays on the right, stall and buildings on the left
        cam_c.location = route(sb - 8.0, 0.8, 1.7)
        tgt_c.location = route(sb + 10.0, -0.5, 0.9)
        cam_d.location = route(sb + 0.5, -2.5, 0.45)
        tgt_d.location = route(sb + 8.0, -4.4, 0.50)
        for ob in (cam_a, tgt_a, cam_b, tgt_b, cam_c, tgt_c, cam_d, tgt_d):
            key(ob, "location", f)
    return sc


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--cam", default="A")
    ap.add_argument("--frames", default="1-120")
    ap.add_argument("--out", default="renders/A")
    ap.add_argument("--samples", type=int, default=32)
    ap.add_argument("--scale", type=int, default=100)
    ap.add_argument("--blend", default="")
    a = ap.parse_args(argv)

    sc = build_scene()
    sc.camera = bpy.data.objects[a.cam]
    r = sc.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y, r.resolution_percentage = 540, 960, a.scale
    r.image_settings.file_format = "PNG"
    r.use_persistent_data = True
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
