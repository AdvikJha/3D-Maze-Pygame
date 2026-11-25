import pygame
import numpy as np
import math

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


focal_length = 1
distance = 10
scale = 100

near_plane = 0.1

def projection(x, y, z):
    x_2d = (focal_length * x)/z
    y_2d = (focal_length * y)/z
    return x_2d, y_2d

def render(x, y): #projected graphical points --> points to render
    rendered_x = x * scale + WIDTH/2
    rendered_y = y * scale + HEIGHT/2
    return rendered_x, rendered_y

camera_position = np.array([0, 0, -1 * distance])

camera_yaw = 0
camera_pitch = 0
camera_pitch_min = -math.pi/2
camera_pitch_max = math.pi/2
rotation_speed = 1.5

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

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

    pygame.display.flip()

pygame.quit()
