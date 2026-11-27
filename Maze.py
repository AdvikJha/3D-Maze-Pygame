import pygame
import numpy as np
import math
import random

# Initialize
pygame.init()

# Display
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Maze")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Baseplate
baseplate_points = np.array([
    [4, 0, 4],
    [-4, 0, 4],
    [4, 0, -4],
    [-4, 0, -4],
    [4, -1, 4],
    [-4, -1, 4],
    [4, -1, -4],
    [-4, -1, -4]
])

baseplate_edges = np.array([
    [0, 1],
    [0, 2],
    [1, 3],
    [2, 3],
    [4, 5],
    [4, 6],
    [5, 7],
    [6, 7],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
])

baseplate_faces = np.array([
    [0, 2, 3, 1],  # Top
    [4, 5, 7, 6],  # Bottom
    [0, 1, 5, 4],  # Front (+Z)
    [2, 6, 7, 3],  # Back (-Z)
    [0, 4, 6, 2],  # Right (+X)
    [1, 3, 7, 5],  # Left (-X)
])

baseplate_side_colors = [
    (255, 0, 0),
    (122.5, 122.5, 0),
    (0, 255, 0),
    (0, 122.5, 122.5),
    (0, 0, 255),
    (255, 0, 255)
]

focal_length = 1
distance = 10
scale = 100

near_plane = 0.1

def clip_polygon(vertices, near_plane):
    clipped = []

    for i in range(len(vertices)):
        current = vertices[i]
        previous = vertices[i - 1]

        current_inside = current[2] >= near_plane
        previous_inside = previous[2] >= near_plane

        if current_inside != previous_inside:
            t = (near_plane - previous[2]) / (current[2] - previous[2])
            intersection = previous + t * (current - previous)
            clipped.append(intersection)

        if current_inside:
            clipped.append(current)

    return clipped

def projection(x, y, z):
    x_2d = (focal_length * x)/z
    y_2d = (focal_length * y)/z
    return x_2d, y_2d

def render(x, y): #projected graphical points --> points to render
    rendered_x = x * scale + WIDTH/2
    rendered_y = y * scale + HEIGHT/2
    return rendered_x, rendered_y

camera_position = np.array([0.0, -2.0, -1.0 * distance])
camera_facing_direction = np.array([0, 0, 1])

camera_yaw = 0
camera_pitch = 0
camera_pitch_min = -math.pi/2
camera_pitch_max = math.pi/2
rotation_speed = 1.5
movement_speed = 5

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    forward = np.array([
        np.sin(camera_yaw),
        0,
        np.cos(camera_yaw)
    ])

    right = np.array([
        np.cos(camera_yaw),
        0,
        -np.sin(camera_yaw)
    ])

    #Camera Direction
    if keys[pygame.K_RIGHT]:
        camera_yaw += rotation_speed * dt
    elif keys[pygame.K_LEFT]:
        camera_yaw -= rotation_speed * dt
    if keys[pygame.K_UP]:
        if camera_pitch < camera_pitch_max:
            camera_pitch += rotation_speed * dt
    elif keys[pygame.K_DOWN]:
        if camera_pitch > camera_pitch_min:
            camera_pitch -= rotation_speed * dt

    #Camera Movement
    if keys[pygame.K_q]:
        camera_position[1] += movement_speed * dt
    elif keys[pygame.K_e]:
        camera_position[1] -= movement_speed * dt
    if keys[pygame.K_w]:
        camera_position += movement_speed * dt * forward
    elif keys[pygame.K_s]:
        camera_position -= movement_speed * dt * forward
    if keys[pygame.K_d]:
        camera_position += movement_speed * dt * right
    elif keys[pygame.K_a]:
        camera_position -= movement_speed * dt * right


    screen.fill(BLACK)

    rotation_y = np.array([ #Rotation Matrix for Y Axis
        [np.cos(camera_yaw), 0, np.sin(camera_yaw)],
        [0, 1, 0],
        [-np.sin(camera_yaw), 0, np.cos(camera_yaw)]
    ])

    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(camera_pitch), -np.sin(camera_pitch)],
        [0, np.sin(camera_pitch), np.cos(camera_pitch)]
    ])

    camera_baseplate_vertices = (rotation_x.T @ rotation_y.T @ (baseplate_points-camera_position).T).T

    edge_baseplate_points = np.empty((0, 2, 3))

    for start, end in baseplate_edges:
        z_start = camera_baseplate_vertices[start][2]
        z_end = camera_baseplate_vertices[end][2]
        point_a = camera_baseplate_vertices[start]
        point_b = camera_baseplate_vertices[end]
        if (z_start < near_plane) != (z_end < near_plane):
            interpolation_factor = (near_plane - z_start)/ (z_end - z_start)
            intersect = point_a + interpolation_factor * (point_b - point_a)
            if z_start < near_plane:
                point_a = intersect
            else:
                point_b = intersect
        if z_start < near_plane and z_end < near_plane:
            continue
        edge_baseplate_points = np.vstack((edge_baseplate_points, [[point_a, point_b]]))

    for point_a, point_b in edge_baseplate_points: #Render Edges
        x_a, y_a = projection(point_a[0], point_a[1], point_a[2])
        x_b, y_b = projection(point_b[0], point_b[1], point_b[2])
        rendered_x_a, rendered_y_a = render(x_a, y_a)
        rendered_x_b, rendered_y_b = render(x_b, y_b)
        pygame.draw.line(screen, WHITE, (rendered_x_a, rendered_y_a), (rendered_x_b, rendered_y_b), 3)

    for i, face in enumerate(baseplate_faces):
        face_vertices = [camera_baseplate_vertices[index] for index in face]

        clipped_vertices = clip_polygon(face_vertices, near_plane)

        if len(clipped_vertices) >= 3:
            projected_face = []

            for vertex in clipped_vertices:
                x, y, z = vertex
                x_2d, y_2d = projection(x, y, z)

                screen_x = int(x_2d * scale + WIDTH / 2)
                screen_y = int(y_2d * scale + HEIGHT / 2)

                projected_face.append((screen_x, screen_y))

            A = clipped_vertices[0]
            B = clipped_vertices[1]
            C = clipped_vertices[2]

            camera_facing_direction = -(A + B + C)/3

            normal = np.cross(B - A, C - A)
            visibility = np.dot(normal, camera_facing_direction)

            if visibility > 0:
                pygame.draw.polygon(screen, baseplate_side_colors[i], projected_face)



    pygame.display.flip()

pygame.quit()
