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
# ⚡ Bolt Optimization: Use defaultdict to avoid O(N) grouping in post-processing
body_info_groups = defaultdict(list)

def quit():
    # ⚡ Bolt Optimization: Pass dict directly, avoiding O(N) copy and re-grouping
    postokeyframes.run(body_info_groups,drop_time,FPS)
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
        if global_time == num_of_balls + 200:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                quit()
                running = False

        # ⚡ Bolt Optimization: Replaced O(N) loop with O(1) calculation
        if global_time != 0 and global_time % drop_time == 0:
            i = global_time // drop_time
            if i < num_of_balls:
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

                # Bolt Fix: Initialize cached data on creation
                ball_body.bolt_cached_data = (global_time, ball_radius, False)

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

            # Bolt Fix: Initialize cached data on creation
            cube_body.bolt_cached_data = (global_time, size, True)


        dt = 1.0 / FPS
        space.step(dt)


        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(FPS*10)


        for i, body in enumerate(space.bodies):
            try:
                dropped, size_val, is_poly = body.bolt_cached_data
            except AttributeError:
                # Fallback: attempt to calculate properties if cache is missing.
                # 'dropped' time is unrecoverable, default to 0.
                dropped = 0
                is_poly = False
                size_val = 10 # Default size

                # Attempt to guess type from shapes (if any)
                if len(body.shapes) > 0:
                    shape = list(body.shapes)[0] # pymunk bodies maintain a set of shapes
                    if isinstance(shape, pymunk.Poly):
                        is_poly = True
                        size_val = 80 # Default for poly (player_size)
                    elif isinstance(shape, pymunk.Circle):
                        is_poly = False
                        size_val = shape.radius

                body.bolt_cached_data = (dropped, size_val, is_poly)

            # ⚡ Bolt Optimization: Group by ID (i+5000) immediately
            body_info_groups[i+5000].append([
                i+5000,
                round((body.position[0]/40)*15,2),
                round((body.position[1]/40)*15,2),
                dropped,
                round(body.angle,2),
                size_val,
                is_poly
            ])

    pygame.quit()



if __name__ == "__main__":
    main()
