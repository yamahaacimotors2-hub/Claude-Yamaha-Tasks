"""MT-15 "Map loads under the wheel" - all CG shots for the 16 s film, v1 (Blender 5.x / bpy, Cycles CPU).

Usage:  python3 film.py --shot S08 --out /path/frames/S08 [--frames 1-72] [--scale 100] [--tv named|clean]

Shots (frame counts follow MT15_Final_SOP_v2.md section 3):
  S01 room, TV 3%      S02 helmet            S03 visor snap       S04 rainy Dhaka wide
  S05 raindrop burst   S06 bike low 3/4      S07 puddle ripple    S08 hero wheel build
  S09 aerial           S10 chase             S11 room, TV 4%
  BG12 end-card background still             PREVIEW still used as the TV preview art

S01-S07, S10 and S11 are CG stand-ins for footage the SOP plans to generate later; S08 and S09
are the intended CG shots. The bike is an unbranded proxy except wheel, fork and fender.
Reuses the world helpers of ../../mt15_blender_proof/proof.py.
"""
import argparse
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "mt15_blender_proof"))

import bpy
import proof as P
from mathutils import Matrix, Vector
from proof import (BIKE_LAT, BUILT, FPS, HALF_ROAD, WATER, heading, key, link, matrix_object,
                   mesh_object, op_object, principled, route)

P.R = 160.0                       # gentler bend than the proof, the route is longer
P.S_MIN, P.S_MAX = 30.0, 204.0
STALL_S = 90.0                    # the tea stall: the one landmark that exists in both states
SPEED = 8.0
TEX = os.path.join(HERE, "textures")

SHOTS = {
    "S01": dict(n=30, set="room"),
    "S02": dict(n=20, set="room"),
    "S03": dict(n=12, set="room"),
    "S04": dict(n=34, set="road", sky="rain", s0=80.0, build="none", mblur=True, stall_w=45),
    "S05": dict(n=30, set="drop"),
    "S06": dict(n=24, set="road", sky="rain", s0=76.0, build="none", mblur=True),
    "S07": dict(n=14, set="puddle"),
    "S08": dict(n=72, set="road", sky="dusk", g0=0, build="timeline", mblur=True),
    "S09": dict(n=36, set="road", sky="dusk", g0=72, build="timeline"),
    "S10": dict(n=30, set="road", sky="dusk", g0=108, build="timeline", mblur=True),
    "S11": dict(n=40, set="room"),
    "BG12": dict(n=1, set="road", sky="dusk", build="all", bike=False, res=(1080, 1920), samples=64),
    "PREVIEW": dict(n=1, set="road", sky="dusk", build="all", bike=False, res=(640, 360), samples=48),
}

# ---------------------------------------------------------------- build timeline (S08 -> S09 -> S10)
BUILD_S0 = 84.0


def timeline_s(g):
    return BUILD_S0 + SPEED * (g - 1) / FPS


def timeline_front(g):
    """Headlight contact point. It runs 6 m ahead, then races ahead as the city opens up."""
    u = min(1.0, max(0.0, (g - 100) / 14.0))
    return timeline_s(g) + 6.0 + 54.0 * u * u * (3 - 2 * u)


def configure(shot):
    sh = SHOTS[shot]
    P.NFRAMES = sh["n"]
    mode, g0 = sh.get("build"), sh.get("g0", 0)
    if mode == "timeline":
        P.s_bike = lambda f: timeline_s(f + g0)
        fronts = [(g, timeline_front(g)) for g in range(-40, 220)]

        def frame_for(s):
            for (ga, fa), (gb, fb) in zip(fronts, fronts[1:]):
                if fb >= s:
                    if fa >= s:
                        return -1e6
                    return ga + (s - fa) / (fb - fa) - g0
            return 1e6
        P.frame_for = frame_for
    else:
        s0 = sh.get("s0", 100.0)
        P.s_bike = lambda f: s0 + SPEED * (f - 1) / FPS
        P.frame_for = (lambda s: -1e6) if mode == "all" else (lambda s: 1e6)
    P.S0 = P.s_bike(1)
    return sh


# ---------------------------------------------------------------- small helpers
def child(ob, parent):
    loc = tuple(ob.location)
    ob.parent = parent
    ob.location = loc
    return ob


def ell(loc, radii, mat, rot=(0, 0, 0), parent=None, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=seg, ring_count=seg // 2,
                                         location=loc, rotation=rot)
    ob = op_object(mat)
    ob.scale = radii
    return child(ob, parent) if parent else ob


def cyl_between(p1, p2, radius, mat, parent=None):
    a, b = Vector(p1), Vector(p2)
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=(b - a).length, vertices=16,
                                        location=(a + b) / 2)
    ob = op_object(mat)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = (b - a).to_track_quat("Z", "Y")
    return child(ob, parent) if parent else ob


def box(loc, size, mat, parent=None, rot_z=0.0, name="box"):
    ob = mesh_object(name, [((0, 0, 0), size)], mat, loc, rot_z)
    return child(ob, parent) if parent else ob


def emit_mat(name, strength):
    """Glows in the object colour, scaled by the object alpha (so it can be animated)."""
    m, nt, b = principled(name, (0.03, 0.03, 0.03), 0.25)
    info = nt.nodes.new("ShaderNodeObjectInfo")
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = strength
    nt.links.new(info.outputs["Alpha"], mul.inputs[0])
    nt.links.new(info.outputs["Color"], b.inputs["Emission Color"])
    nt.links.new(mul.outputs[0], b.inputs["Emission Strength"])
    nt.links.new(info.outputs["Color"], b.inputs["Base Color"])
    return m


def point(loc, watts, color, radius=0.1, parent=None):
    ld = bpy.data.lights.new("pt", "POINT")
    ld.energy, ld.color, ld.shadow_soft_size = watts, color, radius
    ob = link(bpy.data.objects.new("pt", ld))
    ob.location = loc
    return child(ob, parent) if parent else ob


def camera(name, lens, fstop=None):
    cd = bpy.data.cameras.new(name)
    cd.lens, cd.sensor_width, cd.clip_start, cd.clip_end = lens, 36, 0.03, 3000
    ob = link(bpy.data.objects.new(name, cd))
    tgt = link(bpy.data.objects.new(name + "_target", None))
    con = ob.constraints.new("TRACK_TO")
    con.target, con.track_axis, con.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
    if fstop:
        cd.dof.use_dof, cd.dof.focus_object, cd.dof.aperture_fstop = True, tgt, fstop
    return ob, tgt


