import pygame
import numpy as np
from math import *
import random


r,g,b = 236,202,117
# #for random color background
#r,g,b = random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)


COLOR = (r,g,b)
# print(COLOR)
DOT_COLOR =(255,0,0)
BLACK = (0,0,0)
WIDTH , HEIGHT = 1920,1080



pygame.display.set_caption("3d_Projection in Pygame" )
screen = pygame.display.set_mode((WIDTH,HEIGHT))

scale = 144
circle_pos = [WIDTH/2, HEIGHT/2]
angle = 0
fps = 120

points = []

points.append(np.matrix([-1,-1,1]))
points.append(np.matrix([1,-1,1]))
points.append(np.matrix([1,1,1]))
points.append(np.matrix([-1,1,1]))
points.append(np.matrix([-1,-1,-1]))
points.append(np.matrix([1,-1,-1]))
points.append(np.matrix([1,1,-1]))
points.append(np.matrix([-1,1,-1]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points =[
    [n, n] for n in range(len(points))
]


def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

clock = pygame.time.Clock()
while True:

    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    
    #updating stuff

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ]) 

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])


    angle += 0.01
    screen.fill(COLOR)
    

    #drawing stuff
    i = 0 
    for point in points:
        rotated_2d = np.dot(rotation_z, point.reshape(3,1))
        rotated_2d = np.dot(rotation_y, rotated_2d)
        # rotated_2d = np.dot(rotation_x,rotated_2d)

        projected_2d = np.dot(projection_matrix, rotated_2d)

        x = int(projected_2d[0] * scale) + circle_pos[0]
        y = int(projected_2d[1] * scale) + circle_pos[1]

        projected_points[i] =[x,y]
        pygame.draw.circle(screen, DOT_COLOR, (x, y), 10)
        i += 1
        # print(projected_2d )
   
    # connect_points(0, 1, projected_points)
    # connect_points(1, 2, projected_points)
    # connect_points(2, 3, projected_points)
    # connect_points(3, 0, projected_points)

    # connect_points(4, 5, projected_points)
    # connect_points(5, 6, projected_points)
    # connect_points(6, 7, projected_points)
    # connect_points(7, 4, projected_points)

    # connect_points(0, 4, projected_points)
    # connect_points(1, 5, projected_points)
    # connect_points(2, 6, projected_points)
    # connect_points(3, 7, projected_points)

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)
    pygame.display.update()
