import pygame


# Currently there are only 5 buildings
# All object_mask data is pre-calculated
def update_object_mask(object_mask, rel_x, rel_y, bgWidth , bgHeight,
                       obj_1=True, obj_2=True, obj_3=True, obj_4=True, obj_5=True, traffic=True):

    if obj_1 is True:
        # --- RECT 1 ----
        p1 = None
        p2 = None
        if 0 <= rel_y <= 1261:
            if 1975 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x)
            else:
                rel_x_copy = rel_x
            if 0 <= rel_y <= 200:
                rel_y_copy = rel_y + 100
            else:
                rel_y_copy = rel_y - 1000
            p1 = (rel_x_copy, rel_y_copy)

        if 1200 <= rel_y <= 1261:
            if 1975 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x)
            else:
                rel_x_copy = rel_x
            rel_y_copy = rel_y % 100
            p2 = (rel_x_copy, rel_y_copy)

        if 0 <= rel_y <= 700:
            if 1975 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x)
            else:
                rel_x_copy = rel_x
            rel_y_copy = rel_y
            p2 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            p1_building_rect = pygame.Rect(p1, (500, 880))
        if p2 is not None:
            p2_building_rect = pygame.Rect(p2, (500, 360))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p1_building_rect)
        if p2 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p2_building_rect)
        # --- RECT 1 ---

    if obj_2 is True:
        # --- RECT 2 ---
        p1 = None
        p2 = None
        x_offset_value = 590
        if 0 <= rel_y <= 1261:
            if 1370 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            if 0 <= rel_y <= 200:
                rel_y_copy = rel_y + 100
            else:
                rel_y_copy = rel_y - 1000
            p1 = (rel_x_copy, rel_y_copy)

        if 1200 <= rel_y <= 1261:
            if 1370 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y % 100
            p2 = (rel_x_copy, rel_y_copy)

        if 0 <= rel_y <= 700:
            if 1370 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y
            p2 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            p1_building_rect = pygame.Rect(p1, (540, 880))
        if p2 is not None:
            p2_building_rect = pygame.Rect(p2, (540, 360))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p1_building_rect)
        if p2 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p2_building_rect)
        # --- RECT 2 ---

    if obj_3 is True:
        # --- RECT 3 ---
        p1 = None
        p2 = None
        x_offset_value = 1225
        if 0 <= rel_y <= 1261:
            if 775 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            if 0 <= rel_y <= 200:
                rel_y_copy = rel_y + 100
            else:
                rel_y_copy = rel_y - 1000
            p1 = (rel_x_copy, rel_y_copy)

        if 1200 <= rel_y <= 1261:
            if 775 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y % 100
            p2 = (rel_x_copy, rel_y_copy)

        if 0 <= rel_y <= 700:
            if 775 <= rel_x <= 2500:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y
            p2 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            p1_building_rect = pygame.Rect(p1, (500, 880))
        if p2 is not None:
            p2_building_rect = pygame.Rect(p2, (500, 360))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p1_building_rect)
        if p2 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p2_building_rect)
        # --- RECT 3 ---

    if obj_4 is True:
        # --- RECT 4 ---
        p1 = None
        p2 = None
        x_offset_value = 1825
        if 0 <= rel_y <= 1261:
            if 0 <= rel_x <= 1960:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            if 0 <= rel_y <= 200:
                rel_y_copy = rel_y + 100
            else:
                rel_y_copy = rel_y - 1000
            p1 = (rel_x_copy, rel_y_copy)

        if 1200 <= rel_y <= 1261:
            if 0 <= rel_x <= 1960:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y % 100
            p2 = (rel_x_copy, rel_y_copy)

        if 0 <= rel_y <= 700:
            if 0 <= rel_x <= 1960:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y
            p2 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            p1_building_rect = pygame.Rect(p1, (400, 880))
        if p2 is not None:
            p2_building_rect = pygame.Rect(p2, (400, 360))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p1_building_rect)
        if p2 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p2_building_rect)
        # --- RECT 4 ---

    if obj_5 is True:
        # --- RECT 5 ---
        p1 = None
        p2 = None
        x_offset_value = 2300
        if 0 <= rel_y <= 1261:
            if 0 <= rel_x <= 1490:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            if 0 <= rel_y <= 200:
                rel_y_copy = rel_y + 100
            else:
                rel_y_copy = rel_y - 1000
            p1 = (rel_x_copy, rel_y_copy)

        if 1200 <= rel_y <= 1261:
            if 0 <= rel_x <= 1490:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y % 100
            p2 = (rel_x_copy, rel_y_copy)

        if 0 <= rel_y <= 700:
            if 0 <= rel_x <= 1490:
                rel_x_copy = -(bgWidth - rel_x) + x_offset_value
            else:
                rel_x_copy = rel_x + x_offset_value
            rel_y_copy = rel_y
            p2 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            p1_building_rect = pygame.Rect(p1, (200, 880))
        if p2 is not None:
            p2_building_rect = pygame.Rect(p2, (200, 360))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p1_building_rect)
        if p2 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), p2_building_rect)
        # --- RECT 5 ---

    if traffic is True:
        # CAR 1
        p1 = None
        if 0 <= rel_x <= 150:
            rel_x_copy = rel_x + 500
            if 0 <= rel_y <= 500:
                rel_y_copy = rel_y + 90
                found = True
            elif 830 <= rel_y <= 1261:
                rel_y_copy = -(bgHeight - rel_y) + 90
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (30, 490))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR 2
        p1 = None
        if 0 <= rel_x <= 150:
            rel_x_copy = rel_x + 500
            if 415 <= rel_y <= 1100:
                rel_y_copy = -(bgHeight - rel_y) + 765
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (20, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR 3
        p1 = None
        if 0 <= rel_x <= 150:
            rel_x_copy = rel_x + 500
            if 415 <= rel_y <= 1100:
                rel_y_copy = -(bgHeight - rel_y) + 875
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (20, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR 4
        p1 = None
        if 0 <= rel_x <= 150:
            rel_x_copy = rel_x + 500
            if 415 <= rel_y <= 1100:
                rel_y_copy = -(bgHeight - rel_y) + 875
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (20, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR 5
        p1 = None
        if 0 <= rel_x <= 150:
            rel_x_copy = rel_x + 500
            if 415 <= rel_y <= 1100:
                rel_y_copy = -(bgHeight - rel_y) + 950
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (20, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR 6
        p1 = None
        if 350 <= rel_y <= 500:
            rel_y_copy = rel_y - 50
            if 0 <= rel_x <= 700:
                rel_x_copy = rel_x + 110
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (260, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR 7 - BLUE
        p1 = None
        if 350 <= rel_y <= 500:
            rel_y_copy = rel_y - 50
            if 300 <= rel_x <= 1210:
                rel_x_copy = rel_x - 310
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (365, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (0, 0, 255), car_rect)

        # CAR 8
        p1 = None
        if 350 <= rel_y <= 500:
            rel_y_copy = rel_y - 50
            if 660 <= rel_x <= 1425:
                rel_x_copy = rel_x - 590
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (230, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_9
        p1 = None
        if 350 <= rel_y <= 500:
            rel_y_copy = rel_y - 50
            if 1300 <= rel_x <= 2000:
                rel_x_copy = rel_x - 1180
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (285, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_10
        p1 = None
        if 350 <= rel_y <= 500:
            rel_y_copy = rel_y - 50
            if 1850 <= rel_x <= 2430:
                rel_x_copy = rel_x - 1550
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (100, 50))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_11
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1370
            if 375 <= rel_y <= 1130:
                rel_y_copy = rel_y - 570
                found = True
            elif 830 <= rel_y <= 1261:
                rel_y_copy = -(bgHeight - rel_y) + 690
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (30, 400))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_12
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1310
            if 375 <= rel_y <= 1130:
                rel_y_copy = rel_y - 410
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)
        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 230))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_13
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1310
            if 375 <= rel_y <= 1261:
                rel_y_copy = rel_y - 690
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 250))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_14
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1370
            if 780 <= rel_y <= 1261:
                rel_y_copy = rel_y - 790
                found = True
            elif 0 <= rel_y <= 100:
                rel_y_copy = rel_y + 470
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (30, 160))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_15
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1310
            if 780 <= rel_y <= 1261:
                rel_y_copy = rel_y - 738
                found = True
            elif 0 <= rel_y <= 100:
                rel_y_copy = rel_y + 522
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 40))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 0, 0), car_rect)

        # CAR_16
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1370
            if 970 <= rel_y <= 1261:
                rel_y_copy = rel_y - 920
                found = True
            elif 0 <= rel_y <= 210:
                rel_y_copy = rel_y + 340
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 100))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_17
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1310
            if 970 <= rel_y <= 1261:
                rel_y_copy = rel_y - 1030
                found = True
            elif 0 <= rel_y <= 300:
                rel_y_copy = rel_y + 235
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 270))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_18
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1370
            if 1100 <= rel_y <= 1261:
                rel_y_copy = rel_y - 1064
                found = True
            elif 0 <= rel_y <= 400:
                rel_y_copy = rel_y + 194
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 64))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)

        # CAR_19
        p1 = None
        if 1900 <= rel_x <= 2000:
            rel_x_copy = rel_x - 1310
            if 1100 <= rel_y <= 1261:
                rel_y_copy = rel_y - 1118
                found = True
            elif 0 <= rel_y <= 400:
                rel_y_copy = rel_y + 140
                found = True
            else:
                found = False

            if found is not False:
                p1 = (rel_x_copy, rel_y_copy)

        if p1 is not None:
            car_rect = pygame.Rect(p1, (35, 74))

        if p1 is not None:
            pygame.draw.rect(object_mask, (255, 255, 0), car_rect)



