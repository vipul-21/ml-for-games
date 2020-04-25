import random
import torch
from utils import *

class Environment():
    def __init__(self, ghost_posititon, ghost_resources, ghostbuster_positions, ghostbuster_resources):
        # print(ghost_posititon)
        # start_state = [165, 5, [34, 29, 117, 174, 112], [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]], 1]

        WALK = 'WALK'
        SEWAGE = 'SEWAGE'
        TUNNEL = 'TUNNEL'
        BLACK = 'BLACK'
        self.board = (((8, (WALK,)), (9, (WALK,)), (58, (SEWAGE,)), (46, (SEWAGE, TUNNEL))),
                      # locToRoutes[0] has no value; need to access locToRoutes[1] and higher
                      ((8, (WALK,)), (9, (WALK,)), (58, (SEWAGE,)), (46, (SEWAGE, TUNNEL))),  # 001
                      ((20, (WALK,)), (10, (WALK,))),
                      ((11, (WALK,)), (12, (WALK,)), (4, (WALK,)), (22, (SEWAGE,)), (23, (SEWAGE,))),
                      ((3, (WALK,)), (13, (WALK,))),
                      ((15, (WALK,)), (16, (WALK,))),  # 005
                      ((29, (WALK,)), (7, (WALK,))),
                      ((6, (WALK,)), (17, (WALK,)), (42, (SEWAGE,))),
                      ((1, (WALK,)), (19, (WALK,)), (18, (WALK,))),
                      ((1, (WALK,)), (19, (WALK,)), (20, (WALK,))),
                      ((2, (WALK,)), (11, (WALK,)), (34, (WALK,)), (21, (WALK,))),  # 010
                      ((3, (WALK,)), (10, (WALK,)), (22, (WALK,))),
                      ((3, (WALK,)), (23, (WALK,))),
                      ((4, (WALK,)), (14, (WALK, SEWAGE)), (24, (WALK,)), (23, (WALK, SEWAGE)), (52, (SEWAGE,)),
                       (89, (TUNNEL,)), (67, (TUNNEL,)), (46, (TUNNEL,))),
                      ((13, (WALK, SEWAGE)), (15, (WALK, SEWAGE)), (25, (WALK,))),
                      ((5, (WALK,)), (16, (WALK,)), (28, (WALK,)), (26, (WALK,)), (14, (WALK, SEWAGE)),
                       (29, (SEWAGE,)), (41, (SEWAGE,))),  # 015
                      ((5, (WALK,)), (29, (WALK,)), (28, (WALK,)), (15, (WALK,))),
                      ((7, (WALK,)), (30, (WALK,)), (29, (WALK,))),
                      ((8, (WALK,)), (31, (WALK,)), (43, (WALK,))),
                      ((8, (WALK,)), (9, (WALK,)), (32, (WALK,))),
                      ((2, (WALK,)), (9, (WALK,)), (33, (WALK,))),  # 020
                      ((10, (WALK,)), (33, (WALK,))),
                      ((11, (WALK,)), (23, (WALK, SEWAGE)), (35, (WALK,)), (34, (WALK, SEWAGE)),
                       (3, (SEWAGE,)), (65, (SEWAGE,))),
                      ((12, (WALK,)), (13, (WALK, SEWAGE)), (37, (WALK,)), (22, (WALK, SEWAGE)),
                       (3, (SEWAGE,)), (67, (SEWAGE,))),
                      ((13, (WALK,)), (38, (WALK,)), (37, (WALK,))),
                      ((14, (WALK,)), (39, (WALK,)), (38, (WALK,))),  # 025
                      ((15, (WALK,)), (27, (WALK,)), (39, (WALK,))),
                      ((26, (WALK,)), (28, (WALK,)), (40, (WALK,))),
                      ((15, (WALK,)), (16, (WALK,)), (41, (WALK,)), (27, (WALK,))),
                      ((6, (WALK,)), (17, (WALK,)), (42, (WALK, SEWAGE)), (41, (WALK, SEWAGE)), (16, (WALK,)),
                       (55, (SEWAGE,)), (15, (SEWAGE,))),
                      ((17, (WALK,)), (42, (WALK,))),  # 030
                      ((18, (WALK,)), (44, (WALK,)), (43, (WALK,))),
                      ((19, (WALK,)), (33, (WALK,)), (45, (WALK,)), (44, (WALK,))),
                      ((20, (WALK,)), (21, (WALK,)), (46, (WALK,)), (32, (WALK,))),
                      ((10, (WALK,)), (22, (WALK, SEWAGE)), (48, (WALK,)), (47, (WALK,)), (63, (SEWAGE,)),
                       (46, (SEWAGE,))),
                      ((22, (WALK,)), (36, (WALK,)), (65, (WALK,)), (48, (WALK,))),  # 035
                      ((37, (WALK,)), (49, (WALK,)), (35, (WALK,))),
                      ((23, (WALK,)), (24, (WALK,)), (50, (WALK,)), (36, (WALK,))),
                      ((24, (WALK,)), (25, (WALK,)), (51, (WALK,)), (50, (WALK,))),
                      ((26, (WALK,)), (52, (WALK,)), (51, (WALK,)), (25, (WALK,))),
                      ((27, (WALK,)), (41, (WALK,)), (53, (WALK,)), (52, (WALK,))),  # 040
                      ((28, (WALK,)), (29, (WALK, SEWAGE)), (54, (WALK,)), (40, (WALK,)),
                       (15, (SEWAGE,)), (87, (SEWAGE,)), (52, (SEWAGE,))),
                      ((30, (WALK,)), (56, (WALK,)), (72, (WALK, SEWAGE)), (29, (WALK, SEWAGE)),
                       (7, (SEWAGE,))),
                      ((18, (WALK,)), (31, (WALK,)), (57, (WALK,))),
                      ((32, (WALK,)), (58, (WALK,)), (31, (WALK,))),
                      ((32, (WALK,)), (46, (WALK,)), (60, (WALK,)), (59, (WALK,)),  # 045
                       (58, (WALK,))),
                      ((33, (WALK,)), (47, (WALK,)), (61, (WALK,)), (45, (WALK,)), (34, (SEWAGE,)),
                       (78, (SEWAGE,)), (58, (SEWAGE,)), (1, (SEWAGE, TUNNEL)), (13, (TUNNEL,)),
                       (79, (TUNNEL,)), (74, (TUNNEL,))),
                      ((34, (WALK,)), (62, (WALK,)), (46, (WALK,))),
                      ((34, (WALK,)), (35, (WALK,)), (63, (WALK,)), (62, (WALK,))),
                      ((36, (WALK,)), (50, (WALK,)), (66, (WALK,))),
                      ((37, (WALK,)), (38, (WALK,)), (49, (WALK,))),  # 050
                      ((38, (WALK,)), (39, (WALK,)), (52, (WALK,)), (68, (WALK,)), (67, (WALK,))),
                      ((39, (WALK,)), (40, (WALK,)), (69, (WALK,)), (51, (WALK,)), (13, (SEWAGE,)),
                       (41, (SEWAGE,)), (86, (SEWAGE,)), (67, (SEWAGE,))),
                      ((40, (WALK,)), (54, (WALK,)), (69, (WALK,))),
                      ((41, (WALK,)), (55, (WALK,)), (70, (WALK,)), (53, (WALK,))),
                      ((71, (WALK,)), (54, (WALK,)), (29, (SEWAGE,)), (89, (SEWAGE,))),  # 055
                      ((42, (WALK,)), (91, (WALK,))),
                      ((43, (WALK,)), (58, (WALK,)), (73, (WALK,))),
                      ((45, (WALK,)), (59, (WALK,)), (75, (WALK,)), (74, (WALK, SEWAGE)), (57, (WALK,)),
                       (44, (WALK,)), (46, (SEWAGE,)), (77, (SEWAGE,)), (1, (SEWAGE,))),
                      ((45, (WALK,)), (76, (WALK,)), (75, (WALK,)), (58, (WALK,))),
                      ((45, (WALK,)), (61, (WALK,)), (76, (WALK,))),  # 060
                      ((46, (WALK,)), (62, (WALK,)), (78, (WALK,)), (76, (WALK,)), (60, (WALK,))),
                      ((47, (WALK,)), (48, (WALK,)), (79, (WALK,)), (61, (WALK,))),
                      ((48, (WALK,)), (64, (WALK,)), (80, (WALK,)), (79, (WALK, SEWAGE)),
                       (34, (SEWAGE,)), (65, (SEWAGE,)), (100, (SEWAGE,))),
                      ((65, (WALK,)), (81, (WALK,)), (63, (WALK,))),
                      ((35, (WALK,)), (66, (WALK,)), (82, (WALK, SEWAGE)), (64, (WALK,)),  # 065
                       (22, (SEWAGE,)), (67, (SEWAGE,)), (63, (SEWAGE,))),
                      ((49, (WALK,)), (67, (WALK,)), (82, (WALK,)), (65, (WALK,))),
                      ((51, (WALK,)), (68, (WALK,)), (84, (WALK,)), (66, (WALK,)), (23, (SEWAGE,)),
                       (52, (SEWAGE,)), (102, (SEWAGE,)), (82, (SEWAGE,)), (65, (SEWAGE,)),
                       (13, (TUNNEL,)), (89, (TUNNEL,)), (111, (TUNNEL,)),
                       (79, (TUNNEL,))),
                      ((51, (WALK,)), (69, (WALK,)), (85, (WALK,)), (67, (WALK,))),
                      ((52, (WALK,)), (53, (WALK,)), (86, (WALK,)), (68, (WALK,))),
                      ((54, (WALK,)), (71, (WALK,)), (87, (WALK,))),  # 070
                      ((55, (WALK,)), (72, (WALK,)), (89, (WALK,)), (70, (WALK,))),
                      ((42, (WALK, SEWAGE)), (91, (WALK,)), (90, (WALK,)), (71, (WALK,)),
                       (107, (SEWAGE,)), (105, (SEWAGE,))),
                      ((57, (WALK,)), (74, (WALK,)), (92, (WALK,))),
                      ((58, (WALK, SEWAGE)), (75, (WALK,)), (92, (WALK,)), (73, (WALK,)),
                       (94, (SEWAGE,)), (46, (TUNNEL,))),
                      ((58, (WALK,)), (59, (WALK,)), (94, (WALK,)), (74, (WALK,))),  # 075
                      ((59, (WALK,)), (60, (WALK,)), (61, (WALK,)), (77, (WALK,))),
                      ((78, (WALK, SEWAGE)), (96, (WALK,)), (95, (WALK,)), (76, (WALK,)),
                       (124, (SEWAGE,)), (94, (SEWAGE,)), (58, (SEWAGE,))),
                      ((61, (WALK,)), (79, (WALK, SEWAGE)), (97, (WALK,)), (77, (WALK, SEWAGE)),
                       (46, (SEWAGE,))),
                      ((62, (WALK,)), (63, (WALK, SEWAGE)), (98, (WALK,)), (78, (WALK, SEWAGE)),
                       (46, (TUNNEL,)), (67, (TUNNEL,)), (111, (TUNNEL,)),
                       (93, (TUNNEL,))),
                      ((63, (WALK,)), (100, (WALK,)), (99, (WALK,))),  # 080
                      ((64, (WALK,)), (82, (WALK,)), (100, (WALK,))),
                      ((65, (WALK, SEWAGE)), (66, (WALK,)), (67, (SEWAGE,)), (101, (WALK,)), (140, (SEWAGE,)),
                       (81, (WALK,)), (100, (SEWAGE,))),
                      ((102, (WALK,)), (101, (WALK,))),
                      ((67, (WALK,)), (85, (WALK,))),
                      ((68, (WALK,)), (103, (WALK,)), (84, (WALK,))),  # 085
                      ((69, (WALK,)), (52, (SEWAGE,)), (87, (SEWAGE,)), (104, (WALK,)), (116, (SEWAGE,)),
                       (103, (WALK,)), (102, (SEWAGE,))),
                      ((70, (WALK,)), (41, (SEWAGE,)), (88, (WALK,)), (105, (SEWAGE,)), (86, (SEWAGE,))),
                      ((89, (WALK,)), (117, (WALK,)), (87, (WALK,))),
                      ((71, (WALK,)), (55, (SEWAGE,)), (13, (TUNNEL,)), (105, (WALK, SEWAGE)),
                       (128, (TUNNEL,)), (88, (WALK,)), (140, (TUNNEL,)),
                       (67, (TUNNEL,))),
                      ((72, (WALK,)), (91, (WALK,)), (105, (WALK,))),  # 090
                      ((56, (WALK,)), (107, (WALK,)), (105, (WALK,)), (90, (WALK,)), (72, (WALK,))),
                      ((73, (WALK,)), (74, (WALK,)), (93, (WALK,))),
                      ((92, (WALK,)), (94, (WALK, SEWAGE)), (79, (TUNNEL,))),
                      ((74, (SEWAGE,)), (75, (WALK,)), (95, (WALK,)), (77, (SEWAGE,)), (93, (WALK, SEWAGE))),
                      ((77, (WALK,)), (122, (WALK,)), (94, (WALK,))),  # 095
                      ((77, (WALK,)), (97, (WALK,)), (109, (WALK,))),
                      ((78, (WALK,)), (98, (WALK,)), (109, (WALK,)), (96, (WALK,))),
                      ((79, (WALK,)), (99, (WALK,)), (110, (WALK,)), (97, (WALK,))),
                      ((80, (WALK,)), (112, (WALK,)), (110, (WALK,)), (98, (WALK,))),
                      ((81, (WALK,)), (82, (SEWAGE,)), (101, (WALK,)), (113, (WALK,)),  # 100
                       (112, (WALK,)), (111, (SEWAGE,)), (80, (WALK,)), (63, (SEWAGE,))),
                      ((83, (WALK,)), (114, (WALK,)), (100, (WALK,)), (82, (WALK,))),
                      ((67, (SEWAGE,)), (103, (WALK,)), (86, (SEWAGE,)), (115, (WALK,)), (127, (SEWAGE,)),
                       (83, (WALK,))),
                      ((85, (WALK,)), (86, (WALK,)), (102, (WALK,))),
                      ((86, (WALK,)), (116, (WALK,))),
                      ((90, (WALK,)), (72, (SEWAGE,)), (91, (WALK,)), (106, (WALK,)),  # 105
                       (107, (SEWAGE,)), (108, (WALK, SEWAGE)), (87, (SEWAGE,)), (89, (WALK, SEWAGE))),
                      ((107, (WALK,)), (105, (WALK,))),
                      ((91, (WALK,)), (72, (SEWAGE,)), (119, (WALK,)), (161, (SEWAGE,)),
                       (106, (WALK,)), (105, (SEWAGE,))),
                      ((105, (WALK, SEWAGE)), (119, (WALK,)), (135, (SEWAGE,)), (117, (WALK,)),
                       (116, (SEWAGE,)), (115, (BLACK,))),
                      ((97, (WALK,)), (110, (WALK,)), (124, (WALK,)), (96, (WALK,))),
                      ((99, (WALK,)), (111, (WALK,)), (109, (WALK,)), (98, (WALK,))),  # 110
                      ((112, (WALK,)), (100, (SEWAGE,)), (67, (TUNNEL,)),
                       (153, (TUNNEL,)), (124, (WALK, SEWAGE)), (163, (TUNNEL,)),
                       (110, (WALK,)), (79, (TUNNEL,))),
                      ((100, (WALK,)), (125, (WALK,)), (111, (WALK,)), (99, (WALK,))),
                      ((114, (WALK,)), (125, (WALK,)), (100, (WALK,))),
                      ((101, (WALK,)), (115, (WALK,)), (126, (WALK,)),
                       (132, (WALK,)), (131, (WALK,)), (113, (WALK,))),
                      ((102, (WALK,)), (127, (WALK,)), (126, (WALK,)), (114, (WALK,)),  # 115
                       (108, (BLACK,)), (157, (BLACK,))),
                      ((104, (WALK,)), (86, (SEWAGE,)), (117, (WALK,)), (108, (SEWAGE,)),
                       (118, (WALK,)), (142, (SEWAGE,)), (127, (WALK, SEWAGE))),
                      ((88, (WALK,)), (108, (WALK,)), (129, (WALK,)), (116, (WALK,))),
                      ((116, (WALK,)), (129, (WALK,)), (142, (WALK,)), (134, (WALK,))),
                      ((107, (WALK,)), (136, (WALK,)), (108, (WALK,))),
                      ((121, (WALK,)), (144, (WALK,))),  # 120
                      ((122, (WALK,)), (145, (WALK,)), (120, (WALK,))),
                      ((95, (WALK,)), (123, (WALK, SEWAGE)), (146, (WALK,)),
                       (121, (WALK,)), (144, (SEWAGE,))),
                      ((124, (WALK, SEWAGE)), (149, (WALK,)), (165, (SEWAGE,)), (148, (WALK,)),
                       (137, (WALK,)), (144, (SEWAGE,)), (122, (WALK, SEWAGE))),
                      ((109, (WALK,)), (111, (WALK, SEWAGE)), (130, (WALK,)), (138, (WALK,)),
                       (153, (SEWAGE,)), (123, (WALK, SEWAGE)), (77, (SEWAGE,))),
                      ((113, (WALK,)), (131, (WALK,)), (112, (WALK,))),  # 125
                      ((115, (WALK,)), (127, (WALK,)), (140, (WALK,)), (114, (WALK,))),
                      ((116, (WALK, SEWAGE)), (134, (WALK,)), (133, (WALK, SEWAGE)),
                       (126, (WALK,)), (115, (WALK,)), (102, (SEWAGE,))),
                      ((143, (WALK,)), (135, (SEWAGE,)), (89, (TUNNEL,)), (160, (WALK,)),
                       (161, (SEWAGE,)), (188, (WALK,)), (199, (SEWAGE,)), (172, (WALK,)),
                       (187, (SEWAGE,)), (185, (TUNNEL,)), (142, (WALK, SEWAGE)),
                       (140, (TUNNEL,))),
                      ((117, (WALK,)), (135, (WALK,)), (143, (WALK,)), (142, (WALK,)),
                       (118, (WALK,))),
                      ((131, (WALK,)), (139, (WALK,)), (124, (WALK,))),  # 130
                      ((114, (WALK,)), (130, (WALK,)), (125, (WALK,))),
                      ((114, (WALK,)), (140, (WALK,))),
                      ((127, (WALK, SEWAGE)), (141, (WALK,)), (157, (SEWAGE,)), (140, (WALK, SEWAGE))),
                      ((118, (WALK,)), (142, (WALK,)), (141, (WALK,)), (127, (WALK,))),
                      ((108, (SEWAGE,)), (136, (WALK,)), (161, (WALK, SEWAGE)), (143, (WALK,)),  # 135
                       (128, (SEWAGE,)), (129, (WALK,))),
                      ((119, (WALK,)), (162, (WALK,)), (135, (WALK,))),
                      ((123, (WALK,)), (147, (WALK,))),
                      ((152, (WALK,)), (150, (WALK,)), (124, (WALK,))),
                      ((130, (WALK,)), (140, (WALK,)), (154, (WALK,)), (153, (WALK,))),
                      ((132, (WALK,)), (82, (SEWAGE,)), (126, (WALK,)), (89, (TUNNEL,)),  # 140
                       (133, (WALK, SEWAGE)), (128, (TUNNEL,)), (156, (WALK, SEWAGE)),
                       (154, (WALK, SEWAGE)), (153, (TUNNEL,)), (139, (WALK,))),
                      ((134, (WALK,)), (142, (WALK,)), (158, (WALK,)), (133, (WALK,))),
                      ((118, (WALK,)), (116, (SEWAGE,)), (129, (WALK,)), (143, (WALK,)),
                       (128, (WALK, SEWAGE)), (158, (WALK,)), (157, (SEWAGE,)), (141, (WALK,)),
                       (134, (WALK,))),
                      ((135, (WALK,)), (160, (WALK,)), (128, (WALK,)), (142, (WALK,)),
                       (129, (WALK,))),
                      ((120, (WALK,)), (122, (SEWAGE,)), (145, (WALK,)), (123, (SEWAGE,)),
                       (163, (SEWAGE,)), (177, (WALK,))),
                      ((121, (WALK,)), (146, (WALK,)), (144, (WALK,))),  # 145
                      ((122, (WALK,)), (147, (WALK,)), (163, (WALK,)), (145, (WALK,))),
                      ((137, (WALK,)), (164, (WALK,)), (146, (WALK,))),
                      ((123, (WALK,)), (149, (WALK,)), (164, (WALK,))),
                      ((123, (WALK,)), (150, (WALK,)), (165, (WALK,)), (148, (WALK,))),
                      ((138, (WALK,)), (151, (WALK,)), (149, (WALK,))),  # 150
                      ((152, (WALK,)), (166, (WALK,)), (165, (WALK,)), (150, (WALK,))),
                      ((153, (WALK,)), (151, (WALK,)), (138, (WALK,))),
                      ((139, (WALK,)), (111, (TUNNEL,)), (154, (WALK, SEWAGE)),
                       (140, (TUNNEL,)), (167, (WALK,)), (184, (SEWAGE,)),
                       (185, (TUNNEL,)), (166, (WALK,)), (180, (SEWAGE,)),
                       (163, (TUNNEL,)), (152, (WALK,)), (124, (SEWAGE,))),
                      ((140, (WALK, SEWAGE)), (155, (WALK,)), (156, (SEWAGE,)), (153, (WALK, SEWAGE)),
                       (139, (WALK,))),
                      ((156, (WALK,)), (168, (WALK,)), (167, (WALK,)), (154, (WALK,))),  # 155
                      ((140, (WALK, SEWAGE)), (157, (WALK, SEWAGE)), (169, (WALK,)),
                       (184, (SEWAGE,)), (155, (WALK,)), (154, (SEWAGE,))),
                      ((133, (SEWAGE,)), (158, (WALK,)), (142, (SEWAGE,)), (170, (WALK,)),
                       (185, (SEWAGE,)), (156, (WALK, SEWAGE)), (115, (BLACK,)), (194, (BLACK,))),
                      ((141, (WALK,)), (142, (WALK,)), (159, (WALK,)), (157, (WALK,))),
                      ((158, (WALK,)), (172, (WALK,)), (198, (WALK,)), (186, (WALK,)),
                       (170, (WALK,))),
                      ((143, (WALK,)), (161, (WALK,)), (173, (WALK,)), (128, (WALK,))),  # 160
                      ((107, (SEWAGE,)), (174, (WALK,)), (199, (SEWAGE,)), (160, (WALK,)),
                       (128, (SEWAGE,)), (135, (WALK, SEWAGE))),
                      ((175, (WALK,)), (136, (WALK,))),
                      ((146, (WALK,)), (111, (TUNNEL,)), (153, (TUNNEL,)),
                       (191, (SEWAGE,)), (177, (WALK,)), (176, (SEWAGE,)), (144, (SEWAGE,))),
                      ((147, (WALK,)), (148, (WALK,)), (179, (WALK,)), (178, (WALK,))),
                      ((149, (WALK,)), (123, (SEWAGE,)), (151, (WALK,)), (180, (WALK, SEWAGE)),  # 165
                       (179, (WALK,)), (191, (SEWAGE,))),
                      ((153, (WALK,)), (183, (WALK,)), (181, (WALK,)), (151, (WALK,))),
                      ((155, (WALK,)), (168, (WALK,)), (183, (WALK,)), (153, (WALK,))),
                      ((155, (WALK,)), (184, (WALK,)), (167, (WALK,))),
                      ((156, (WALK,)), (184, (WALK,))),
                      ((157, (WALK,)), (159, (WALK,)), (185, (WALK,))),  # 170
                      ((173, (WALK,)), (175, (WALK,)), (199, (WALK,))),
                      ((128, (WALK,)), (187, (WALK,)), (159, (WALK,))),
                      ((160, (WALK,)), (174, (WALK,)), (171, (WALK,)), (188, (WALK,))),
                      ((175, (WALK,)), (173, (WALK,)), (161, (WALK,))),
                      ((162, (WALK,)), (171, (WALK,)), (174, (WALK,))),  # 175
                      ((177, (WALK,)), (163, (SEWAGE,)), (189, (WALK,)), (190, (SEWAGE,))),
                      ((144, (WALK,)), (163, (WALK,)), (176, (WALK,))),
                      ((164, (WALK,)), (191, (WALK,)), (189, (WALK,))),
                      ((165, (WALK,)), (191, (WALK,)), (164, (WALK,))),
                      ((165, (WALK, SEWAGE)), (181, (WALK,)), (153, (SEWAGE,)), (193, (WALK,)),  # 180
                       (184, (SEWAGE,)), (190, (SEWAGE,))),
                      ((166, (WALK,)), (182, (WALK,)), (193, (WALK,)), (180, (WALK,))),
                      ((183, (WALK,)), (195, (WALK,)), (181, (WALK,))),
                      ((167, (WALK,)), (196, (WALK,)), (182, (WALK,)), (166, (WALK,))),
                      ((169, (WALK,)), (156, (SEWAGE,)), (185, (WALK, SEWAGE)), (197, (WALK,)),
                       (196, (WALK,)), (180, (SEWAGE,)), (168, (WALK,)), (153, (SEWAGE,))),
                      ((170, (WALK,)), (157, (SEWAGE,)), (186, (WALK,)), (187, (SEWAGE,)),  # 185
                       (128, (TUNNEL,)), (184, (WALK, SEWAGE)), (153, (TUNNEL,))),
                      ((159, (WALK,)), (198, (WALK,)), (185, (WALK,))),
                      ((172, (WALK,)), (128, (SEWAGE,)), (188, (WALK,)), (198, (WALK,)),
                       (185, (SEWAGE,))),
                      ((128, (WALK,)), (173, (WALK,)), (199, (WALK,)), (187, (WALK,))),
                      ((178, (WALK,)), (190, (WALK,)), (176, (WALK,))),
                      ((191, (WALK, SEWAGE)), (192, (WALK,)), (180, (SEWAGE,)),  # 190
                       (189, (WALK,)), (176, (SEWAGE,))),
                      ((179, (WALK,)), (165, (SEWAGE,)), (192, (WALK,)), (190, (WALK, SEWAGE)),
                       (178, (WALK,)), (163, (SEWAGE,))),
                      ((191, (WALK,)), (194, (WALK,)), (190, (WALK,))),
                      ((181, (WALK,)), (194, (WALK,)), (180, (WALK,))),
                      ((195, (WALK,)), (192, (WALK,)), (193, (WALK,)), (157, (BLACK,))),
                      ((182, (WALK,)), (197, (WALK,)), (194, (WALK,))),  # 195
                      ((183, (WALK,)), (184, (WALK,)), (197, (WALK,))),
                      ((196, (WALK,)), (184, (WALK,)), (195, (WALK,))),
                      ((159, (WALK,)), (187, (WALK,)), (199, (WALK,)), (186, (WALK,))),
                      ((188, (WALK,)), (128, (SEWAGE,)), (171, (WALK,)), (161, (SEWAGE,)),
                       (198, (WALK,)))
                      )

        self.ghost_posititon = ghost_posititon
        self.ghost_posititon_avail = ghost_posititon
        self.ghostbuster_positions = ghostbuster_positions
        self.ghost_resources = 5
        # self.ghostbuster_resources = ghostbuster_resources
        self.ghostbuster_resources = [[10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4], [10, 8, 4]]
        self.done = False
        self.possible_moves = self.get_possible_moves()
        # self.possible_moves = self.board[self.ghost_posititon]


    def get_state(self, round_number):
        # in_state = [self.ghost_posititon, self.ghost_resources, self.ghostbuster_positions, self.ghostbuster_resources, round_number]

        in_state = [self.ghost_posititon, self.ghost_resources, self.ghostbuster_positions, self.ghostbuster_resources,round_number]
        # print("1", in_state)
        state = generate_feature_space(in_state)
        # print("2")
        # print(state)
        return torch.tensor(state), in_state

    def getdistance(self, x, y):
        return abs(int(x) - int(y))

    def num_actions_available(self):
        return len(self.possible_moves)

    def take_action(self, action, timestep, choices):
        # update Mr. X's position to simulate his taking an action
        next_move =  random.choice(self.board[self.ghost_posititon])
        self.ghost_posititon_avail = next_move[0]
        # if timestep  in [3, 8, 12, 18, 24]:
        if timestep  in [3, 8, 12, 18, 24]:
            self.ghost_posititon = next_move[0]

        d = {
            "WALK": 0,
            "SEWAGE": 1,
            "TUNNEL": 2,
            "BLACK": 3
        }
        # print(self.ghostbuster_resources)
        for index, each_detective in enumerate(self.ghostbuster_positions):
            pm = self.board[each_detective]
            new_pm = []
            # for x in pm:
            #     for k in range(0, len(x[1])):
            #         if (x[1][k] != "BLACK"):
            #
            #             if (self.ghostbuster_resources[index][d[x[1][k]]] > 0):
            #                 new_pm.append((x[0], x[1][k]))
            # print("Detective:", index, "moves : ", new_pm, self.ghostbuster_resources[index])

            if (action[index] > 0):
                random_move = action[index]

                # print(random_move)
                if 'WALK' in choices[index]:
                    resource_used = 0

                elif 'SEWAGE' in choices[index]:
                    resource_used = 1

                else:
                    resource_used = 2

                self.ghostbuster_positions[index] = random_move
                self.ghostbuster_resources[index][resource_used] -= 1
        #     self.ghost_posititon_avail = self.ghost_posititon
        # # print(self.ghost_posititon_avail)
        # if self.ghost_posititon_avail is not None:
        #     self.ghostbuster_positions, self.ghostbuster_resources = self.take_action_detectives()
        # else:
        #     self.take_action_detectives_random()


        # self.take_action_detectives_random()
        # detective_position_average = 0
        # for each_detective in self.ghostbuster_positions:
        #   detective_position_average += each_detective
        # detective_position_average = detective_position_average/5

        # reward = self.getdistance(self.ghost_posititon, detective_position_average)
        self.done = self.is_done(timestep)
        if self.done == 1:
            return 100
        elif (self.done == 2):
            return -100
        else:
            return 0

    def get_possible_moves(self):
        new_possible_moves = []
        res_state_loc = []
        res_state_resources = self.ghostbuster_resources
        d = {
            "WALK": 0,
            "SEWAGE": 1,
            "TUNNEL": 2,
            "BLACK": 3
        }
        # print(self.ghostbuster_resources)
        for index, each_detective in enumerate(self.ghostbuster_positions):
            pm = self.board[each_detective]
            new_pm = []
            for x in pm:
                for k in range(0, len(x[1])):
                    if (x[1][k] != "BLACK"):
                        if (self.ghostbuster_resources[index][d[x[1][k]]] > 0):
                            new_pm.append((x[0], x[1][k]))
            new_possible_moves.append(new_pm)
            # print("Detective:", index, "moves : ", new_pm, self.ghostbuster_resources[index])
        return new_possible_moves
        # for count, det in enumerate(self.ghostbuster_positions):
        #     moves = self.board[int(det)]
        #     min_dist_node = -1
        #     min_dist_val = float("inf")
        #
        #     for move in moves:
        #         val = self.getdistance(self.ghost_posititon_avail, move[0])
        #
        #         if (val < min_dist_val):
        #             min_dist_node = move
        #             min_dist_val = val
        #
        #     res_state_loc.append(min_dist_node[0])
        #     # print("COUNT: ", count)
        #     if (min_dist_node[1][0] == 'WALK'):
        #         res_state_resources[count][0] = max(res_state_resources[count][0] - 1, 0)
        #
        #     elif (min_dist_node[1][0] == 'SEWAGE'):
        #         res_state_resources[count][1] = max(res_state_resources[count][1] - 1, 0)
        #     else:
        #         res_state_resources[count][2] = max(res_state_resources[count][2] - 1, 0)
        # return (res_state_loc, res_state_resources)

    def is_done(self, timestep):
        # game ends when either one detective is at the place of Mr. X
        for each_detective in self.ghostbuster_positions:
            if each_detective == self.ghost_posititon_avail:
                return 1
        if (timestep == 24):
            return 2
        return 0

    # returns true is ghost wins
    def winner(self):

        for each_ghostbuster in self.ghostbuster_positions:
            if each_ghostbuster == self.ghost_posititon_avail:
                return False
        return True

    def take_action_against(self, action_ghost, choices_ghost, action_ghostbuster, choices_ghostbuster, timestep):
        # next_move =  random.choice(self.board[self.ghost_posititon])
        # self.ghost_posititon_avail = next_move[0]
        # if timestep  in [3, 8, 12, 18, 24]:
        # if timestep  in [1, 3, 5, 8, 10, 12, 15, 18, 20, 24]:
        self.ghost_posititon = action_ghost
        d = {
            "WALK": 0,
            "SEWAGE": 1,
            "TUNNEL": 2,
            "BLACK": 3
        }
        # print(self.ghostbuster_resources)
        for index, each_detective in enumerate(self.ghostbuster_positions):
            pm = self.board[each_detective]
            new_pm = []
            if (action_ghostbuster[index] > 0):
                random_move = action_ghostbuster[index]
                if 'WALK' in choices_ghostbuster[index]:
                    resource_used = 0

                elif 'SEWAGE' in choices_ghostbuster[index]:
                    resource_used = 1

                else:
                    resource_used = 2

                self.ghostbuster_positions[index] = random_move
                self.ghostbuster_resources[index][resource_used] -= 1

        self.done = self.is_done(timestep)
        if self.done == 1:
            return 100
        elif (self.done == 2):
            return -100
        else:
            return 0
