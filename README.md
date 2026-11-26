# 3D-Maze-Pygame
This is a maze simulation built entirely in python with only pygame and numpy. It is currently a work in progress.

## Features
 - 3D Coordinate System
 - Perspective Projection
 - World-to-Camera Transformation
 - Camera Yaw and Pitch Rotation
 - Six-Direction Camera Movement
 - Near Plane Clipping

## How it works
First, we must edit the coordinates of the baseplate relative to our perspective. I applied the World-to-Camera Transformation formula where $V_{camera}$ is camera_baseplate_vertices, $V_{world}$ is baseplate_points, $C$ is camera_position, $R_y$ is rotation_y, $R_x$ is rotation_x, $\theta$ is camera_yaw, and $\phi& is camera_pitch. To avoid having people looking too far up or down I set the range to $-\frac{\pi}{2} \leq \phi \leq \frac{\pi}{2} For this formula we must use the inverse of Ry because Ry would rotate world relative to the camera so the inverse rotates the camera relative to the world. We can calculate the inverse using the transpose because rotation matrices are orthogonal.

World-to-Camera Transformation Formula:

$$
V_{camera}=R_x^{-1} \cdot R_y^{-1}(V_{world}-C)
$$

X Rotation Matrix:

$$
R_x=
\begin{bmatrix}
1 & 0 & 0\\
0 & \cos(\phi) & -\sin(\phi)\\
0 & \sin(\phi) & \cos(\phi)
\end{bmatrix}
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

Next, we need to add camera movement. Adding vertical camera movement is simple. We just need to change the y coordinate. For WASD movement though, to make sure the camera moves forward relative to the current camera yaw, we need a forward and right variable. I used these equations for my WASD EQ movement.

$$
y_{pos} = y_{pos} + v \cdot \Delta t
$$

$$
C = C + v \cdot \Delta t \cdot v_f
$$

$$
C = C + v \cdot \Delta t \cdot v_r
$$

$$
v_f = 
\begin{bmatrix}
\sin(\theta)\\
0\\
\cos(\theta)
\end{bmatrix}
$$

$$
v_r = 
\begin{bmatrix}
\cos(\theta)\\
0\\
-\sin(\theta)
\end{bmatrix}
$$

The simulation starts with three dimensional coordinates for my baseplate. Because pygame is a two dimensional environment, we must project these points onto a two dimensional screen. I used the Perspective Projection Equation (formula shown below) where f is focal length and d is camera distance.


$$
2D = \left(\frac{xf}{z+d}, \frac{yf}{z+d}\right)
$$

Though in my code, d is not used and instead the denominator is just z. This is because  I have already subtracted camera position. 

Once we have the projected points, we need to render the points by centering it and multiplying by scale.

$$
\text{Rendered} =
\left(
x_{\text{2D}}\cdot s+\frac{\text{W}}{2},
\quad
y_{\text{2D}}\cdot s+\frac{\text{H}}{2}
\right)
$$

Next, we use Near Plane Clipping to prevent geometry that is too close to or behind the camera from being projected. Without it, points with a camera-space z-coordinate of zero cause division by zero, while negative z-coordinates can produce inverted geometry. I calculated the intersection points using Linear Interpolation.


$$
P=A+t(B-A)
$$

$$
t=\frac{z_{\text{near}}-z_A}{z_B-z_A}
$$

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
| Up Arrow | Rotate camera up |
| Down Arrow | Rotate camera down |
| W | Move camera forward |
| A | Move camera left |
| S | Move camera backward |
| D | Move camera right |
| E | Move camera up |
| Q | Move camera down |
