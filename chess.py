import pygame
import data
import sys
import threading

class Chess():
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()
        self.color_black = (120,77,50)
        self.color_white = (251,242,227)
        self.player1 = "black"
        self.player2 = "white"
        self.player_turn = self.player2
        self.level = 3
        self.game_status = "main_menu"
        self.play_against = "cpu"
        self.active_for_process = True
        self.animation_no = 0
        self.click_sound = pygame.mixer.Sound("click.wav")
        self.white_queen_moved_status = False
        self.black_queen_moved_status = False

        # For checked
        self.total_move = 0
        self.draw_last_move_status = False
        self.checked_status = False
        self.clicked_status = False
        self.clicked_choice = []
        # for checkmate
        self.checkmate_status = False
        self.save_position = []
        self.board = self.make_copy(data.board)
        self.sprites = {"bP":pygame.transform.scale(pygame.image.load("images/bP.png"), (125, 125)),
                           "bR":pygame.transform.scale(pygame.image.load("images/bR.png"), (125, 125)),
                           "bN":pygame.transform.scale(pygame.image.load("images/bN.png"), (125, 125)),
                           "bK":pygame.transform.scale(pygame.image.load("images/bK.png"), (125, 125)),
                           "bQ":pygame.transform.scale(pygame.image.load("images/bQ.png"), (125, 125)),
                           "bB":pygame.transform.scale(pygame.image.load("images/bB.png"), (125, 125)),
                           "wP":pygame.transform.scale(pygame.image.load("images/wP.png"), (125, 125)),
                           "wR":pygame.transform.scale(pygame.image.load("images/wR.png"), (125, 125)),
                           "wN":pygame.transform.scale(pygame.image.load("images/wN.png"), (125, 125)),
                           "wK":pygame.transform.scale(pygame.image.load("images/wK.png"), (125, 125)),
                           "wQ":pygame.transform.scale(pygame.image.load("images/wQ.png"), (125, 125)),
                           "wB":pygame.transform.scale(pygame.image.load("images/wB.png"), (125, 125))}
        self.show_promotion = False
        # Undo and Redo
        self.undo_list = []

        self.book = {}
        self.zombie_font = "ZOMBIE.TTF"
        self.menu_font = "Toxia-OwOA.ttf"
        # pygame related things
        self.cell_dimension = (80, 80)
        self.info = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.info.current_w, self.info.current_h))
        self.game_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.game_backgroud = pygame.image.load("images/lava.jpg")
        self.game_surface.blit(self.game_backgroud, (0, 0))

        self.board_surface = pygame.Surface((self.info.current_h-80,self.info.current_h-80))
        self.icon_image = pygame.image.load("images/chess.png")
        pygame.display.set_caption("Chess Game")
        self.text_font_checkmate = pygame.font.Font("Roboto-Regular.ttf", 60)
        self.checkmate_font = pygame.font.Font("ZOMBIE.TTF",80)
        self.win_font = pygame.font.Font("ZOMBIE.TTF",40)
        self.promot_font = pygame.font.Font("ZOMBIE.TTF", 30)
        self.index_font = pygame.font.Font("Roboto-Regular.ttf", 20)
        # self.checkmate_image = pygame.image.load("images/checkmate.jpg")

        self.promotion_surface = pygame.Surface((500,250),pygame.SRCALPHA, 16)

        # Intro
        self.intro_surface = pygame.Surface((self.info.current_w,self.info.current_h))
        self.intro_backgroud = pygame.image.load("images/battle_chess.jpg")
        self.intro_surface.blit(self.intro_backgroud,(0,0))
        self.zombie_font = "ZOMBIE.TTF"
        self.menu_font = "Toxia-OwOA.ttf"
        self.intro_menu = {"continue":{"x":self.info.current_w//2,
                                       "y":400,
                                       "width":255,
                                       "height":50,
                                        "color":(225,255,0),
                                       "hover":False},
                           "new game": {"x": self.info.current_w // 2,
                                        "y": 500,
                                        "width": 253,
                                        "height": 50,
                                        "color": (255, 255, 0),
                                        "hover":False},
                           "mode": {"x": self.info.current_w // 2,
                                        "y": 600,
                                        "width": 132,
                                        "height": 50,
                                        "color": (255, 255, 0),
                                    "hover":False},
                           "level": {"x": self.info.current_w // 2,
                                        "y": 700,
                                        "width": 128,
                                        "height": 50,
                                        "color": (255, 255, 0),
                                     "hover":False},
                           "info": {"x": self.info.current_w // 2,
                                        "y": 800,
                                        "width": 105,
                                        "height": 50,
                                        "color": (255, 255, 0),
                                    "hover":False},
                           "exit": {"x": self.info.current_w // 2,
                                        "y": 900,
                                        "width": 98,
                                        "height": 50,
                                        "color": (255, 255, 0),
                                    "hover":False}
                           }


        # level
        self.level_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.level_backgroud = pygame.image.load("images/battle_chess.jpg")
        self.level_surface.blit(self.intro_backgroud, (0, 0))
        self.level_menu = {
                           "low": {"x": self.info.current_w // 2,
                                    "y": 550,
                                   "default":False,
                                    "width": 132,
                                    "height": 50,
                                    "color": (255, 255, 0),
                                    "hover": False},
                           "medium": {"x": self.info.current_w // 2,
                                     "y": 650,
                                     "width": 128,
                                      "default": True,
                                     "height": 50,
                                     "color": (255, 255, 0),
                                     "hover": False},
                           "high": {"x": self.info.current_w // 2,
                                    "y": 750,
                                    "width": 105,
                                    "height": 50,
                                    "default":False,
                                    "color": (255, 255, 0),
                                    "hover": False},
                           "back": {"x": self.info.current_w // 2,
                                    "y": 900,
                                    "width": 98,
                                    "height": 50,
                                    "default": False,
                                    "color": (255, 255, 0),
                                    "hover": False}
                           }

        # select mode
        self.mode_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.mode_backgroud = pygame.image.load("images/battle_chess.jpg")
        self.mode_surface.blit(self.intro_backgroud, (0, 0))
        self.mode_menu = {
            "against computer": {"x": self.info.current_w // 2,
                    "y": 550,
                    "default": True,
                    "width": 300,
                    "height": 50,
                    "color": (255, 255, 0),
                    "hover": False},
            "against human": {"x": self.info.current_w // 2,
                       "y": 650,
                       "width": 300,
                       "default": False,
                       "height": 50,
                       "color": (255, 255, 0),
                       "hover": False},
            "back": {"x": self.info.current_w // 2,
                     "y": 750,
                     "width": 105,
                     "height": 50,
                     "default": False,
                     "color": (255, 255, 0),
                     "hover": False},
        }

        # info
        self.info_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.info_backgroud = pygame.image.load("images/battle_chess.jpg")
        self.info_surface.blit(self.intro_backgroud, (0, 0))


        # Killed piece surface
        self.killed_sprites = {"bP": pygame.transform.scale(pygame.image.load("images/bP.png"), (60, 60)),
                        "bR": pygame.transform.scale(pygame.image.load("images/bR.png"), (60, 60)),
                        "bN": pygame.transform.scale(pygame.image.load("images/bN.png"), (60, 60)),
                        "bK": pygame.transform.scale(pygame.image.load("images/bK.png"), (60, 60)),
                        "bQ": pygame.transform.scale(pygame.image.load("images/bQ.png"), (60, 60)),
                        "bB": pygame.transform.scale(pygame.image.load("images/bB.png"), (60, 60)),
                        "wP": pygame.transform.scale(pygame.image.load("images/wP.png"), (60, 60)),
                        "wR": pygame.transform.scale(pygame.image.load("images/wR.png"), (60, 60)),
                        "wN": pygame.transform.scale(pygame.image.load("images/wN.png"), (60, 60)),
                        "wK": pygame.transform.scale(pygame.image.load("images/wK.png"), (60, 60)),
                        "wQ": pygame.transform.scale(pygame.image.load("images/wQ.png"), (60, 60)),
                        "wB": pygame.transform.scale(pygame.image.load("images/wB.png"), (60, 60))}

        self.killed_piece = []
        self.black_surface = pygame.Surface((80,1000),pygame.SRCALPHA, 32)
        self.white_surface = pygame.Surface((80,1000),pygame.SRCALPHA, 32)




        # text = self.text_font_for_player_turn.render()

    def reset_board(self):
        self.color_black = (120, 77, 50)
        self.color_white = (251, 242, 227)
        self.player1 = "black"
        self.player2 = "white"
        self.player_turn = self.player2
        self.game_status = "main_menu"


        # For checked
        self.total_move = 0
        self.draw_last_move_status = False
        self.checked_status = False
        self.clicked_status = False
        self.clicked_choice = []
        # for checkmate
        self.checkmate_status = False
        self.save_position = []
        self.board = self.make_copy(data.board)
        self.show_promotion = False
        # Undo and Redo
        self.undo_list = []
        # pygame related things
        self.game_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.game_backgroud = pygame.image.load("images/lava.jpg")
        self.game_surface.blit(self.game_backgroud, (0, 0))

        self.board_surface = pygame.Surface((self.info.current_h - 80, self.info.current_h - 80))
        # self.checkmate_image = pygame.image.load("images/checkmate.jpg")

        self.promotion_surface = pygame.Surface((500, 250), pygame.SRCALPHA, 16)

        # Intro
        self.intro_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.intro_surface.blit(self.intro_backgroud, (0, 0))

        # level
        self.level_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.level_surface.blit(self.intro_backgroud, (0, 0))

        # select mode
        self.mode_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.mode_surface.blit(self.intro_backgroud, (0, 0))

        # info
        self.info_surface = pygame.Surface((self.info.current_w, self.info.current_h))
        self.info_surface.blit(self.intro_backgroud, (0, 0))

        self.killed_piece = []
        self.black_surface = pygame.Surface((80, 1000), pygame.SRCALPHA, 32)
        self.white_surface = pygame.Surface((80, 1000), pygame.SRCALPHA, 32)

    def event_for_play_against_cpu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_status = "main_menu"
            if self.player_turn == self.player2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.undo_list)>=2:
                            self.undo_list.pop()
                            self.killed_piece.pop()
                            self.board = self.make_copy(self.undo_list[-1])
                            self.undo_list.pop()
                            self.killed_piece.pop()
                            if len(self.undo_list) % 2 == 1:
                                self.player_turn = self.player1
                            else:
                                self.player_turn = self.player2
                            self.clicked_choice.clear()
                            self.clicked_status = False
                            if self.get_checked_status(self.player_turn[0]):
                                self.checked_status = True
                                self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                            else:
                                self.checked_status = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: # return (left, middle, right) as (1,0,0)
                        pos = pygame.mouse.get_pos() # getting coordinate where mouse was beign clicked
                        if self.show_promotion:
                            x,y = (pos[0],pos[1])
                            selected_item = "00"
                            if 250+460< x <375+460 and 375+40< y < 540:
                                selected_item = "wK"
                            elif 375+460< x <500+460 and 375+40<y < 540:
                                selected_item = "wR"
                            elif 500+460< x <625+460 and 375+40<y < 540:
                                selected_item = "wN"
                            elif 625+460< x < 750+ 460 and 375+40<y < 540:
                                selected_item = "wB"
                            if selected_item != "00":
                                self.board[self.show_promotion_position[1]][self.show_promotion_position[0]] = selected_item
                                self.player_turn = self.player1
                                self.show_promotion = False
                                if self.get_checked_status(self.player_turn[0]):
                                    self.checked_status = True
                                    self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                                else:
                                    self.checked_status = False

                        else:
                            x,y = (pos[0]-460)//125, (pos[1]-40)//125
                            if (x,y) in self.clicked_choice and self.clicked_status:
                                self.undo_list.append(self.make_copy(self.board))
                                self.killed_piece.append(self.board[y][x])
                                self.initial_pos = (self.clicked_piece[0], self.clicked_piece[1])
                                self.final_pos = (x,y)
                                item_at_clicked_piece = self.board[self.clicked_piece[1]][self.clicked_piece[0]]
                                self.board[y][x] = item_at_clicked_piece
                                self.board[self.clicked_piece[1]][self.clicked_piece[0]] = "00"
                                # if self.player_turn == self.player1:
                                #     self.player_turn = self.player2
                                # else:
                                if y == 0 and item_at_clicked_piece == "wP":
                                    self.show_promotion_position = (x,y)
                                    self.show_promotion = True
                                else:
                                    self.player_turn = self.player1

                                if self.get_checked_status(self.player_turn[0]):
                                    self.checked_status = True
                                    self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                                else:
                                    self.checked_status = False
                                self.total_move +=1
                                self.clicked_status = False
                                self.clicked_choice.clear()
                                self.draw_last_move_status = True
                            elif self.check_valid_click(x,y) and not self.check_checkmate(self.board,self.player_turn[0]):
                                self.draw_last_move_status = False
                                self.clicked_piece = (x,y)
                                self.clicked_status = True
                                possible_move = self.get_valid_choice(self.board,x,y)
                                self.clicked_choice = possible_move[:]
    def event_for_play_against_human(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_status = "main_menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.undo_list)>=1:
                            self.board = self.make_copy(self.undo_list[-1])
                            self.undo_list.pop()
                            self.killed_piece.pop()
                            if self.player_turn == self.player1:
                                self.player_turn = self.player2
                            else:
                                self.player_turn = self.player1
                            self.clicked_choice.clear()
                            self.clicked_status = False
                            if self.get_checked_status(self.player_turn[0]):
                                self.checked_status = True
                                self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                            else:
                                self.checked_status = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]: # return (left, middle, right) as (1,0,0)
                        pos = pygame.mouse.get_pos() # getting coordinate where mouse was beign clicked
                        if self.show_promotion:
                            x,y = (pos[0],pos[1])
                            selected_item = "00"
                            if self.player_turn[0] == "w":
                                if 250+460< x <375+460 and 375+40< y < 540:
                                    selected_item = "wK"
                                elif 375+460< x <500+460 and 375+40<y < 540:
                                    selected_item = "wR"
                                elif 500+460< x <625+460 and 375+40<y < 540:
                                    selected_item = "wN"
                                elif 625+460< x < 750+ 460 and 375+40<y < 540:
                                    selected_item = "wB"
                            else:
                                if 250+460< x <375+460 and 375+40< y < 540:
                                    selected_item = "bK"
                                elif 375+460< x <500+460 and 375+40<y < 540:
                                    selected_item = "bR"
                                elif 500+460< x <625+460 and 375+40<y < 540:
                                    selected_item = "bN"
                                elif 625+460< x < 750+ 460 and 375+40<y < 540:
                                    selected_item = "bB"
                            if selected_item != "00":
                                self.board[self.show_promotion_position[1]][self.show_promotion_position[0]] = selected_item
                                if self.player_turn == self.player1:
                                    self.player_turn = self.player2
                                else:
                                    self.player_turn = self.player1
                                self.show_promotion = False
                                if self.get_checked_status(self.player_turn[0]):
                                    self.checked_status = True
                                    self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                                else:
                                    self.checked_status = False

                        else:
                            x,y = (pos[0]-460)//125, (pos[1]-40)//125
                            if (x,y) in self.clicked_choice and self.clicked_status:
                                self.undo_list.append(self.make_copy(self.board))
                                self.killed_piece.append(self.board[y][x])
                                self.initial_pos = (self.clicked_piece[0], self.clicked_piece[1])
                                self.final_pos = (x,y)
                                item_at_clicked_piece = self.board[self.clicked_piece[1]][self.clicked_piece[0]]
                                self.board[y][x] = item_at_clicked_piece
                                self.board[self.clicked_piece[1]][self.clicked_piece[0]] = "00"
                                if y == 0 and item_at_clicked_piece == "wP":
                                    self.show_promotion_position = (x,y)
                                    self.show_promotion = True
                                elif y == 7 and item_at_clicked_piece == "bP":
                                    self.show_promotion_position = (x,y)
                                    self.show_promotion = True
                                else:
                                    if self.player_turn == self.player1:
                                        self.player_turn = self.player2
                                    else:
                                        self.player_turn = self.player1

                                if self.get_checked_status(self.player_turn[0]):
                                    self.checked_status = True
                                    self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                                else:
                                    self.checked_status = False
                                self.total_move +=1
                                self.clicked_status = False
                                self.clicked_choice.clear()
                                self.draw_last_move_status = True
                            elif self.check_valid_click(x,y) and not self.check_checkmate(self.board,self.player_turn[0]):
                                self.draw_last_move_status = False
                                self.clicked_piece = (x,y)
                                self.clicked_status = True
                                possible_move = self.get_valid_choice(self.board,x,y)
                                self.clicked_choice = possible_move[:]

    def draw_turn(self):
        pass

    def draw_killed_pieces(self):
        self.black_surface.fill((100, 100, 100, 3))
        self.white_surface.fill((100, 100, 100, 3))
        by = 10
        wy = 1000-70
        for item in self.killed_piece:
            if item !="00":
                if item[0] == "w":
                    self.white_surface.blit(self.killed_sprites[item], (10,wy))
                    wy += -60
                else:
                    self.black_surface.blit(self.killed_sprites[item], (10, by))
                    by += 60
            else:
                pass
        self.game_surface.blit(self.white_surface, (190, 40))
        self.game_surface.blit(self.black_surface, (1650, 40))
    def cpu_thinking_animation(self,index):
        if index == 0:
            ani_surf = pygame.Surface((20,20))
            ani_surf.fill((255,0,0))
            self.board_surface.blit(ani_surf, (520,460))
        elif index == 1:
            ani_surf = pygame.Surface((20,20))
            ani_surf.fill((0, 255, 0))
            self.board_surface.blit(ani_surf, (520, 520))
        elif index == 2:
            ani_surf = pygame.Surface((20,20))
            ani_surf.fill((0, 0, 255))
            self.board_surface.blit(ani_surf, (460, 520))
        else:
            ani_surf = pygame.Surface((20,20))
            ani_surf.fill((0,0,0))
            self.board_surface.blit(ani_surf, (460, 460))


    def game(self):
        if self.play_against == "cpu":
            self.event_for_play_against_cpu()
        else:
            self.event_for_play_against_human()
        self.draw_board()
        if self.checked_status:
            self.draw_checked()
        if self.clicked_status:
            self.show_choices()
        if self.draw_last_move_status:
            self.draw_last_move()
        self.draw_pieces()
        # self.draw_turn()
        if self.check_checkmate(self.board,self.player_turn[0]):
            if self.player_turn == self.player1:
                text = "White Won"
                self.draw_checkmate(text,(255,255,255))
            else:
                text = "Black Won"
                self.draw_checkmate(text,(0,0,0))
        if self.play_against == 'cpu' and self.player_turn == self.player1:
            self.cpu_thinking_animation(int(self.animation_no)%4)
            self.animation_no +=0.15
        if self.show_promotion:
            self.show_promotion_option(self.player_turn[0])
        self.draw_killed_pieces()
        self.game_surface.blit(self.board_surface,((self.info.current_w - self.info.current_h + 80)//2,40))
        self.screen.blit(self.game_surface, (0,0))
        pygame.display.update()
        if self.play_against == "cpu" and self.player_turn==self.player1:
            # self.cpu_turn()
            if self.active_for_process:
                self.active_for_process = False
                mythread = threading.Thread(target=self.cpu_turn)
                mythread.start()

    def cpu_turn(self):
        if self.player_turn == self.player1 and not self.check_checkmate(self.board, self.player_turn[0]):
            if self.show_promotion:
                best = -1000000
                choice = "bK"
                for item in ["bK", "bR", "bN", "bB"]:
                    self.board[self.show_promotion_position[1]][self.show_promotion_position[0]] = item
                    copy_board = self.make_copy(self.board)
                    score, initial, final = self.minimax(copy_board, 4, -10000000, 10000000, False, self.total_move)
                    if score > best:
                        best = score
                        choice = item
                self.board[self.show_promotion_position[1]][self.show_promotion_position[0]] = choice
                self.player_turn = self.player2
                self.active_for_process = True
                self.show_promotion = False
                if self.get_checked_status(self.player_turn[0]):
                    self.checked_status = True
                    self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                else:
                    self.checked_status = False


            else:
                if not self.check_checkmate(self.board,self.player_turn[0]):
                    self.undo_list.append(self.make_copy(self.board))
                    copy_board = self.make_copy(self.board)
                    score, initial, final = self.minimax(copy_board, self.level, -10000000, 10000000, True, self.total_move)
                    # print("score: ", score, "initial : ", initial, "final: ", final)
                    self.killed_piece.append(self.board[final[1]][final[0]])
                    self.initial_pos = initial
                    self.final_pos = final
                    item = self.board[initial[1]][initial[0]]
                    self.board[initial[1]][initial[0]] = "00"
                    self.board[final[1]][final[0]] = item
                    self.draw_last_move_status = True
                    if final[1] == 7 and item == "bP":
                        self.show_promotion_position = final
                        self.show_promotion = True
                    else:
                        self.player_turn = self.player2
                        self.active_for_process = True

                    if self.get_checked_status(self.player_turn[0]):
                        self.checked_status = True
                        self.queen_position = self.get_queen_position(self.board, self.player_turn[0])
                    else:
                        self.checked_status = False
                    self.total_move += 1

    def draw_text(self,text,font_name,size,x,y,color,surface):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx, text_rect.centery = x , y
        # print(text,text_rect.size)
        surface.blit(text_surface,text_rect)

    # main_menu+


    def draw_menu(self):
        hcolor = (255,160,0) # color on hover
        ncolor = (255,255,0) # default color
        for menu in self.intro_menu:
            if self.intro_menu[menu]["hover"]:
                self.draw_text(menu,self.zombie_font,50,self.intro_menu[menu]["x"],self.intro_menu[menu]["y"],hcolor,self.intro_surface)
            else:
                self.draw_text(menu, self.zombie_font, 50, self.intro_menu[menu]["x"], self.intro_menu[menu]["y"],ncolor, self.intro_surface)
    def draw_hover(self,x,y):
        for menu in self.intro_menu:
            x1,x2 = self.intro_menu[menu]["x"]-self.intro_menu[menu]["width"]//2 , self.intro_menu[menu]["x"]+self.intro_menu[menu]["width"]//2
            y1,y2 = self.intro_menu[menu]["y"]-self.intro_menu[menu]["height"]//2 , self.intro_menu[menu]["y"]+self.intro_menu[menu]["height"]//2
            if x1 < x <x2 and y1<y<y2:
                self.intro_menu[menu]["hover"] = True
            else:
                self.intro_menu[menu]["hover"] = False
    def follow_command(self,x,y):
        for menu in self.intro_menu:
            x1, x2 = self.intro_menu[menu]["x"] - self.intro_menu[menu]["width"] // 2, \
                     self.intro_menu[menu]["x"] + self.intro_menu[menu]["width"] // 2
            y1, y2 = self.intro_menu[menu]["y"] - self.intro_menu[menu]["height"] // 2, \
                     self.intro_menu[menu]["y"] + self.intro_menu[menu]["height"] // 2
            if x1 < x < x2 and y1 < y < y2:
                if menu == "continue":
                    self.click_sound.play()
                    self.game_status = "game"
                if menu == "new game":
                    self.click_sound.play()
                    self.reset_board()
                    self.game_status = "game"
                if menu == "level":
                    self.click_sound.play()
                    self.game_status = "level_menu"
                if menu == "mode":
                    self.click_sound.play()
                    self.game_status = "select_mode"
                if menu == "info":
                    self.click_sound.play()
                    self.game_status = "game_info"
                if menu == "exit":
                    self.click_sound.play()
                    pygame.quit()
                    sys.exit()
            else:
                pass
    def main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == pygame.KEYDOWN:
            #     self.game_status = "main"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x,y = pygame.mouse.get_pos()
                    self.follow_command(x,y)
        x,y = pygame.mouse.get_pos()
        self.draw_hover(x,y)

        # print(self.info.current_w,self.info.current_h)
        self.draw_text("Battle Chess",self.zombie_font,90,self.info.current_w//2,200,(255,200,0),self.intro_surface)
        self.draw_menu()
        self.screen.blit(self.intro_surface,(0,0))
        pygame.display.update()

    # select level
    def draw_level_menu(self):
        hcolor = (255, 160, 0)  # color on hover
        dcolor = (255, 255, 0)  # default color
        scolor = (255,0,0) # selected color
        for menu in self.level_menu:
            if self.level_menu[menu]["default"]:
                self.draw_text(menu, self.zombie_font, 50, self.level_menu[menu]["x"], self.level_menu[menu]["y"],
                               scolor, self.level_surface)
            elif self.level_menu[menu]["hover"]:
                self.draw_text(menu, self.zombie_font, 50, self.level_menu[menu]["x"], self.level_menu[menu]["y"],
                               hcolor, self.level_surface)
            else:
                self.draw_text(menu, self.zombie_font, 50, self.level_menu[menu]["x"], self.level_menu[menu]["y"],
                               dcolor, self.level_surface)
    def draw_level_hover(self,x,y):
        for menu in self.level_menu:
            x1,x2 = self.level_menu[menu]["x"]-self.level_menu[menu]["width"]//2 , self.level_menu[menu]["x"]+self.level_menu[menu]["width"]//2
            y1,y2 = self.level_menu[menu]["y"]-self.level_menu[menu]["height"]//2 , self.level_menu[menu]["y"]+self.level_menu[menu]["height"]//2
            if x1 < x <x2 and y1<y<y2:
                self.level_menu[menu]["hover"] = True
            else:
                self.level_menu[menu]["hover"] = False
    def follow_level_command(self,x,y):
        for menu in self.level_menu:
            x1, x2 = self.level_menu[menu]["x"] - self.level_menu[menu]["width"] // 2, \
                     self.level_menu[menu]["x"] + self.level_menu[menu]["width"] // 2
            y1, y2 = self.level_menu[menu]["y"] - self.level_menu[menu]["height"] // 2, \
                     self.level_menu[menu]["y"] + self.level_menu[menu]["height"] // 2
            if x1 < x < x2 and y1 < y < y2:
                if menu == "low":
                    self.click_sound.play()
                    self.level = 2
                    self.level_menu["low"]["default"] = True
                    self.level_menu["medium"]["default"] = False
                    self.level_menu["high"]["default"] = False
                if menu == "medium":
                    self.click_sound.play()
                    self.level = 3
                    self.level_menu["low"]["default"] = False
                    self.level_menu["medium"]["default"] = True
                    self.level_menu["high"]["default"] = False
                if menu == "high":
                    self.click_sound.play()
                    self.level = 4
                    self.level_menu["low"]["default"] = False
                    self.level_menu["medium"]["default"] = False
                    self.level_menu["high"]["default"] = True
                if menu == "back":
                    self.click_sound.play()
                    self.game_status = "main_menu"
            else:
                pass
    def select_level(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x,y = pygame.mouse.get_pos()
                    self.follow_level_command(x,y)
        x,y = pygame.mouse.get_pos()
        self.draw_level_hover(x,y)
        self.draw_text("Battle Chess",self.zombie_font,90,self.info.current_w//2,200,(255,200,0),self.level_surface)
        self.draw_text("Level",self.zombie_font,80,self.info.current_w//2,400,(255,150,0),self.level_surface)
        self.draw_level_menu()
        self.screen.blit(self.level_surface,(0,0))
        pygame.display.update()


    # select mode
    def draw_mode_menu(self):
        hcolor = (255, 160, 0)  # color on hover
        dcolor = (255, 255, 0)  # default color
        scolor = (255,0,0) # selected color
        for menu in self.mode_menu:
            if self.mode_menu[menu]["default"]:
                self.draw_text(menu, self.zombie_font, 50, self.mode_menu[menu]["x"], self.mode_menu[menu]["y"],
                               scolor, self.mode_surface)
            elif self.mode_menu[menu]["hover"]:
                self.draw_text(menu, self.zombie_font, 50, self.mode_menu[menu]["x"], self.mode_menu[menu]["y"],
                               hcolor, self.mode_surface)
            else:
                self.draw_text(menu, self.zombie_font, 50, self.mode_menu[menu]["x"], self.mode_menu[menu]["y"],
                               dcolor, self.mode_surface)
    def draw_mode_hover(self,x,y):
        for menu in self.mode_menu:
            x1,x2 = self.mode_menu[menu]["x"]-self.mode_menu[menu]["width"]//2 , self.mode_menu[menu]["x"]+self.mode_menu[menu]["width"]//2
            y1,y2 = self.mode_menu[menu]["y"]-self.mode_menu[menu]["height"]//2 , self.mode_menu[menu]["y"]+self.mode_menu[menu]["height"]//2
            if x1 < x <x2 and y1<y<y2:
                self.mode_menu[menu]["hover"] = True
            else:
                self.mode_menu[menu]["hover"] = False
    def follow_mode_command(self,x,y):
        for menu in self.mode_menu:
            x1, x2 = self.mode_menu[menu]["x"] - self.mode_menu[menu]["width"] // 2, \
                     self.mode_menu[menu]["x"] + self.mode_menu[menu]["width"] // 2
            y1, y2 = self.mode_menu[menu]["y"] - self.mode_menu[menu]["height"] // 2, \
                     self.mode_menu[menu]["y"] + self.mode_menu[menu]["height"] // 2
            if x1 < x < x2 and y1 < y < y2:
                if menu == "against computer":
                    self.click_sound.play()
                    self.play_against = "cpu"
                    self.mode_menu["against computer"]["default"] = True
                    self.mode_menu["against human"]["default"] = False
                if menu == "against human":
                    self.click_sound.play()
                    self.play_against = "human"
                    self.mode_menu["against computer"]["default"] = False
                    self.mode_menu["against human"]["default"] = True
                if menu == "back":
                    self.click_sound.play()
                    self.game_status = "main_menu"
            else:
                pass
    def select_mode(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x,y = pygame.mouse.get_pos()
                    self.follow_mode_command(x,y)
        x,y = pygame.mouse.get_pos()
        self.draw_mode_hover(x,y)
        self.draw_text("Battle Chess",self.zombie_font,90,self.info.current_w//2,200,(255,200,0),self.mode_surface)
        self.draw_text("Game Mode",self.zombie_font,80,self.info.current_w//2,400,(255,150,0),self.mode_surface)
        self.draw_mode_menu()
        self.screen.blit(self.mode_surface,(0,0))
        pygame.display.update()

    # Game Info
    def game_info(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x,y = pygame.mouse.get_pos()
                    x1, x2 = self.info.current_w // 2 - 65, self.info.current_w // 2 + 65
                    y1, y2 = 875, 925
                    if x1 < x < x2 and y1 < y < y2:
                        self.click_sound.play()
                        self.game_status = "main_menu"

        self.draw_text("Battle Chess",self.zombie_font,90,self.info.current_w//2,200,(255,200,0),self.info_surface)
        self.draw_text("Developed By Chhotu Kumar & Vaibhav Sathawane",self.menu_font,40,self.info.current_w//2,350,(255,0,0),self.info_surface)
        x, y = pygame.mouse.get_pos()
        x1, x2 = self.info.current_w//2 - 65, self.info.current_w//2 + 65
        y1, y2 = 875, 925
        if x1 < x < x2 and y1 < y < y2:
            self.draw_text("back", self.zombie_font, 50, self.info.current_w // 2, 900, (255, 190, 0),
                           self.info_surface)
        else:
            self.draw_text("back", self.zombie_font, 50, self.info.current_w // 2, 900, (255, 255, 0),
                           self.info_surface)
        # self.draw_text("back",self.zombie_font,50,self.info.current_w//2,900,(255,255,0),self.info_surface)
        self.screen.blit(self.info_surface,(0,0))
        pygame.display.update()


    def status_manager(self):
        if self.game_status == "main_menu":
            self.main_menu()
        if self.game_status == "game":
            self.game()
        if self.game_status == "level_menu":
            self.select_level()
        if self.game_status == "select_mode":
            self.select_mode()
        if self.game_status == "game_info":
            self.game_info()

    def draw_index(self):
        color = (0, 0, 0)
        x = 60+20
        text = self.index_font.render("a", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 10
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x +=80

        text = self.index_font.render("b", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 10
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80

        text = self.index_font.render("c", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 15
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80
        text = self.index_font.render("d", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 15
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80

        text = self.index_font.render("e", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 15
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80

        text = self.index_font.render("f", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 15
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80

        text = self.index_font.render("g", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 15
        self.screen.blit(text, text_rect)

        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80

        text = self.index_font.render("h", True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, 15
        self.screen.blit(text, text_rect)
        text_rect.centerx, text_rect.centery = x, 685
        self.screen.blit(text, text_rect)
        x += 80

        y = 700 - 40 - 30
        for i in range(1,9):
            text = self.index_font.render(str(i), True, color)
            text_rect = text.get_rect()
            text_rect.centerx, text_rect.centery = 15, y
            self.screen.blit(text, text_rect)
            y -= 80
        y = 700-40-30
        for i in range(1,9):
            text = self.index_font.render(str(i), True, color)
            text_rect = text.get_rect()
            text_rect.centerx, text_rect.centery = 685, y
            self.screen.blit(text, text_rect)
            y -= 80
    def draw_cell(self,x,y):
        if (x+y)%2 ==0:
            color = self.color_white
        else:
            color = self.color_black
        rect = pygame.Rect(x*125,y*125, 125,125)
        pygame.draw.rect(self.board_surface, color, rect)
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                self.draw_cell(i,j)
    def draw_pieces(self):
        for y in range(8):
            for x in range(8):
                if self.board[y][x] !="00":
                    position = (x * 125, y * 125)
                    self.board_surface.blit(self.sprites[self.board[y][x]], position)
    def show_choices(self):
        for choice in self.clicked_choice:
            x,y = choice[0],choice[1]
            if (x + y) % 2 == 0:
                color = (172, 172, 89)
            else:
                color = (128, 128, 0)
            rect = pygame.Rect(x *125, y *125, 125, 125)
            pygame.draw.rect(self.board_surface, color, rect)
    def draw_last_move(self):
        initial_color = (100,100,100)
        rect = pygame.Rect(self.initial_pos[0]*125,self.initial_pos[1]*125, 125,125)
        pygame.draw.rect(self.board_surface, initial_color, rect)

        final_color = (150, 150, 150)
        rect = pygame.Rect(self.final_pos[0] * 125, self.final_pos[1] * 125, 125,125)
        pygame.draw.rect(self.board_surface, final_color, rect)
    def draw_checked(self):
        color = (255, 0, 30)
        rect = pygame.Rect(self.queen_position[0] * 125, self.queen_position[1] * 125, 125, 125)
        pygame.draw.rect(self.board_surface, color, rect)
    def draw_checkmate(self,text2,color):
        self.promotion_surface.fill((255,100,0, 160))
        text = self.checkmate_font.render("Checkmate", True, (255, 255, 0))
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = 250,80
        self.promotion_surface.blit(text,text_rect)

        text = self.win_font.render(text2, True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = 250,180
        self.promotion_surface.blit(text,text_rect)

        self.board_surface.blit(self.promotion_surface,(250,375))

    def print_alpha_numeric(self,x,y):
        first = "0"
        if x==0:
            first = "a"
        elif x == 1:
            first = "b"
        elif x == 2:
            first = "c"
        elif x == 3:
            first = "d"
        elif x == 4:
            first = "e"
        elif x == 5:
            first = "f"
        elif x == 6:
            first = "g"
        elif x == 7:
            first = "h"

        second = 8-y
        print(first,second)
    def get_choice(self,board, x1,y1):
        valid_choice = []
        item = board[y1][x1]

        if item[1] == "P":
            if item[0] =="b":
                # down(0,1)
                x,y = x1,y1+1
                if 0<= x <= 7 and 0<=y <= 7:
                    if board[y][x] == "00":
                        valid_choice.append((x,y))
                # left attack(-1,1)
                x,y = x1-1, y1+1
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] != "00" and board[y][x][0] !="b":
                        valid_choice.append((x,y))
                # right attack(1,1)
                x, y = x1 + 1, y1 + 1
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] != "00" and board[y][x][0] != "b":
                        valid_choice.append((x, y))

                if y1==1:
                    # two step move
                    x,y = x1, y1+2
                    if board[y-1][x] == "00" and board[y][x] == "00":
                        valid_choice.append((x,y))

            else:
                # up(0,-1)
                x, y = x1, y1 - 1
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] == "00":
                        valid_choice.append((x, y))
                # left attack(-1,-1)
                x, y = x1 - 1, y1 - 1
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] != "00" and board[y][x][0] != "w":
                        valid_choice.append((x, y))
                # right attack(1,-1)
                x, y = x1 + 1, y1 - 1
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board[y][x] != "00" and board[y][x][0] != "w":
                        valid_choice.append((x, y))

                if y1 == 6:
                    # two step move
                    x, y = x1, y1 - 2
                    if board[y + 1][x] == "00" and board[y][x] == "00":
                        valid_choice.append((x, y))
        elif item[1] == "R":
            # up (0,-1)
            x,y = x1 , y1-1
            while 0<=x <= 7 and 0<=y<=7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x,y))
                    break
                y += -1
            # down(0,1)
            x, y = x1, y1 + 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += 1

            # Left(-1,0)
            x, y = x1-1, y1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                x += -1

            # Right (1,0)
            x, y = x1+1, y1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                x += 1
        elif item[1] == "B":
            # topleft (-1,-1)
            x, y = x1-1, y1 - 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += -1
                x += -1

            # topright(1,-1)
            x, y = x1 + 1, y1 - 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += -1
                x += 1

            #bottomleft(-1,1)
            x, y = x1 - 1, y1 + 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += 1
                x += -1

            #bottom right(1,1)
            x, y = x1 + 1, y1 + 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += 1
                x += 1
        elif item[1] == "K":
            # up (0,-1)
            x, y = x1, y1 - 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += -1
            # down(0,1)
            x, y = x1, y1 + 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += 1

            # Left(-1,0)
            x, y = x1 - 1, y1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                x += -1

            # Right (1,0)
            x, y = x1 + 1, y1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                x += 1

            # topleft (-1,-1)
            x, y = x1 - 1, y1 - 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += -1
                x += -1

            # topright(1,-1)
            x, y = x1 + 1, y1 - 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += -1
                x += 1

            # bottomleft(-1,1)
            x, y = x1 - 1, y1 + 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += 1
                x += -1

            # bottom right(1,1)
            x, y = x1 + 1, y1 + 1
            while 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
                    break
                y += 1
                x += 1
        elif item[1] == "Q":
            # up(0,-1)
            x,y = x1, y1-1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # down(0,1)
            x, y = x1, y1 + 1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # left(-1,0)
            x, y = x1-1, y1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # right(1,0)
            x, y = x1+1, y1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # topleft(-1,-1)
            x, y = x1-1, y1 - 1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # topright(1,-1)
            x, y = x1+1, y1 - 1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))

            # bottomleft(-1,1)
            x, y = x1-1, y1 + 1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))

             # bottomright(1,1)
            x, y = x1+1, y1 + 1
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # if not self.black_queen_moved_status:
            #     if board[y1][x1+1] == "00" and board[y1][x1+2] == "00" and board[y1][x1+3] == "bR":




        elif item[1] == "N":
            #(-1,-2)
            x,y = x1-1, y1-2
            if 0<= x <= 7 and 0<=y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x,y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # (-1,2)
            x, y = x1 - 1, y1 + 2
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            #top right(1,-2)
            x, y = x1 + 1, y1 - 2
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))

            # top right(1,2)
            x, y = x1 + 1, y1 + 2
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            # (2,-1)
            x, y = x1 + 2, y1 - 1
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            #(2,1)
            x, y = x1 + 2, y1 + 1
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            #(-2,-1)
            x, y = x1 - 2, y1 - 1
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
            #(-2,1)
            x, y = x1 - 2, y1 + 1
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board[y][x] == "00":
                    valid_choice.append((x, y))
                else:
                    if board[y][x][0] != item[0]:
                        valid_choice.append((x, y))
        return valid_choice
    def get_valid_choice(self,board,x1,y1):
        possible_move = self.get_choice(board,x1,y1)
        # print("All choice: ",possible_move)
        to_be_removed = []
        item_at_x1_and_y1 = board[y1][x1]
        # print("item_has_to_move: ",item_at_x1_and_y1)
        if item_at_x1_and_y1[1] != "Q":
            queen_pos = self.get_queen_position(board,item_at_x1_and_y1[0])
            # print("queen_position",queen_pos)

        for move in possible_move:
            item_at_move = board[move[1]][move[0]]
            # print("item_at_move before : ",move,item_at_move)
            board[move[1]][move[0]] = item_at_x1_and_y1 # move current item at new position ie move
            # print("item_at_move after : ",move,board[move[1]][move[0]])
            board[y1][x1] = "00"
            # print("item_has_to_move after: ", board[y1][x1])
            if item_at_x1_and_y1[1] == "Q":
                queen_pos = self.get_queen_position(board,item_at_x1_and_y1[0])
                # print("queen_position inside",queen_pos)

            flag = False
            # print(move)
            for y in range(8):
                for x in range(8):
                    if board[y][x] !="00" and  board[y][x][0] != item_at_x1_and_y1[0]:

                        temp_all_move = self.get_choice(board,x,y)
                        if queen_pos in temp_all_move:
                            to_be_removed.append(move)
                            flag = True
                            break
                if flag:
                    break
            board[move[1]][move[0]] = item_at_move
            board[y1][x1] = item_at_x1_and_y1
        for choice in to_be_removed:
            possible_move.remove(choice)
        return possible_move
    def get_queen_position(self,board,player):
        if player == "b":
            for y in range(8):
                for x in range(8):
                    if board[y][x] == "bQ":
                        return (x,y)
        if player == "w":
            for y in range(8):
                for x in range(8):
                    if board[y][x] == "wQ":
                        return (x,y)
    def get_checked_status(self,player):
        queen_pos = self.get_queen_position(self.board,player)
        for y in range(8):
            for x in range(8):
                if self.board[y][x] !="00"and  self.board[y][x][0] !=player:
                    possible_moves = self.get_choice(self.board,x,y)
                    if queen_pos in possible_moves:
                        return True
        return False
    def make_copy(self,board):
        copy = []
        for y in range(8):
            temp = []
            for x in range(8):
                temp.append(board[y][x])
            copy.append(temp)
        return copy
    def get_all_possible_moves(self,board,player):
        all_possible_move = []
        if player == "b":
            for y in range(8):
                for x in range(8):
                    if board[y][x] != "00" and board[y][x][0] == "b":
                        temp = self.get_valid_choice(board, x, y)
                        for item in temp:
                            all_possible_move.append(((x, y), item))
        else:
            for y in range(8):
                for x in range(8):
                    if board[y][x] != "00" and board[y][x][0] =="w":
                        temp = self.get_valid_choice(board,x,y)
                        for item in temp:
                            all_possible_move.append(((x,y),item))

        return all_possible_move
    def show_promotion_option(self, player):
        self.promotion_surface.fill((255, 100, 0, 160))
        if player == "w":
            text = self.promot_font.render("Select a Piece for promotion",False,(255,255,255))
            text_rect = text.get_rect()
            text_rect.centerx = 250
            text_rect.centery = 40
            self.promotion_surface.blit(text,text_rect)
            self.promotion_surface.blit(self.sprites["wK"], (0, 62))
            self.promotion_surface.blit(self.sprites["wR"], (125, 62))
            self.promotion_surface.blit(self.sprites["wN"], (250, 62))
            self.promotion_surface.blit(self.sprites["wB"], (375, 62))
            self.board_surface.blit(self.promotion_surface, (250, 375))
        if self.play_against == "cpu":
            if player == "b":
                text = self.promot_font.render("Selecting a Piece for promotion", False, (0,0, 0))
                text_rect = text.get_rect()
                text_rect.centerx = 250
                text_rect.centery = 40
                self.promotion_surface.blit(text, text_rect)
                self.promotion_surface.blit(self.sprites["bK"], (0, 62))
                self.promotion_surface.blit(self.sprites["bR"], (125, 62))
                self.promotion_surface.blit(self.sprites["bN"], (250, 62))
                self.promotion_surface.blit(self.sprites["bB"], (375, 62))
                self.board_surface.blit(self.promotion_surface,(250,375))
        else:
            if player == "b":
                text = self.promot_font.render("Select a Piece for promotion", False, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.centerx = 250
                text_rect.centery = 40
                self.promotion_surface.blit(text, text_rect)
                self.promotion_surface.blit(self.sprites["bK"], (0, 62))
                self.promotion_surface.blit(self.sprites["bR"], (125, 62))
                self.promotion_surface.blit(self.sprites["bN"], (250, 62))
                self.promotion_surface.blit(self.sprites["bB"], (375, 62))
                self.board_surface.blit(self.promotion_surface, (250, 375))

    def check_checkmate(self,board,player):
        #this is for black
        if player =="b":
            possible_move_black = []
            for y in range(8):
                for x in range(8):
                    if board[y][x] !="00" and board[y][x][0] == "b":
                        temp_move = self.get_valid_choice(board,x,y)
                        possible_move_black.extend(temp_move)
            # print("this is for black", possible_move_black)
            if len(possible_move_black) <= 0 :
                return True
        else:
            possible_move_white = []
            for y in range(8):
                for x in range(8):
                    if board[y][x] !="00" and board[y][x][0] == "w":
                        temp_move = self.get_valid_choice(board,x,y)
                        possible_move_white.extend(temp_move)
            # print("this is for white :",possible_move_white)
            if len(possible_move_white) <= 0:
                return True
        return False
    def check_valid_click(self,x,y):
        if 0<=x<=7 and 0<=y<=7:
            if self.board[y][x] !="00":
                if self.board[y][x][0] == "b" and self.player_turn == self.player1:
                    return True
                if self.board[y][x][0] == "w" and self.player_turn == self.player2:
                    return True
        return False

    def minimax(self,board, depth,alpha, beta, maximizing, total_move):
        if maximizing and self.check_checkmate(board,"b"):
            initial = (10, 10)
            final = (100, 100)
            score = -200000
            # print("In maxima game over")
            return score, initial, final
        if not maximizing and self.check_checkmate(board,"w"):
            initial = (10, 10)
            final = (100, 100)
            score = 200000
            # print("In minima gameover")
            return (score, initial, final)
        if depth == 0:
            initial = (10,10)
            final = (100,100)
            score = data.evaluateScore(board,total_move)
            return (score,initial,final)
        if maximizing:
            # print("maximizingggggggggggggggggggggggggg")
            best_score = -20000
            initial = (10,10)
            final = (100,100)

            possible_move = self.get_all_possible_moves(board,"b")
            for each_move in possible_move:
                start = each_move[0]
                end = each_move[1]

                item_start = board[start[1]][start[0]]
                item_at_each_move = board[end[1]][end[0]]
                board[end[1]][end[0]] = item_start
                board[start[1]][start[0]] = "00"
                # data.print_board(board)

                temp_score, temp_initial, temp_final = self.minimax(board, depth - 1, alpha, beta,not maximizing,total_move)

                if temp_score > best_score:
                    best_score = temp_score
                    initial = start
                    final = end
                # data.print_board(board)
                # print("depth: ",depth,"max: ",temp_score)
                board[start[1]][start[0]] = item_start
                board[end[1]][end[0]] = item_at_each_move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return (best_score,initial,final)
        else:
            # print("minimizing")
            best_score = 20000
            initial= (10, 10)
            final = (100, 100)
            possible_move = self.get_all_possible_moves(board, "w")
            for each_move in possible_move:
                start = each_move[0]
                end = each_move[1]

                item_start = board[start[1]][start[0]]
                item_at_each_move = board[end[1]][end[0]]
                board[end[1]][end[0]] = item_start
                board[start[1]][start[0]] = "00"
                # data.print_board(board)

                temp_score, temp_initial, temp_final = self.minimax(board, depth - 1, alpha, beta, not maximizing,
                                                                    total_move)

                if temp_score < best_score:
                    best_score = temp_score
                    initial = start
                    final = end
                # data.print_board(board)
                # print("depth: ",depth,"max: ",temp_score)
                board[start[1]][start[0]] = item_start
                board[end[1]][end[0]] = item_at_each_move
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return (best_score, initial, final)
    def make_key(self, board, maximizing):
        temp_string = ""
        #small letter for black and capital letter for white
        for y in range(8):
            for x in range(8):
                item = board[y][x]
                if item == "00":
                    temp_string +="0"
                elif item == "bP":
                    temp_string += "p"
                elif item == "wP":
                    temp_string +="P"
                elif item == "bK":
                    temp_string +="k"
                elif item == "wK":
                    temp_string += "K"
                elif item == "bQ":
                    temp_string += "q"
                elif item == "wQ":
                    temp_string += "Q"
                elif item == "bR":
                    temp_string += "r"
                elif item == "wR":
                    temp_string += "R"
                elif item == "bN":
                    temp_string += "n"
                elif item == "wN":
                    temp_string += "N"
                elif item == "bB":
                    temp_string += "b"
                elif item == "wB":
                    temp_string += "B"

        if maximizing:
            temp_string += "T"
        else:
            temp_string += "F"
        return temp_string