import pygame
import numpy as np

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

def projection(x, y, z):
    x_2d = (focal_length * x)/z
    y_2d = (focal_length * y)/z
    return x_2d, y_2d

camera_position = np.array([0, 0, -1 * distance])

camera_yaw = 0
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
        camera_yaw -= rotation_speed * dt
    elif keys[pygame.K_LEFT]:
        camera_yaw += rotation_speed * dt

    screen.fill(BLACK)

    rotation_y = np.array([ #Rotation Matrix for Y Axis
        [np.cos(camera_yaw), 0, np.sin(camera_yaw)],
        [0, 1, 0],
        [-np.sin(camera_yaw), 0, np.cos(camera_yaw)]
    ])

    projected_points = np.empty((0, 2))
    render_points = np.empty((0, 2))

    camera_baseplate_vertices = (rotation_y.T @ (baseplate_points-camera_position).T).T

    for x, y, z in camera_baseplate_vertices:  #Render Points
        x_2d, y_2d = projection(x, y, z)
        projected_points = np.vstack((projected_points, [x_2d, y_2d]))
        rendered_x = x_2d*scale+WIDTH/2
        rendered_y = y_2d*scale+HEIGHT/2
        render_points = np.vstack((render_points, [rendered_x, rendered_y]))
        pygame.draw.circle(screen, WHITE, (round(x_2d*scale+WIDTH/2), round(y_2d*scale+HEIGHT/2)), 3)

    for start, end in baseplate_edges: #Render Edges
        pygame.draw.line(screen, WHITE, tuple(render_points[start]), tuple(render_points[end]), 3)

    pygame.display.flip()

pygame.quit()