def make_world(kind):
    w = bpy.data.worlds.new(kind)
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    if kind == "room":
        bg.inputs["Color"].default_value = (0.02, 0.03, 0.06, 1)
        bg.inputs["Strength"].default_value = 0.5
        return w
    horizon, zenith, strength = {
        "rain": ((0.22, 0.30, 0.38, 1), (0.03, 0.05, 0.09, 1), 0.40),
        "dusk": ((0.80, 0.32, 0.24, 1), (0.10, 0.06, 0.24, 1), 0.30),
    }[kind]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position, cr.color_ramp.elements[0].color = 0.0, horizon
    cr.color_ramp.elements[1].position, cr.color_ramp.elements[1].color = 0.38, zenith
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    return w


def extra_materials(M):
    M["graphite"] = principled("graphite", (0.10, 0.11, 0.12), 0.38, 0.5)[0]
    M["black"] = principled("black", (0.015, 0.015, 0.017), 0.5)[0]
    M["jacket"] = principled("jacket", (0.020, 0.021, 0.024), 0.7)[0]
    M["helmet"] = principled("helmet", (0.012, 0.012, 0.014), 0.16)[0]
    M["visor"] = principled("visor", (0.02, 0.03, 0.05), 0.03, 0.9)[0]
    M["liquid"] = emit_mat("liquid", 1.7)
    M["glow"] = emit_mat("glow", 3.0)
    m, nt, b = principled("glass", (1, 1, 1), 0.0)
    b.inputs["Transmission Weight"].default_value = 1.0
    b.inputs["IOR"].default_value = 1.33
    M["glass"] = m
    return M


# ---------------------------------------------------------------- helmet, bike body, rider
def build_helmet(M, loc=(0, 0, 0), rot_z=0.0, parent=None):
    """Full-face helmet. Front is local +Y. Returns (root, visor_pivot); rotate pivot.x to open."""
    root = link(bpy.data.objects.new("helmet", None))
    root.location, root.rotation_euler = loc, (0, 0, rot_z)
    if parent:
        child(root, parent)
    ell((0, 0, 0), (0.135, 0.150, 0.140), M["helmet"], parent=root)
    ell((0, 0.070, -0.070), (0.110, 0.090, 0.062), M["helmet"], parent=root)        # chin bar
    ell((0, 0.066, 0.018), (0.098, 0.088, 0.040), principled("eyeport", (0.30, 0.19, 0.13), 0.6)[0], parent=root)
    for ex in (-0.036, 0.036):
        ell((ex, 0.146, 0.022), (0.013, 0.009, 0.007), M["black"], parent=root, seg=10)
    pivot = link(bpy.data.objects.new("visor_pivot", None))
    pivot.location = (0, 0.0, 0.018)
    child(pivot, root)
    ell((0, 0.080, 0.0), (0.112, 0.082, 0.056), M["visor"], parent=pivot)
    return root, pivot


def build_body(M, rig):
    """Naked-bike silhouette and a rider in full gear. Deliberately generic: no logos, no decals."""
    for old in ("proxy_bike",):
        bpy.data.objects.remove(bpy.data.objects[old])
    box((0, -0.05, 0.50), (0.24, 0.56, 0.34), M["black"], rig)                    # engine
    box((0, -0.02, 0.33), (0.20, 0.50, 0.10), M["graphite"], rig)                 # belly pan
    ell((0, 0.13, 0.93), (0.185, 0.30, 0.135), M["graphite"], parent=rig)         # tank
    for x in (-0.168, 0.168):
        box((x, 0.20, 0.87), (0.02, 0.30, 0.11), M["rim_cyan"], rig)              # side panels
    box((0, -0.36, 0.87), (0.24, 0.50, 0.07), M["black"], rig)                    # seat
    box((0, -0.74, 0.93), (0.15, 0.30, 0.06), M["graphite"], rig)                 # tail
    box((0, 0.46, 0.96), (0.24, 0.16, 0.14), M["graphite"], rig)                  # headlamp housing
    box((0, 0.40, 1.07), (0.70, 0.05, 0.05), M["black"], rig)                     # handlebar
    cyl_between((0.16, -0.20, 0.42), (0.17, -0.74, 0.50), 0.05, M["black"], rig)  # exhaust
    cyl_between((0, -0.25, 0.42), (0, -0.66, 0.30), 0.035, M["black"], rig)       # swingarm
    # rider
    ell((0, -0.20, 1.24), (0.20, 0.17, 0.33), M["jacket"], rot=(math.radians(-22), 0, 0), parent=rig)
    build_helmet(M, (0, -0.02, 1.63), parent=rig)
    for sx in (-1, 1):
        cyl_between((sx * 0.20, -0.12, 1.40), (sx * 0.31, 0.38, 1.10), 0.050, M["jacket"], rig)
        cyl_between((sx * 0.13, -0.32, 0.99), (sx * 0.20, 0.03, 0.82), 0.075, M["jacket"], rig)
        cyl_between((sx * 0.20, 0.03, 0.82), (sx * 0.20, -0.12, 0.44), 0.060, M["jacket"], rig)
        box((sx * 0.20, -0.07, 0.40), (0.10, 0.26, 0.09), M["black"], rig)        # boot
        ell((sx * 0.31, 0.39, 1.09), (0.045, 0.06, 0.04), M["black"], parent=rig)  # glove


# ---------------------------------------------------------------- road world
def pop(ob, s, delay):
    f0 = P.frame_for(s) + delay
    if f0 <= 1:
        return
    ob.scale = (0, 0, 0); key(ob, "scale", f0)
    ob.scale = (1.18, 1.18, 1.18); key(ob, "scale", f0 + 5)
    ob.scale = (1, 1, 1); key(ob, "scale", f0 + 8)


