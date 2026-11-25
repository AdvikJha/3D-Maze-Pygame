# 3D-Maze-Pygame
This is a maze simulation built entirely in python with only pygame and numpy. It is currently a work in progress.

## Features
 - 3D Coordinate System
 - Perspective Projection
 - World-to-Camera Transformation
 - Camera Yaw and Pitch Rotation
 - Near Plane Clipping

## How it works
First, we must edit the coordinates of the baseplate relative to our perspective. In Line 91, I apply the World-to-Camera Transformation formula where $V_{camera}$ is camera_baseplate_vertices, $V_{world}$ is baseplate_points, $C$ is camera_position, $R_y$ is rotation_y, $R_x$ is rotation_x, $\theta$ is camera_yaw, and $\phi$ is camera_pitch. To avoid having people looking too far up or down I set the range to $-\frac{\pi}{2} \leq \phi \leq \frac{\pi}{2}$ For this formula we must use the inverse of $R_y$ because $R_y$ would rotate world relative to the camera so the inverse rotates the camera relative to the world. We can calculate the inverse using the transpose because rotation matrices are orthogonal.

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

The simulation starts with three dimensional coordinates for my baseplate (Line 22). Because pygame is a two dimensional environment, we must project these points onto a two dimensional screen. I used the Perspective Projection Equation (formula shown below) on Line 53 of my code where f is focal length and d is camera distance.


$$
2D = \left(\frac{xf}{z+d}, \frac{yf}{z+d}\right)
$$

Though in my code, d is not used and instead the denominator is just z. This is because on Line 91 I have already subtracted camera position. 

Once we have the projected points, we need to render the points by centering it and multiplying by scale as I did in Lines 96-97.

$$
\text{Rendered} =
\left(
x_{\text{2D}}\cdot s+\frac{\text{W}}{2},
\quad
y_{\text{2D}}\cdot s+\frac{\text{H}}{2}
\right)
$$

## Current Issues

As of now, the camera yaw makes unwanted shapes and patterns at certain angles and when turned fully around, you can see the baseplate upside down. This is because of the Perspective Projection Equation. It works most of the time but when z=0, the coordinates are undefined causing unwanted coordinate behavior and negative z values can cause inverted geometry. This problem will be mostly fixed once I implement Near Plane Clipping in a future commit.

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
