import pymunk
import pygame
import pymunk.pygame_util
import random
import NeditGD
from collections import defaultdict
import postokeyframes
import math

random.seed(14) #<---- some seeds have buggy player position most are fineish tho

player = True

FPS = 25

num_of_balls = 120
global_time = 0
drop_time = 20

player_size = 80

body_list = []
body_map = {}
body_info_list = []

def quit():
    postokeyframes.run(list(body_info_list),drop_time,FPS)
    pygame.quit()

def main():
    global global_time
    pygame.init()


    screen = pygame.display.set_mode((80*19, 80*11))
    pygame.display.set_caption("orbit borbits")
    clock = pygame.time.Clock()


    space = pymunk.Space()
    space.gravity = (0, 900)




    ground_segment = pymunk.Segment(space.static_body, (0, 80*11), (80*19, 80*11), 5)
    ground_segment.elasticity = 0.9
    ground_segment.friction = .7
    space.add(ground_segment)

    ground_segment = pymunk.Segment(space.static_body, (0, 0), (0, 80*11), 5)
    ground_segment.elasticity = 0.9
    space.add(ground_segment)

    ground_segment = pymunk.Segment(space.static_body, (80*19, 0), (80*19, 80*11), 5)
    ground_segment.elasticity = 0.9
    space.add(ground_segment)


    draw_options = pymunk.pygame_util.DrawOptions(screen)

    running = True
    while running:
        global_time += 1
        #print(global_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                quit()
            if global_time == num_of_balls + 200:
                quit()

        # ⚡ Bolt Optimization: Replaced O(N) loop with O(1) calculation
        if global_time != 0 and global_time % drop_time == 0:
            i = global_time // drop_time
            if 0 <= i < num_of_balls:
                ball_mass = 1
                ball_radius = 40 + random.randint(1,20)
                ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
                ball_body = pymunk.Body(ball_mass, ball_moment)
                ball_body.position = ((600/num_of_balls)*random.randint(1,num_of_balls*2), -250)  # Starting position
                ball_shape = pymunk.Circle(ball_body, ball_radius)
                ball_shape.elasticity = 0.5
                ball_shape.friction = 1
                space.add(ball_body, ball_shape)
                ball_body.apply_impulse_at_local_point(pymunk.Vec2d(10-random.randint(0,20), 0), (0, 0))

        if global_time == (50)*drop_time and player:
            cube_mass = 1
            size = player_size
            cube_moment = pymunk.moment_for_box(cube_mass, (size,size))
            cube_body = pymunk.Body(cube_mass, cube_moment)
            cube_body.position = (600,-400)
            cube_shape = pymunk.Poly.create_box(cube_body,(size,size))
            cube_shape.friction = 0.7
            cube_shape.elasticity = 0.5
            space.add(cube_body,cube_shape)



        dt = 1.0 / FPS
        space.step(dt)


        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(FPS*10)


        for i, body in enumerate(space.bodies):
            if body.id not in body_map:
                body_map[body.id] = len(body_list)
                body_list.append(body.id)
            dropped = (body_map[body.id]+1)*drop_time

            shape = next(iter(body.shapes))
            if isinstance(shape,pymunk.Circle):
                radius = shape.radius

                body_info_list.append([i+5000,round((body.position[0]/40)*15,2),round((body.position[1]/40)*15,2),dropped,round(body.angle,2),radius/(40*2)*30,False])# w clean code
            else:
                size = 50

                body_info_list.append([i+5000,round((body.position[0]/40)*15,2),round((body.position[1]/40)*15,2),dropped,round(body.angle,2),size/(40*2)*30,True])

    pygame.quit()



if __name__ == "__main__":
    main()