def build_road(M, sh):
    sc = bpy.context.scene
    sc.world = make_world(sh["sky"])
    P.strip("road", -HALF_ROAD, HALF_ROAD, 0.0, M["wet_road"])
    P.strip("ground_built", BUILT * HALF_ROAD, BUILT * 80.0, 0.0, M["clay"], step=2.0)
    P.strip("promenade", WATER * HALF_ROAD, WATER * 4.9, 0.0, M["clay"])
    P.strip("bank", WATER * 4.9, WATER * 4.9001, -0.3, M["clay"])
    bpy.ops.mesh.primitive_plane_add(size=2400, location=(0, 0, -0.6))
    bpy.context.object.data.materials.append(M["water"])

    def placed(s, lat, size, z=0.0):
        return (Matrix.Translation(route(s, lat, z)) @ Matrix.Rotation(heading(s), 4, "Z")
                @ Matrix.Diagonal((*size, 1)))

    slots, dashes = [], []
    s = P.S_MIN + 1
    while s < P.S_MAX - 1:
        for lat in (HALF_ROAD + 0.16, -HALF_ROAD - 0.16):
            slots.append(placed(s, lat, (0.46, 0.92, 0.008), 0.004))
        if int(s) % 4 == 0:
            dashes.append(placed(s, 0.0, (0.12, 1.6, 0.006), 0.003))
        s += 1.0
    matrix_object("slots", slots, M["slot"])
    matrix_object("dashes", dashes, M["paint"])

    # kerb stones, one per metre on both sides
    s = P.S_MIN + 1
    while s < P.S_MAX - 1:
        for lat in (HALF_ROAD + 0.16, -HALF_ROAD - 0.16):
            ob = mesh_object("curb", [((0, 0, 0.13), (0.42, 0.94, 0.26))], M["module"],
                             route(s, lat), heading(s))
            ob.color = (0.62, 0.60, 0.55, 0)
            P.seat(ob, s)
        s += 1.0

    # waterside railing with small warm lamps: these are what the hero shot sees light up
    s, n = P.S_MIN + 1, 0
    while s < P.S_MAX - 2:
        post = mesh_object("rail_post", [((0, 0, 0.55), (0.16, 0.16, 1.1))], M["module"],
                           route(s, WATER * 4.5), heading(s))
        post.color = (0.50, 0.49, 0.46, 0)
        P.seat(post, s, delay=3, grow=True)
        rail = mesh_object("rail", [((0, 1.0, 0.95), (0.06, 1.86, 0.06)),
                                    ((0, 1.0, 0.55), (0.06, 1.86, 0.06))], M["module"],
                           route(s, WATER * 4.5), heading(s + 1.0))
        rail.color = (0.16, 0.17, 0.19, 0)
        P.seat(rail, s + 2.0, delay=6, drop=0.35)
        if n % 2 == 0:
            cap = mesh_object("rail_lamp", [((0, 0, 0), (0.20, 0.20, 0.16))], M["emit"],
                              route(s, WATER * 4.5, 1.20), heading(s))
            cap.color = (1.0, 0.66, 0.30, 0)
            P.glow(cap, s, delay=15)
            P.practical("rail_light", route(s, WATER * 4.35, 1.25), s, 15, 70, (1.0, 0.66, 0.30), 0.07)
        if n % 5 == 2:
            palm(M, s + 1.0, WATER * 4.12, 4.2 + random.random() * 1.2)
        s, n = s + 2.0, n + 1

    # street lamps and palms on the town-side pavement
    s = P.S_MIN + 4
    while s < P.S_MAX - 4:
        pole = mesh_object("lamp_pole", [((0, 0, 2.6), (0.10, 0.10, 5.2)),
                                         ((BUILT * 0.7, 0, 5.15), (1.5, 0.08, 0.08))], M["module"],
                           route(s, BUILT * (HALF_ROAD + 0.7)), heading(s))
        pole.color = (0.12, 0.13, 0.15, 0)
        P.seat(pole, s, delay=4, grow=True)
        head_lat = BUILT * (HALF_ROAD - 0.75)
        head = mesh_object("lamp_head", [((0, 0, 0), (0.5, 0.22, 0.08))], M["emit"],
                           route(s, head_lat, 5.08), heading(s))
        head.color = (1.0, 0.62, 0.28, 0)
        P.glow(head, s, delay=16)
        P.practical("lamp_light", route(s, head_lat, 4.9), s, 16, 800, (1.0, 0.62, 0.30), 0.2)
        if abs(s + 6 - STALL_S) > 4:
            palm(M, s + 6.0, BUILT * 4.6, 5.0 + random.random() * 1.5)
        s += 12.0

    # buildings: dull concrete masses first, then pastel Art Deco fronts, windows and neon
    pastel = [(0.86, 0.44, 0.36), (0.42, 0.74, 0.64), (0.88, 0.76, 0.52), (0.60, 0.50, 0.78),
              (0.26, 0.60, 0.64)]
    FACE = 6.4
    s, i = P.S_MIN + 3, 0
    while s < P.S_MAX - 6:
        width, depth, height = 8.2, 8.0, random.choice((7.0, 9.5, 12.0, 15.0))
        parts = [((0, 0, height / 2), (depth, width, height)),
                 ((0, 0, height + 0.5), (depth * 0.8, width * 0.7, 1.0)),          # stepped crown
                 ((0, 0, height + 1.4), (depth * 0.6, width * 0.36, 0.9)),
                 ((BUILT * -(depth / 2 + 0.12), 0, height * 0.55), (0.24, 0.7, height * 1.1))]  # fin
        mass = mesh_object("bldg", parts, M["module"], route(s, BUILT * (FACE + depth / 2)), heading(s))
        mass.color = (*pastel[i % 5], 0)
        f = P.frame_for(s) + 4
        if f <= 1:
            mass.color[3] = 1
        else:
            mass.color[3] = 0; key(mass, "color", f)
            mass.color[3] = 1; key(mass, "color", f + 10)
        face = route(s, BUILT * (FACE - 0.06))
        if abs(s - STALL_S) > 5:
            shutter = mesh_object("shutter", [((0, 0, 1.4), (0.10, 4.6, 2.8))], M["module"],
                                  face, heading(s))
            shutter.color = (0.20, 0.22, 0.24, 0)
            P.seat(shutter, s, delay=6, drop=1.2)
        wins = []
        for floor in range(1, int(height // 3)):
            for col in (-2.6, 0.0, 2.6):
                if random.random() < 0.7:
                    wins.append(((0, col, 1.6 + floor * 3.0), (0.08, 1.3, 1.5)))
        if wins:
            w_ob = mesh_object("windows", wins, M["emit"], face, heading(s))
            w_ob.color = (*random.choice(((1.0, 0.70, 0.36), (0.75, 0.85, 1.0))), 0)
            P.glow(w_ob, s, delay=18)
        col = ((0.0, 0.85, 1.0), (1.0, 0.05, 0.65))[i % 2]
        band = mesh_object("neon_band", [((0, 0, height - 0.35), (0.08, width * 0.86, 0.14)),
                                         ((0, 0, 3.25), (0.08, 3.8, 0.14))], M["neon"],
                           route(s, BUILT * (FACE - 0.16)), heading(s))
        band.color = (*col, 0)
        P.glow(band, s, delay=20)
        P.practical("neon_light", route(s, BUILT * 5.4, 3.2), s, 20, 240, col, 0.6)
        s, i = s + 9.0, i + 1

    # the tea stall: present and lit in BOTH states
    ST = STALL_S
    for dy, dl in ((-1.4, 4.2), (1.4, 4.2), (-1.4, 5.9), (1.4, 5.9)):
        p = mesh_object("stall_post", [((0, 0, 1.15), (0.09, 0.09, 2.3))], M["module"],
                        route(ST + dy, BUILT * dl), heading(ST))
        p.color = (0.30, 0.20, 0.12, 1)
    for name, parts, lat, col in (
            ("stall_roof", [((0, 0, 2.36), (2.3, 3.3, 0.10))], 5.05, (0.10, 0.22, 0.50)),
            ("stall_counter", [((0, 0, 0.5), (0.6, 2.6, 1.0))], 5.3, (0.36, 0.24, 0.14)),
            ("stall_stools", [((0, dy, 0.22), (0.30, 0.30, 0.44)) for dy in (-0.9, 0.0, 0.9)], 4.45,
             (0.70, 0.08, 0.06))):
        ob = mesh_object(name, parts, M["module"], route(ST, BUILT * lat), heading(ST))
        ob.color = (*col, 1)
    glasses = mesh_object("stall_glasses", [((0.05 * (k % 2), -0.9 + k * 0.22, 1.045), (0.055, 0.055, 0.09))
                                           for k in range(7)], M["emit"], route(ST, BUILT * 5.3), heading(ST))
    glasses.color = (0.75, 0.32, 0.08, 0.35)                            # tea in small glasses
    kettle = mesh_object("stall_kettle", [((0, 0.95, 1.12), (0.22, 0.22, 0.24))], M["module"],
                         route(ST, BUILT * 5.3), heading(ST))
    kettle.color = (0.55, 0.56, 0.58, 1)
    bulb = mesh_object("stall_bulb", [((0, 0, 0), (0.12, 0.12, 0.12))], M["emit"],
                       route(ST, BUILT * 5.0, 2.1), heading(ST))
    bulb.color = (1.0, 0.72, 0.36, 1)
    point(route(ST, BUILT * 5.0, 2.0), sh.get("stall_w", 260), (1.0, 0.72, 0.36), 0.08)

    # far shore across the water stays unbuilt
    for n in range(40):
        h = 8 + random.random() * 30
        mesh_object("far_clay", [((0, 0, h / 2 - 0.6), (14, 14, h))], M["clay"],
                    route(-20 + n * 8.0, WATER * (150 + random.random() * 70)), random.random())


def palm(M, s, lat, height):
    trunk = mesh_object("palm_trunk", [((0, 0, height / 2), (0.20, 0.20, height))], M["module"],
                        route(s, lat), heading(s))
    trunk.color = (0.30, 0.21, 0.13, 0)
    P.seat(trunk, s, delay=5, grow=True)
    blades = []
    for k in range(9):
        blades.append(Matrix.Rotation(math.radians(k * 40 + random.random() * 14), 4, "Z")
                      @ Matrix.Rotation(math.radians(-24 - random.random() * 14), 4, "X")
                      @ Matrix.Translation((0, 1.15, 0)) @ Matrix.Diagonal((0.34, 2.3, 0.03, 1)))
    crown = matrix_object("palm_crown", blades, M["module"])
    crown.location = route(s, lat, height)
    crown.color = (0.10, 0.42, 0.22, 0)
    f0 = P.frame_for(s) + 5
    if f0 > 1:
        crown.color[3] = 0.0; key(crown, "color", f0 + 12)
        crown.color[3] = 1.0; key(crown, "color", f0 + 18)
    else:
        crown.color[3] = 1.0
    pop(crown, s, 11)


def road_cameras(shot, n):
    """One camera per road shot. Water is always on the left of the direction of travel."""
    sb = P.s_bike
    if shot == "S04":       # from under the tea stall roof: the bike passes left to right in the rain
        cam, tgt = camera(shot, 20)
        path = lambda f: (route(STALL_S + 0.2, BUILT * 6.15, 1.55),
                          route(85.5 + 0.75 * (sb(f) - 85.5), BIKE_LAT, 0.95))
    elif shot == "S06":     # low front three-quarter, the angle of the official product photo
        cam, tgt = camera(shot, 26)
        path = lambda f: (route(sb(f) + 3.3 - 0.02 * f, BIKE_LAT + BUILT * 1.30, 0.46),
                          route(sb(f) + 0.1, BIKE_LAT, 0.82))
    elif shot == "S08":     # hero: beside the front wheel, looking along the beam
        cam, tgt = camera(shot, 18)
        path = lambda f: (route(sb(f) - 0.40, BIKE_LAT + WATER * 0.52, 0.30),
                          route(sb(f) + 6.5, BIKE_LAT + WATER * 0.70, -0.45))
    elif shot == "S09":     # aerial: built strip and the stall below, grey road above
        cam, tgt = camera(shot, 32)
        path = lambda f: (route(84.0 + f * 0.12, BUILT * 2.0, 34.0), route(sb(f) - 1.0, 0.0, 0.0))
    elif shot == "S10":     # rear chase: the city opens ahead
        cam, tgt = camera(shot, 22)
        path = lambda f: (route(sb(f) - 6.5 - 0.02 * f, BIKE_LAT + BUILT * 0.9, 1.45 + 0.012 * f),
                          route(sb(f) + 12.0, 0.5, 1.5))
    elif shot == "BG12":
        cam, tgt = camera(shot, 24)
        path = lambda f: (route(118.0, 0.7, 0.85), route(150.0, -1.2, 3.4))
    else:                   # PREVIEW
        cam, tgt = camera(shot, 22)
        path = lambda f: (route(112.0, BIKE_LAT, 1.6), route(140.0, 0.4, 1.9))
    for f in range(1, n + 1):
        cam.location, tgt.location = path(f)
        key(cam, "location", f)
        key(tgt, "location", f)
    return cam


def spray(M, rig, n):
    """Coloured spray trailing the rear wheel (S06). Amber near the tyre, magenta further out."""
    random.seed(11)
    for i in range(70):
        phase, life = random.random(), 14 + random.random() * 10
        side, up = random.uniform(-0.55, 0.55), random.uniform(0.6, 1.9)
        back, size = random.uniform(1.6, 3.6), random.uniform(0.018, 0.05)
        bead = ell((0, 0, 0), (size, size, size), M["liquid"], parent=rig, seg=10)
        for f in range(1, n + 1):
            t = ((f / life) + phase) % 1.0
            bead.location = (side * t, -0.95 - back * t, 0.06 + up * t - 1.7 * t * t)
            k = max(0.0, 1.0 - t)
            bead.scale = (size * k, size * k * 2.4, size * k)
            mix = min(1.0, t * 1.6)
            bead.color = (1.0, 0.45 * (1 - mix) + 0.07 * mix, 0.05 * (1 - mix) + 0.55 * mix, 1.0)
            for path in ("location", "scale", "color"):
                key(bead, path, f)


def build_road_shot(M, shot, sh):
    random.seed(7)
    build_road(M, sh)
    if sh.get("bike", True):
        rig = P.build_bike(M)
        build_body(M, rig)
        if shot == "S04":   # light from the shop side, so the passing bike is more than a shadow
            ld = bpy.data.lights.new("shop", "AREA")
            ld.energy, ld.size, ld.color = 520, 2.5, (1.0, 0.74, 0.46)
            k = link(bpy.data.objects.new("shop", ld))
            k.location, k.rotation_euler = (4.5, 0.4, 2.3), (0, math.radians(62), 0)
            child(k, rig)
            k.visible_glossy = False
        if shot == "S06":
            spray(M, rig, sh["n"])
            ld = bpy.data.lights.new("key", "AREA")
            ld.energy, ld.size, ld.color = 35, 1.6, (0.70, 0.85, 1.0)
            k = link(bpy.data.objects.new("key", ld))
            k.location, k.rotation_euler = (2.4, 2.6, 1.9), (math.radians(62), 0, math.radians(138))
            child(k, rig)
            k.visible_glossy = False
            point((0.3, -2.4, 0.7), 90, (1.0, 0.25, 0.45), 0.4, rig)      # spray colour on the road
            point((-0.9, -1.6, 1.9), 120, (1.0, 0.55, 0.25), 0.3, rig)    # amber rim on rider and tank
            bpy.data.lights["headlight"].energy = 1200                   # the lens sits in the beam
    return road_cameras(shot, sh["n"])


# ---------------------------------------------------------------- room (S01, S02, S03, S11)
def build_room(M, shot, sh, tv):
    sc = bpy.context.scene
    sc.world = make_world("room")
    n = sh["n"]
    wall = principled("wall", (0.13, 0.14, 0.17), 0.9)[0]
    wood = principled("wood", (0.07, 0.045, 0.03), 0.45)[0]
    dark = principled("dark", (0.025, 0.025, 0.03), 0.6)[0]
    fabric = principled("fabric", (0.05, 0.055, 0.07), 0.95)[0]
    skin = principled("skin", (0.36, 0.22, 0.15), 0.55)[0]
    olive = principled("olive", (0.20, 0.22, 0.12), 0.85)[0]
    hair = principled("hair", (0.012, 0.010, 0.010), 0.5)[0]

    box((0, 1.0, -0.02), (6, 8, 0.04), wood)
    box((0, 3.08, 1.5), (6, 0.06, 3.2), wall)
    box((-2.3, 1.0, 1.5), (0.06, 8, 3.2), wall)
    box((2.3, 1.0, 1.5), (0.06, 8, 3.2), wall)
    win = box((-2.25, 1.9, 1.55), (0.02, 1.1, 1.3), M["glow"])        # night window
    win.color = (0.10, 0.22, 0.60, 1)
    for dz in (-0.2, 0.25):
        box((-2.23, 1.9, 1.55 + dz), (0.03, 1.1, 0.04), dark)
    box((0, 2.80, 0.30), (1.9, 0.45, 0.5), dark)                       # TV console
    box((0, 3.00, 1.40), (1.36, 0.05, 0.80), dark)                     # TV frame
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 2.965, 1.40), rotation=(math.radians(90), 0, 0))
    screen = bpy.context.object
    screen.scale = (1.28, 0.72, 1)
    pct = "4" if shot == "S11" else "3"
    m, nt, b = principled("tv", (0, 0, 0), 0.25)
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.join(TEX, f"tv_{pct}_{tv}.png"))
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = 3.2
    screen.data.materials.append(m)
    # floor lamp, left of the TV
    box((-1.30, 2.75, 0.62), (0.04, 0.04, 1.24), dark)
    shade = ell((-1.30, 2.75, 1.34), (0.17, 0.17, 0.15), M["glow"])
    shade.color = (1.0, 0.62, 0.30, 1)
    point((-1.30, 2.70, 1.30), 70, (1.0, 0.62, 0.30), 0.12)
    # shelf with books
    box((1.35, 3.0, 2.30), (1.1, 0.22, 0.04), dark)
    for k, c in enumerate(((0.5, 0.1, 0.1), (0.1, 0.3, 0.4), (0.6, 0.5, 0.2), (0.2, 0.2, 0.25), (0.4, 0.15, 0.3))):
        box((0.95 + k * 0.11, 3.0, 2.45), (0.07, 0.18, 0.26 - 0.02 * (k % 3)), principled("bk", c, 0.7)[0])
    box((1.04, 2.62, 0.31), (0.46, 0.46, 0.62), dark)                  # side table
    box((0.50, 1.25, 0.24), (0.95, 0.50, 0.05), dark)                  # coffee table
    for dx in (-0.4, 0.4):
        box((0.50 + dx, 1.25, 0.11), (0.05, 0.40, 0.22), dark)
    box((0.20, -0.12, 0.52), (1.9, 0.26, 1.04), fabric)                # sofa back
    box((0.20, 0.35, 0.25), (1.9, 0.80, 0.50), fabric)                 # sofa seat

    HEL_TABLE = (0.62, 2.74, 0.69)          # on the TV console, under the right half of the screen
    fig = link(bpy.data.objects.new("figure", None))
    if shot in ("S01", "S11"):
        # seated, seen from behind: slouch, controller hanging in the right hand
        if shot == "S01":
            head = ell((0.22, 0.10, 1.20), (0.105, 0.115, 0.125), skin, parent=fig)
            ell((0.22, 0.075, 1.245), (0.112, 0.118, 0.105), hair, parent=head)
        else:                   # he is back, and has not even taken the helmet off
            head, _ = build_helmet(M, (0.22, 0.10, 1.215), 0.0, parent=fig)
            for k in range(30):  # rain still on the helmet
                a, b2 = random.uniform(0, 6.28), random.uniform(0.15, 1.5)
                ell((0.137 * math.sin(b2) * math.cos(a), 0.152 * math.sin(b2) * math.sin(a),
                     0.142 * math.cos(b2)), (0.006, 0.006, 0.004), M["glass"], parent=head, seg=8)
        cyl_between((0.22, 0.10, 1.02), (0.22, 0.10, 1.12), 0.05, skin, fig)
        ell((0.22, 0.12, 0.90), (0.27, 0.13, 0.20), M["jacket"] if shot == "S11" else olive, parent=fig)
        sleeve = M["jacket"] if shot == "S11" else skin
        cyl_between((0.46, 0.14, 0.96), (0.52, 0.42, 0.74), 0.045, sleeve, fig)
        hand = link(bpy.data.objects.new("hand", None))
        hand.location = (0.52, 0.42, 0.74)
        child(hand, fig)
        cyl_between((0, 0, 0), (-0.10, 0.28, 0.02), 0.038, skin, hand)
        box((-0.13, 0.33, 0.03), (0.16, 0.10, 0.045), dark, hand)
        led = box((-0.13, 0.33, 0.056), (0.03, 0.02, 0.006), M["glow"], hand)
        led.color = (0.2, 0.6, 1.0, 1)
        if shot == "S01":       # the hand gives up: controller sags, head tips sideways
            for f, rx, tilt in ((1, 0, 0), (10, 0, 0), (22, -0.50, 0.10), (30, -0.55, 0.12)):
                hand.rotation_euler = (rx, 0, 0); key(hand, "rotation_euler", f)
                head.rotation_euler = (0, tilt, 0); key(head, "rotation_euler", f)
            build_helmet(M, HEL_TABLE, math.radians(150))
        else:                   # back in the same seat; a small shake of the head at 4%
            point((1.2, -0.9, 1.7), 10, (1.0, 0.75, 0.55), 0.3)       # lets the wet helmet read
            for f, tilt in ((1, 0), (14, 0), (19, 0.16), (24, -0.12), (29, 0.07), (34, 0)):
                head.rotation_euler = (0, tilt, 0); key(head, "rotation_euler", f)
        cam, tgt = camera(shot, 44)
        for f in range(1, n + 1):
            u = (f - 1) / max(1, n - 1)
            if shot == "S01":
                cam.location = (0.50 - 0.04 * u, -1.05 + 0.25 * u, 1.50)
            else:
                cam.location = (0.50 - 0.01 * u, -1.05 + 0.05 * u, 1.50)
            tgt.location = (0.04, 3.0, 1.12)
            key(cam, "location", f); key(tgt, "location", f)
    elif shot == "S02":
        # the helmet in the TV glow; a hand comes in and lifts it
        hel, _ = build_helmet(M, HEL_TABLE, math.radians(150))
        x, y, z = HEL_TABLE
        glint = point((x - 0.9, y - 0.7, z + 0.25), 0, (0.80, 0.92, 1.0), 0.02)
        for f, w, gx in ((1, 0, -0.9), (9, 0, -0.9), (12, 16, -0.3), (15, 22, 0.3), (18, 0, 0.9)):
            glint.data.energy = w; glint.data.keyframe_insert("energy", frame=f)
            glint.location = (x + gx, y - 0.7, z + 0.25); key(glint, "location", f)
        for f, dz, tilt in ((1, 0, 0), (13, 0, 0), (16, 0, 0.05), (20, 0, 0)):
            hel.location = (x, y, z + dz); key(hel, "location", f)
            hel.rotation_euler = (tilt, 0, math.radians(150)); key(hel, "rotation_euler", f)
        point((1.5, 2.2, 1.3), 14, (1.0, 0.66, 0.40), 0.25)             # warm edge on the shell
        point((-0.3, 1.9, 1.1), 5, (0.55, 0.70, 1.0), 0.4)              # cool fill from the TV side
        cam, tgt = camera(shot, 50, fstop=2.8)
        for f in range(1, n + 1):
            u = (f - 1) / (n - 1)
            cam.location = (0.16 + 0.06 * u, 1.66 + 0.22 * u, 0.98 - 0.05 * u)
            tgt.location = (x, y, z + 0.03)
            key(cam, "location", f); key(tgt, "location", f)
    else:                       # S03: helmet on, visor snaps shut, TV still glowing behind
        bust = link(bpy.data.objects.new("bust", None))
        bust.location = (0.10, 1.15, 0)
        hel, pivot = build_helmet(M, (0, 0, 1.62), math.radians(200), parent=bust)
        ell((0, 0.02, 1.26), (0.25, 0.15, 0.27), M["jacket"], parent=bust)
        box((0, -0.10, 1.40), (0.34, 0.02, 0.035), principled("stripe", (0.45, 0.47, 0.5), 0.3)[0], bust)
        for f, deg in ((1, 58), (3, 58), (7, -3), (8, 0), (12, 0)):
            pivot.rotation_euler = (math.radians(deg), 0, 0); key(pivot, "rotation_euler", f)
        cam, tgt = camera(shot, 40, fstop=2.8)
        for f in range(1, n + 1):
            u = (f - 1) / (n - 1)
            cam.location = (0.44 - 0.02 * u, 0.30 + 0.05 * u, 1.60)
            tgt.location = (0.10, 1.15, 1.615)
            key(cam, "location", f); key(tgt, "location", f)
        point((0.9, 0.5, 1.9), 34, (1.0, 0.70, 0.45), 0.3)            # soft warm key on the helmet
    return cam


