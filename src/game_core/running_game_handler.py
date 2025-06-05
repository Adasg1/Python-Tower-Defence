import pygame

from src.assets.asset_manager import AssetManager
from src.constants.colors import LIGHT_BROWN
from src.enum.game_state import GameState
from src.enum.tower_type import TowerType
from src.utils.exit_handler import handle_exit


class RunningGameHandler:
    def __init__(self, game_context, wave_manager, towers_manager, spells_manager):
        self.context = game_context
        self.towers = towers_manager
        self.waves = wave_manager
        self.spells = spells_manager
        self.timer_font = AssetManager.get_font('LuckiestGuy-Regular', 20)
        self.skip_table_bg = AssetManager.get_image("images/game_stats/skip_table", (260, 55))
        self.skip_button = AssetManager.get_image("images/buttons/button_skip", (55, 55))
        self.skip_button_rect = pygame.Rect(0, 0, 55, 55)
        self.pause_button = AssetManager.get_image("images/buttons/button_pause", (65, 65))
        self.pause_button_rect = self.pause_button.get_rect()
        self.pause_button_rect.topleft = (5, 5)

    def draw(self, screen):
        screen.blit(self.pause_button, self.pause_button_rect)
        self.draw_wave_info_and_skip(screen)

    def draw_wave_info_and_skip(self, screen):
        if self.waves.wave_delay:
            self.waves.ticks_since_last_wave += 1
            if self.waves.ticks_since_last_wave >= 900:
                self.waves.start_next_wave()

            bg_pos = (1023, 50)
            screen.blit(self.skip_table_bg, bg_pos)

            if self.context.game_stats.get_wave > 1:
                time_remaining = (900 - self.waves.ticks_since_last_wave)//60 + 1
                timer_text = self.timer_font.render(f"Next wave in: {time_remaining}s", True, LIGHT_BROWN) # wyswietlony timer
            else:
                timer_text = self.timer_font.render(f"Start First Wave", True,LIGHT_BROWN)  # wyswietlony timer
            screen.blit(timer_text, (bg_pos[0] + 25, bg_pos[1] + 18))

            self.skip_button_rect.topleft = (bg_pos[0] + 205, bg_pos[1])  # przycisk skip
            screen.blit(self.skip_button, self.skip_button_rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.pause_button_rect.collidepoint(mouse_pos):
                    self.context.game_state = GameState.PAUSED
                if self.skip_button_rect.collidepoint(mouse_pos) and self.waves.wave_delay:
                    self.waves.start_next_wave()
                    return

                for spell in self.spells.spells:
                    if spell.is_toggled:
                        if spell.rect.collidepoint(mouse_pos):
                            spell.is_toggled = False
                        else:
                            spell.is_toggled = False
                            spell.use(mouse_pos)
                    elif spell.rect.collidepoint(mouse_pos) and spell.is_unlocked:
                        if not spell.is_toggled and not spell.is_on_cooldown():
                            spell.is_toggled = True

                for spot in self.towers.spots:
                    if not spot.occupied:
                        if spot.rect.collidepoint(mouse_pos) and not spot.tower_ui.showed_options:
                            spot.tower_ui.show_options()
                        elif spot.tower_ui.showed_options:
                            up = 0
                            if spot.rect.midbottom[1] > 670:
                                up = 50
                            options_rect = pygame.Rect(
                                spot.rect.x - 30,
                                spot.rect.y - 60 - up,
                                200,
                                200
                            )

                            if options_rect.collidepoint(mouse_pos):
                                rel_x = mouse_pos[0] - options_rect.x
                                rel_y = mouse_pos[1] - options_rect.y
                                tower_type = None
                                if 70 < rel_x < 120 and 10 < rel_y < 60:
                                    tower_type = TowerType.ARCHER

                                elif 8 < rel_x < 58 and 60 < rel_y < 110:
                                    tower_type = TowerType.ICE

                                elif 135 < rel_x < 185 and 60 < rel_y < 110:
                                    tower_type = TowerType.STONE

                                elif 32 < rel_x < 82 and 128 < rel_y < 178:
                                    tower_type = TowerType.BANK

                                elif 110 < rel_x < 160 and 128 < rel_y < 178:
                                    tower_type = TowerType.EXECUTOR

                                if tower_type:
                                    if tower_type.cost <= self.context.game_stats.get_money:
                                        self.towers.place_tower(spot, tower_type)
                                    #else:
                                        #print("Not enough money")
                            else:
                                spot.tower_ui.hide_options()
                    else:
                        if spot.rect.collidepoint(mouse_pos) and not spot.tower_ui.showed_options:
                            spot.tower_ui.show_options()
                        elif spot.tower_ui.showed_options:
                            up = 0
                            if spot.tower.rect.midbottom[1] > 670:
                                up = 50
                            options_rect = pygame.Rect(
                                0,
                                0,
                                200,
                                200
                            )
                            options_rect.midbottom = spot.tower.rect.midbottom
                            options_rect.y += 50 - up

                            if options_rect.collidepoint(mouse_pos):
                                rel_x = mouse_pos[0] - options_rect.x
                                rel_y = mouse_pos[1] - options_rect.y
                                if 70 < rel_x < 120 and 10 < rel_y < 60:
                                    upgrade_cost = spot.tower.get_upgrade_cost()
                                    if upgrade_cost <= self.context.game_stats.get_money:
                                        self.towers.upgrade_tower(spot, upgrade_cost)
                                    #else:
                                        #print("Not enough money")

                                if 70 < rel_x < 120 and 140 < rel_y < 190:
                                    self.towers.sell_tower(spot)
                            else:
                                spot.tower_ui.hide_options()