"""
MIT License

Copyright (c) 2017 Cyrille Rossant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import matplotlib.pyplot as plt

w = 400
h = 300

def normalize(x):
    x /= np.linalg.norm(x)
    return x

def intersect_plane(O, D, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the 
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d

def intersect_triangle(O, D, v0, v1, v2):
    # Return the distance from O to the intersection of the ray (O, D) with the 
    # triangle (v1, v2, v3), or +inf if there is no intersection.
    
    N = triangle_plane_normal(v0,v1,v2)

    denom = np.dot(D, N)

    # Check if ray and plane are parallel
    if np.abs(denom) < 1e-6:
        return np.inf  # parallel, so they dont intersect
    
    d = np.dot(v0 - O, N) / denom
    if d < 0:
        return np.inf
    
    # Find the point of intersection on the object.
    M = O + D * d

    if check_inside_triangle(v0, v1, v2, M, N) == False:
        return np.inf  # the point of intersection M is not inside the triangle
    
    return d    


def check_inside_triangle(v0, v1, v2, M, N):
    # inside-outside test

    # edge 0
    edge0 = v1 - v0
    vp0 = M - v0

    # C: vector perpendicular to triangle's plane 
    C = np.cross(edge0,vp0); 
    if np.dot(N,C) < 0:
        return False  #M is on the right side 
 
    # edge 1
    edge1 = v2 - v1 
    vp1 = M - v1
    C = np.cross(edge1,vp1); 
    if np.dot(N,C) < 0:
        return False  #M is on the right side 
 
    # edge 2
    edge2 = v0 - v2 
    vp2 = M - v2 
    C = np.cross(edge2,vp2); 
    if np.dot(N,C) < 0:
      return False  #M is on the right side 
    
    #this ray hits the triangle
    return True


def triangle_plane_normal(v0, v1, v2):
    # compute plane's normal
    v0v1 = v1-v0
    v0v2 = v2-v0
    N = np.cross(v0v1,v0v2)
    return normalize(N)

def intersect_sphere(O, D, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the 
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a scalar.
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf

def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])
    elif obj['type'] == 'triangle':
        return intersect_triangle(O, D, obj['v0'], obj['v1'], obj['v2'])

def get_normal(obj, M):
    # Find normal.
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    elif obj['type'] == 'triangle':
        N = triangle_plane_normal(obj["v0"],obj["v1"],obj["v2"])   
    return N
    
def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color

def trace_ray(rayO, rayD):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i
    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return
    # Find the object.
    obj = scene[obj_idx]
    # Find the point of intersection on the object.
    M = rayO + rayD * t
    # Find properties of the object.
    N = get_normal(obj, M)
    color = get_color(obj, M)
    # Start computing the color.
    col_ray = compute_light(obj, N, M, color, obj_idx)
    return obj, M, N, col_ray

def add_sphere(position, radius, color):
    return dict(type='sphere', position=np.array(position), 
        radius=np.array(radius), color=np.array(color), reflection=.5)
    
def add_plane(position, normal):
    return dict(type='plane', position=np.array(position), 
        normal=np.array(normal),
        color=lambda M: (color_plane0 
            if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else color_plane1),
        diffuse_c=.75, specular_c=.5, reflection=.25)

def add_triangle(position_v0, position_v1, position_v2, color):
    return dict(type='triangle',
                v0=np.array(position_v0),
                v1=np.array(position_v1),
                v2=np.array(position_v2),
                color=np.array(color), 
                reflection=.5)

def compute_light(obj, N, M, color, obj_idx):
    toO = normalize(O - M)
    col_ray = ambient
    for light in light_set:
        toL = normalize(light["position"] - M)
        # Shadow: find if the point is shadowed or not.
        l = [intersect(M + N * .0001, toL, obj_sh) 
                for k, obj_sh in enumerate(scene) if k != obj_idx]
        if l and min(l) >= np.inf:
            # Lambert shading (diffuse).
            col_ray += (
                color
                * obj.get('diffuse_c', diffuse_c)
                * max(np.dot(N, toL), 0) 
            )
            # Blinn-Phong shading (specular).
            col_ray += (
                light["color"]
                * obj.get('specular_c', specular_c)
                * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k 
            )       
    return col_ray
    
# List of objects.
color_plane0 = 1. * np.ones(3)
color_plane1 = 0. * np.ones(3)

triangle_v0 = [0.25, -0.25, -0.25]
triangle_v1 = [-0.25, -0.25, -0.25]
triangle_v2 = [-0.25,  0.25, -0.25]
triangle_color = [0., 0., 1.]

scene = [add_sphere([.75, .1, 1.], .6, [0., 0., 1.]),
         add_sphere([-.75, .1, 2.25], .6, [.5, .223, .5]),
         add_sphere([-2.75, .1, 3.5], .6, [1., .572, .184]),
         add_plane([0., -.5, 0.], [0., 1., 0.]),
         add_triangle(triangle_v0, triangle_v1, triangle_v2, triangle_color),
         add_triangle([-0.25,-0.25,0.25],[-0.25,0.25,0.25],[0.25,0.25,0.25],[1.,0.,0.])
        ]

# Define here a Light Set with position and color for each individual light.

# original
light1 = {
  "position": np.array([5., 5., -10.]),
  "color": np.ones(3)
}
# cyan
light2 = {
  "position": np.array([-5., 5., -5.]),
  "color":  np.array([0., 1., 1.])
}
# magenta
light3 = {
  "position": np.array([-15., 1., -5.]),
  "color":  np.array([1., 0., 1.])
}

#light_set = [light1, light2, light3]
light_set = [light1, light2]
#light_set = [light1]

# Default light and material parameters.
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50

depth_max = 5  # Maximum number of light reflections.
col = np.zeros(3)  # Current color.
O = np.array([0., 0.35, -1.])  # Camera.
Q = np.array([0., 0., 0.])  # Camera pointing to.
img = np.zeros((h, w, 3))

r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1., -1. / r + .25, 1., 1. / r + .25)

# Loop through all pixels.
for i, x in enumerate(np.linspace(S[0], S[2], w)):
    if i % 10 == 0:
        print i / float(w) * 100, "%"
    for j, y in enumerate(np.linspace(S[1], S[3], h)):
        col[:] = 0
        Q[:2] = (x, y)
        D = normalize(Q - O)
        depth = 0
        rayO, rayD = O, D
        reflection = 1.
        # Loop through initial and secondary rays.
        while depth < depth_max:
            traced = trace_ray(rayO, rayD)
            if not traced:
                break
            obj, M, N, col_ray = traced
            # Reflection: create a new ray.
            rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
            depth += 1
            col += reflection * col_ray
            reflection *= obj.get('reflection', 1.)
        img[h - j - 1, i, :] = np.clip(col, 0, 1)

plt.imsave('2triangle2light.png', img)