# ---------------------------------------------------------------- macro sets
def build_drop(M, sh):
    """S05: a hanging raindrop, time frozen. The headlight reaches it and it bursts into colour."""
    sc = bpy.context.scene
    sc.world = make_world("rain")
    n = sh["n"]
    random.seed(5)
    leaf = principled("leaf", (0.05, 0.16, 0.06), 0.35)[0]
    lf = ell((-0.02, 0.10, 0.125), (0.05, 0.13, 0.005), leaf, rot=(math.radians(-38), 0, math.radians(20)))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.042, segments=48, ring_count=32, location=(0, 0, -0.03))
    drop = op_object(M["glass"])
    for v in drop.data.vertices:            # pull the top of the sphere into a teardrop neck
        if v.co.z > 0:
            t = v.co.z / 0.042
            k = (1 - t) ** 1.6 * 0.94 + 0.06
            v.co.x, v.co.y, v.co.z = v.co.x * k, v.co.y * k, v.co.z * 2.5
    for i in range(16):                     # other drops, frozen in the air
        r = random.uniform(0.004, 0.012)
        ell((random.uniform(-0.22, 0.22), random.uniform(-0.08, 0.5), random.uniform(-0.28, 0.22)),
            (r, r, r * 1.25), M["glass"], seg=16)
    box((0, 6, -1.7), (40, 60, 0.02), M["wet_road"])
    for i in range(6):                      # the street, far out of focus
        b = ell((-0.9 + i * 0.25, 5.0 + i * 2.2, 0.75 - i * 0.07), (0.07, 0.07, 0.07), M["glow"], seg=12)
        b.color = (0.75, 0.86, 1.0, 1)
    stall = ell((1.3, 7.5, -0.35), (0.16, 0.16, 0.16), M["glow"], seg=12)
    stall.color = (1.0, 0.60, 0.22, 1)
    # the headlight arrives from behind-left of the drop
    lamp = ell((-0.55, 3.2, -0.25), (0.05, 0.05, 0.05), M["glow"], seg=12)
    ld = bpy.data.lights.new("beam", "SPOT")
    ld.spot_size, ld.color, ld.shadow_soft_size = math.radians(30), (0.85, 0.93, 1.0), 0.02
    beam = link(bpy.data.objects.new("beam", ld))
    beam.location = (-0.55, 3.2, -0.25)
    aim = beam.constraints.new("TRACK_TO")
    aim.target, aim.track_axis, aim.up_axis = drop, "TRACK_NEGATIVE_Z", "UP_Y"
    for f, w, a in ((1, 0, 0.0), (5, 0, 0.05), (11, 900, 1.0), (30, 1500, 1.0)):
        ld.energy = w; ld.keyframe_insert("energy", frame=f)
        lamp.color = (0.9, 0.95, 1.0, a * 3); key(lamp, "color", f)
    glow = point((0.03, 0.0, -0.03), 0, (1.0, 0.35, 0.25), 0.02)
    for f, w in ((11, 0), (14, 6), (30, 3)):
        glow.data.energy = w; glow.data.keyframe_insert("energy", frame=f)
    # the burst: liquid arms thrown to screen right, amber at the root and magenta at the tips
    BURST = 12
    for arm in range(9):
        d = Vector((1.0, random.uniform(-0.07, 0.07), random.uniform(-0.30, 0.42))).normalized()
        side = d.cross(Vector((0, 0, 1))).normalized()
        length, beads, r0 = random.uniform(0.20, 0.46), 28, random.uniform(0.009, 0.014)
        ph = random.uniform(0, 6.28)
        for i in range(beads):
            q = i / (beads - 1)
            r = r0 * (1 - q) ** 0.45 + 0.002
            bead = ell((0, 0, 0), (r, r, r), M["liquid"], seg=12)
            bead["burst"] = 1
            mixc = min(1.0, max(0.0, (q - 0.25) / 0.5))
            col = (1.0, 0.30 * (1 - mixc) + 0.02 * mixc, 0.02 * (1 - mixc) + 0.45 * mixc)
            for f in range(BURST - 1, n + 1):
                t = max(0.0, (f - BURST) / 16.0)
                e = 1 - (1 - min(1.0, t)) ** 2.6 + 0.15 * t
                pos = (Vector((0.035, 0, -0.03)) + d * length * e * q ** 0.85
                       + side * math.sin(q * 5 + ph) * 0.018 * e + Vector((0, 0, -0.05 * t * t * q)))
                bead.location = pos
                bead.color = (*col, 1.0 if f >= BURST else 0.0)
                s = 0.0 if f < BURST else min(1.0, 0.35 + t * 4)
                bead.scale = (r * s, r * s, r * s)
                for path in ("location", "color", "scale"):
                    key(bead, path, f)
    cam, tgt = camera("S05", 70, fstop=5.6)
    for f in range(1, n + 1):
        u = (f - 1) / (n - 1)
        cam.location = (0.04 + 0.08 * u, -0.95 + 0.05 * u, -0.05)
        tgt.location = (0.07 + 0.06 * u, 0.0, -0.03)
        key(cam, "location", f); key(tgt, "location", f)
    return cam


