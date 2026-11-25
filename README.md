# 3D-Maze-Pygame
This is a maze simulation built entirely in Python with only pygame and numpy. It is currently a work in progress.

## Features
 - 3D Software Rendering
 - Perspective Projection
 - World-to-Camera Transformation
 - Camera Yaw Rotation
 - Near Plane Clipping

## How it works
First, we must edit the coordinates of the baseplate relative to our perspective. I applied the World-to-Camera Transformation formula where $V_{camera}$ is camera_baseplate_vertices, $V_{world}$ is baseplate_points, $C$ is camera_position, $R_y$ is rotation_y, and $\theta$ is camera_yaw. We use the inverse of the camera's rotation matrix because we are transforming world coordinates into camera space. Instead of making the camera orbit the world, we use the opposite rotation to the world coordinates to express their positions relative to the camera. We can calculate the inverse using the transpose because rotation matrices are orthogonal.

World-to-Camera Transformation Formula:

$$
V_{camera}=R_y^{-1}(V_{world}-C)
$$

Y Rotation Matrix:

$$
R_y=
\begin{bmatrix}
\cos(\theta) & 0 & \sin(\theta)\\
0 & 1 & 0\\
-\sin(\theta) & 0 & \cos(\theta)
\end{bmatrix}
$$

The simulation starts with three dimensional coordinates for my baseplate. Because pygame is a two dimensional environment, we must project these points onto a two dimensional screen. I used the Perspective Projection Equation (formula shown below) where f is focal length and d is camera distance.


$$
2D = \left(\frac{xf}{z_{camera}+d}, \frac{yf}{z_{camera}+d}\right)
$$

Though in my code, d is not used and instead the denominator is just z. This is because on I have already subtracted camera position. 

Once we have the projected points, we need to render the points by centering it and multiplying by scale.

$$
\text{Rendered} =
\left(
x_{\text{2D}}\cdot s+\frac{\text{W}}{2},
\quad
y_{\text{2D}}\cdot s+\frac{\text{H}}{2}
\right)
$$

Next, we use Near Plane Clipping to allow geometry that is behind or too close to the camera to be hidden. Without it, points will be shown even when not in the line of sight of the camera. I calculated Near Plane using Linear Interpolation.

\[
P=A+t(B-A)
\]

\[
t=\frac{z_{\text{near}}-z_A}{z_B-z_A}
\]

$A$: Starting endpoint of the edge
$B$: Ending endpoint of the edge
$P$: Point where Near Plane intersects with Edge 
$t$: Interpolation factor between 0 and 1
$z_{near}$: Camera-space depth of the near plane

## Installation

To use this simulation you must have python installed. You also need to have numpy and pygame installed. If you do not have them installed, open Terminal and run:

```
pip install numpy pygame
```

Next, download the Maze.py file and run this in your Terminal

```
python downloads/Maze.py
```

## Controls

| Key | Function |
|---|---|
| Left Arrow | Rotate camera left |
| Right Arrow | Rotate camera right |
