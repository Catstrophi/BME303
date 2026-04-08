# Import all the needed libraries
import tkinter as tk
import random
from Tower_Class import Tower, add_towers
from Enemy_Class import Enemy, spawn_single_enemy
from Draw_Bone import draw_bone
from Fix_Bone import fix_bone
from Flow_Field import create_flow_field
from Vaccine_Class import Vaccine
from Game_Variables import *


class Bone_Game:
    # Added on_finish parameter
    def __init__(self, main_window, enable_vaccine=True, rindex_code=0, is_finished=None):
        self.main_window = main_window
        self.enable_vaccine = enable_vaccine
        self.game_finished = is_finished

        self.window_size = GRID_SIZE * CELL_SIZE
        self.window = tk.Canvas(self.main_window, width=self.window_size, height=self.window_size, bg="white")
        self.window.pack()

        self.random_index = random.Random(rindex_code)

        self.walls, self.left_edge, self.right_edge = draw_bone(self.window, GRID_SIZE, CELL_SIZE, FRACTURE_GAP,
                                                                self.random_index)
        self.towers = add_towers(self.window, TOWER_HP, TOWER_DMG, TOWER_RANGE, TOTAL_TOWERS, CELL_SIZE)
        self.flow_field = create_flow_field(self.walls, GRID_SIZE)

        self.enemies = []
        self.heal_timer = 0
        self.current_heal_speed = HEAL_SPEED
        self.vaccine = Vaccine(self.window)

        self.total_ticks = 0
        self.current_spawn_amount = BASE_SPAWN_AMOUNT
        self.spawn_accumulator = 0.0
        self.total_enemy_defeated = 0
        self.is_finished = False

        self.wave_info = self.window.create_text((GRID_SIZE * CELL_SIZE) // 2, 20, text="", fill="black",
                                                 font=("Arial", 14, "bold"))
        # Data tracking variables
        self.history_time = []
        self.history_enemies = []
        self.history_healing = []
        self.history_heal_speed = []

        total_gap = 0
        for y in self.right_edge:
            total_gap += self.right_edge[y] - self.left_edge[y]

        self.initial_gap = total_gap

    def enemy_spawn(self):
        spawn_rate = self.current_spawn_amount / TICKS_PER_CYCLE
        self.spawn_accumulator += spawn_rate

        while self.spawn_accumulator >= 1.0:
            new_enemy = spawn_single_enemy(self.window, ENEMY_HP, ENEMY_DMG, ENEMY_RANGE, GRID_SIZE, CELL_SIZE,
                                           self.random_index)
            self.enemies.append(new_enemy)
            self.spawn_accumulator -= 1.0

    def remove_destroyed(self):
        is_destroyed = False
        surviving_towers = []
        for current_tower in self.towers:
            if current_tower.health > 0:
                surviving_towers.append(current_tower)
            else:
                is_destroyed = True

        if is_destroyed == True and len(surviving_towers) > 0:
            all_health = []
            for tower in surviving_towers:
                all_health.append(tower.health)
                self.window.delete(tower.shape)
                self.window.delete(tower.hp)
            self.towers = add_towers(self.window, TOWER_HP, TOWER_DMG, TOWER_RANGE, len(all_health), CELL_SIZE,
                                     health_list=all_health)
        else:
            self.towers = surviving_towers

        surviving_enemies = []
        for current_enemy in self.enemies:
            if current_enemy.health > 0:
                surviving_enemies.append(current_enemy)
            else:
                self.total_enemy_defeated += 1
        self.enemies = surviving_enemies

    def actions(self):
        for current_tower in self.towers:
            current_tower.attack(self.enemies)
        for current_enemy in self.enemies:
            current_enemy.act(self.towers, self.flow_field)

    def bone_healing(self):
        enemies_in_radius = 0
        for current_enemy in self.enemies:
            enemy_distance = self.flow_field.get((current_enemy.cell_x, current_enemy.cell_y), 999)
            if enemy_distance <= INFECTION_RADIUS:
                enemies_in_radius += 1

        self.current_heal_speed = HEAL_SPEED
        if enemies_in_radius >= INFECTION_ENEMY:
            self.current_heal_speed += INFECTION_PENALTY

        self.heal_timer += UPDATE_SPEED

        if self.heal_timer >= self.current_heal_speed:
            is_bone_updated = fix_bone(self.window, CELL_SIZE, self.walls, self.left_edge, self.right_edge)
            if is_bone_updated:
                self.flow_field = create_flow_field(self.walls, GRID_SIZE)
            self.heal_timer = 0

    def game_over(self):
        center_x = (24 + 75) // 2
        left_edge_set = set(self.left_edge.values())
        right_edge_set = set(self.right_edge.values())

        if left_edge_set == {center_x} and right_edge_set == {center_x}:
            self.window.delete("all")
            self.window.configure(bg="green")
            win_text = f"BONE HEALED \n Stats: Towers: {TOTAL_TOWERS} \n Total Enemies: {self.total_enemy_defeated}"
            self.window.create_text((GRID_SIZE * CELL_SIZE) // 2, (GRID_SIZE * CELL_SIZE) // 2, text=win_text,
                                    fill="white", font=("Arial", 24, "bold"))
            return True

        for current_enemy in self.enemies:
            enemy_distance = self.flow_field.get((current_enemy.cell_x, current_enemy.cell_y))
            if enemy_distance == 0:
                self.window.delete("all")
                self.window.configure(bg="red")
                lose_text = f"INFECTED \n Stats: Towers: {TOTAL_TOWERS} \n Total Enemies: {self.total_enemy_defeated}"
                self.window.create_text((GRID_SIZE * CELL_SIZE) // 2, (GRID_SIZE * CELL_SIZE) // 2, text=lose_text,
                                        fill="black", font=("Arial", 20, "bold"))
                return True

        return False

    def update_ui(self):
        wave_num = (self.total_ticks // TICKS_PER_CYCLE) + 1

        if self.enable_vaccine:
            vaccine_text = f"Vaccine Amount: {self.vaccine.num_vaccine}"
        else:
            vaccine_text = "VACCINE DISABLED"

        display_text = f"Wave: {wave_num} | Spawn Rate: {self.current_spawn_amount} | Active Enemies: {len(self.enemies)} | {vaccine_text}"
        self.window.itemconfig(self.wave_info, text=display_text)
        self.window.tag_raise(self.wave_info)

    def record_data(self):
        self.history_time.append(self.total_ticks)
        self.history_enemies.append(len(self.enemies))

        current_gap = 0
        for y in self.right_edge:
            current_gap += self.right_edge[y] - self.left_edge[y]

        healing_percentage = max(0, 100 - ((current_gap / self.initial_gap) * 100))
        self.history_healing.append(healing_percentage)
        self.history_heal_speed.append(self.current_heal_speed)

    def game_loop(self):
        if self.is_finished:
            return

        self.total_ticks += 1

        if self.total_ticks % TICKS_PER_CYCLE == 0:
            self.current_spawn_amount = self.current_spawn_amount + self.current_spawn_amount * SPAWN_INCREASE_AMOUNT

        if self.enable_vaccine:
            self.current_spawn_amount = self.vaccine.apply(self.total_ticks, self.current_spawn_amount)

        self.enemy_spawn()
        self.remove_destroyed()
        self.actions()
        self.bone_healing()

        self.record_data()

        is_game_over = self.game_over()

        if is_game_over == True:
            self.game_finished()
            return

        self.update_ui()

        # The game drives its own clock again!
        self.main_window.after(UPDATE_SPEED, self.game_loop)

    def start_game(self):
        self.game_loop()