def build_puddle(M, sh):
    """S07: one drop hits a puddle and the rings carry the colour outward."""
    sc = bpy.context.scene
    sc.world = make_world("rain")
    n = sh["n"]
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=220, size=3.6)
    water = op_object(M["water"])
    import numpy as np
    nv = len(water.data.vertices)
    co = np.empty(nv * 3)
    water.data.vertices.foreach_get("co", co)
    co = co.reshape(nv, 3)
    rad = np.hypot(co[:, 0], co[:, 1])

    def ripple(scene, *_):
        t = (scene.frame_current + scene.frame_subframe - 3.0) / FPS       # the drop lands on frame 3
        front = max(0.0, t) * 0.95                                         # ring train grows at 0.95 m/s
        z = 0.007 * np.sin(2 * math.pi * (rad - front) / 0.10) * np.exp(-(front - rad) / 0.30)
        z = np.where(rad < front, z, 0.0) * np.exp(-rad / 1.1)
        out = co.copy()
        out[:, 2] = z
        water.data.vertices.foreach_set("co", out.ravel())
        water.data.update()
    bpy.app.handlers.frame_change_pre.append(ripple)
    box((0, 3.0, -0.04), (30, 30, 0.02), M["wet_road"])
    for x, y, z, r, col in ((-0.5, 5.5, 1.5, 0.22, (1.0, 0.60, 0.22)), (0.6, 6.5, 1.9, 0.20, (1.0, 0.08, 0.55)),
                            (0.1, 8.0, 2.6, 0.18, (0.80, 0.90, 1.0)), (-1.3, 7.0, 2.2, 0.16, (1.0, 0.60, 0.22)),
                            (1.5, 9.0, 3.0, 0.20, (0.0, 0.80, 1.0))):
        b = ell((x, y, z), (r * 0.6, r * 0.6, r * 0.6), M["neon"], seg=12)
        b.color = (*col, 0.25)
        key(b, "color", 2)
        b.color = (*col, 1.0)
        key(b, "color", n)
    # the beam arriving: a low white light that sweeps onto the upper half of the frame
    point((-1.8, 2.6, 0.35), 160, (1.0, 0.55, 0.25), 0.05)           # raking amber: lights the ring crests
    point((1.6, 3.0, 0.45), 140, (1.0, 0.10, 0.55), 0.05)            # raking magenta
    sweep = point((2.6, 4.0, 0.5), 0, (0.85, 0.93, 1.0), 0.3)
    for f, wt in ((4, 0), (n, 700)):
        sweep.data.energy = wt; sweep.data.keyframe_insert("energy", frame=f)
    faller = ell((0, 0, 0.5), (0.014, 0.014, 0.03), M["liquid"], seg=12)
    faller.color = (1.0, 0.25, 0.30, 1)
    for f, z, s in ((1, 0.55, 1), (3, 0.0, 1), (4, -0.02, 0)):
        faller.location = (0, 0, z); key(faller, "location", f)
        faller.scale = (0.014 * s, 0.014 * s, 0.03 * s); key(faller, "scale", f)
    for k in range(10):                     # the crown thrown up by the hit
        a = k * 0.628
        bead = ell((0, 0, 0), (0.008, 0.008, 0.008), M["liquid"], seg=8)
        bead.color = (1.0, 0.30, 0.20, 1)
        for f in range(3, n + 1):
            t = (f - 3) / 9.0
            bead.location = (0.13 * t * math.cos(a), 0.13 * t * math.sin(a), 0.22 * t - 0.26 * t * t)
            s = 0.008 if 0 < t < 0.85 else 0.0
            bead.scale = (s, s, s)
            key(bead, "location", f); key(bead, "scale", f)
    cam, tgt = camera("S07", 45, fstop=5.6)
    for f in range(1, n + 1):
        cam.location = (0.0, -1.05 + 0.004 * f, 0.50)
        tgt.location = (0.0, 0.10, 0.0)
        key(cam, "location", f); key(tgt, "location", f)
    return cam


# ---------------------------------------------------------------- main
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", required=True, choices=list(SHOTS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", default="")
    ap.add_argument("--scale", type=int, default=100)
    ap.add_argument("--samples", type=int, default=0)
    ap.add_argument("--tv", default="named", choices=("named", "clean"))
    ap.add_argument("--blend", default="")
    ap.add_argument("--n", type=int, default=0, help="override the shot length in frames (for handles)")
    ap.add_argument("--burst-only", action="store_true",
                    help="S05: render only the colour burst on a transparent background, for comping over a still")
    a = ap.parse_args(argv)

    if a.n:
        SHOTS[a.shot]["n"] = a.n
    sh = configure(a.shot)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.render.fps = 1, sh["n"], FPS
    M = extra_materials(P.make_materials())
    kind = sh["set"]
    if kind == "road":
        cam = build_road_shot(M, a.shot, sh)
    elif kind == "room":
        cam = build_room(M, a.shot, sh, a.tv)
    elif kind == "drop":
        cam = build_drop(M, sh)
    else:
        cam = build_puddle(M, sh)
    sc.camera = cam

    r = sc.render
    r.engine = "CYCLES"
    r.resolution_x, r.resolution_y = sh.get("res", (720, 1280))
    r.resolution_percentage = a.scale
    r.image_settings.file_format = "PNG"
    r.use_persistent_data = True
    r.use_motion_blur = bool(sh.get("mblur")) or kind in ("drop", "puddle")
    r.motion_blur_shutter = 0.5
    cy = sc.cycles
    cy.samples = a.samples or sh.get("samples", 24 if kind in ("drop", "puddle", "room") else 16)
    cy.use_denoising, cy.use_adaptive_sampling = True, True
    glassy = kind in ("drop", "puddle")
    cy.max_bounces = 10 if glassy else 4
    cy.diffuse_bounces, cy.glossy_bounces = 2, 4 if glassy else 3
    cy.transmission_bounces = 8 if glassy else 2
    cy.caustics_reflective = cy.caustics_refractive = False
    sc.view_settings.exposure = {"road": 0.6, "room": 1.5, "drop": 0.6, "puddle": 0.7}[kind]
    if kind in ("drop", "puddle"):
        sc.view_settings.view_transform = "Standard"      # keeps the amber and magenta saturated
    if kind == "road" and sh["sky"] == "rain":
        sc.view_settings.exposure = 0.75
    if a.burst_only:
        for ob in sc.objects:
            if ob.type in ("MESH", "LIGHT") and not ob.get("burst"):
                ob.hide_render = True
        sc.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
        r.film_transparent = True
        r.image_settings.color_mode = "RGBA"
    if a.blend:
        bpy.ops.wm.save_as_mainfile(filepath=a.blend)
    frames = []
    for part in (a.frames or f"1-{sh['n']}").split(","):
        lo, _, hi = part.partition("-")
        frames += range(int(lo), int(hi or lo) + 1)
    for f in frames:
        sc.frame_set(f)
        r.filepath = f"{a.out}/f{f:04d}.png"
        bpy.ops.render.render(write_still=True)
        print(f"FRAME_DONE {a.shot} {f}", flush=True)


if __name__ == "__main__":
    main()
