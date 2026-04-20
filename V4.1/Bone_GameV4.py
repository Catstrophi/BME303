# Import all the needed libraries
import tkinter as tk
import random
from Immune_Cell_Class import Immune_cell, add_Immune_cells
from Virus_Class import virus, spawn_single_virus
from Draw_Bone import draw_bone
from Fix_Bone import fix_bone
from Flow_Field import create_flow_field
from Antiviral_Class import Antiviral
from Game_Variables import *
from PIL import ImageGrab


class Bone_Game:
    # Added on_finish parameter
    def __init__(self, main_window, enable_Antiviral=True, rindex_code=0, is_finished=None):
        self.main_window = main_window
        self.enable_Antiviral = enable_Antiviral
        self.game_finished = is_finished

        self.window_size = GRID_SIZE * CELL_SIZE
        self.window = tk.Canvas(self.main_window, width=self.window_size, height=self.window_size, bg="white")
        self.window.pack()

        self.random_index = random.Random(rindex_code)

        self.walls, self.left_edge, self.right_edge = draw_bone(self.window, GRID_SIZE, CELL_SIZE, FRACTURE_GAP,
                                                                self.random_index)
        self.Immune_cells = add_Immune_cells(self.window, Immune_cell_HP, Immune_cell_DMG, Immune_cell_RANGE, TOTAL_Immune_cellS, CELL_SIZE)
        self.flow_field = create_flow_field(self.walls, GRID_SIZE)

        self.viruses = []
        self.heal_timer = 0
        self.current_heal_speed = HEAL_SPEED
        self.Antiviral = Antiviral(self.window)

        self.total_ticks = 0
        self.current_spawn_amount = BASE_SPAWN_AMOUNT
        self.spawn_accumulator = 0.0
        self.total_virus_defeated = 0
        self.is_finished = False

        self.wave_info = self.window.create_text((GRID_SIZE * CELL_SIZE) // 2, 20, text="", fill="black",
                                                 font=("Arial", 14, "bold"))
        # Data tracking variables
        self.history_time = []
        self.history_viruses = []
        self.history_healing = []
        self.history_heal_speed = []

        # GIF recording
        self.frames = []
        self.recording = True
        self.gif_filename = "simulation.gif"
        self.gif_fps = 20

        total_gap = 0
        for y in self.right_edge:
            total_gap += self.right_edge[y] - self.left_edge[y]

        self.initial_gap = total_gap

    def capture_frame(self):
        if not self.recording:
            return

        root = self.main_window.winfo_toplevel()
        root.update_idletasks()
        root.update()
        frame = ImageGrab.grab(window=root.winfo_id())
        self.frames.append(frame)

    def save_gif(self):
        """Save all captured frames as an animated GIF."""
        if not self.frames:
            return
        duration_ms = int(2000 / self.gif_fps)

        self.frames[0].save(
            self.gif_filename,
            save_all=True,
            append_images=self.frames[1:],
            loop=0,  # 0 = loop forever
            duration=duration_ms,
        )

    def virus_spawn(self):
        spawn_rate = self.current_spawn_amount / TICKS_PER_CYCLE
        self.spawn_accumulator += spawn_rate

        while self.spawn_accumulator >= 1.0:
            new_virus = spawn_single_virus(self.window, virus_HP, virus_DMG, virus_RANGE, GRID_SIZE, CELL_SIZE,
                                           self.random_index)
            self.viruses.append(new_virus)
            self.spawn_accumulator -= 1.0

    def remove_destroyed(self):
        is_destroyed = False
        surviving_Immune_cells = []
        for current_Immune_cell in self.Immune_cells:
            if current_Immune_cell.health > 0:
                surviving_Immune_cells.append(current_Immune_cell)
            else:
                is_destroyed = True

        if is_destroyed == True and len(surviving_Immune_cells) > 0:
            all_health = []
            for Immune_cell in surviving_Immune_cells:
                all_health.append(Immune_cell.health)
                self.window.delete(Immune_cell.shape)
                self.window.delete(Immune_cell.hp)
            self.Immune_cells = add_Immune_cells(self.window, Immune_cell_HP, Immune_cell_DMG, Immune_cell_RANGE, len(all_health), CELL_SIZE,
                                     health_list=all_health)
        else:
            self.Immune_cells = surviving_Immune_cells

        surviving_viruses = []
        for current_virus in self.viruses:
            if current_virus.health > 0:
                surviving_viruses.append(current_virus)
            else:
                self.total_virus_defeated += 1
        self.viruses = surviving_viruses

    def actions(self):
        for current_Immune_cell in self.Immune_cells:
            current_Immune_cell.attack(self.viruses)
        for current_virus in self.viruses:
            current_virus.act(self.Immune_cells, self.flow_field)

    def bone_healing(self):
        viruses_in_radius = 0
        for current_virus in self.viruses:
            virus_distance = self.flow_field.get((current_virus.cell_x, current_virus.cell_y), 999)
            if virus_distance <= INFECTION_RADIUS:
                viruses_in_radius += 1

        self.current_heal_speed = HEAL_SPEED
        if viruses_in_radius >= INFECTION_virus:
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
            win_text = f"BONE HEALED \n Stats: Immune_cells: {TOTAL_Immune_cellS} \n Total viruses: {self.total_virus_defeated}"
            self.window.create_text((GRID_SIZE * CELL_SIZE) // 2, (GRID_SIZE * CELL_SIZE) // 2, text=win_text,
                                    fill="white", font=("Arial", 24, "bold"))
            self.capture_frame()
            self.recording = False
            self.save_gif()
            return True

        for current_virus in self.viruses:
            virus_distance = self.flow_field.get((current_virus.cell_x, current_virus.cell_y))
            if virus_distance == 0:
                self.window.delete("all")
                self.window.configure(bg="red")
                lose_text = f"INFECTED \n Stats: Immune_cells: {TOTAL_Immune_cellS} \n Total viruses: {self.total_virus_defeated}"
                self.window.create_text((GRID_SIZE * CELL_SIZE) // 2, (GRID_SIZE * CELL_SIZE) // 2, text=lose_text,
                                        fill="black", font=("Arial", 20, "bold"))
                self.capture_frame()  # capture final frame
                self.recording = False
                self.save_gif()
                return True

        return False

    def update_ui(self):
        wave_num = (self.total_ticks // TICKS_PER_CYCLE) + 1

        if self.enable_Antiviral:
            Antiviral_text = f"Antiviral Cycles: {self.Antiviral.num_Antiviral}"
        else:
            Antiviral_text = "No Antivirals"

        display_text = f"Wave: {wave_num} | Spawn Rate: {self.current_spawn_amount} | Active viruses: {len(self.viruses)} | {Antiviral_text}"
        self.window.itemconfig(self.wave_info, text=display_text)
        self.window.tag_raise(self.wave_info)

    def record_data(self):
        self.history_time.append(self.total_ticks)
        self.history_viruses.append(len(self.viruses))

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

        if self.enable_Antiviral:
            self.current_spawn_amount = self.Antiviral.apply(self.total_ticks, self.current_spawn_amount)

        self.virus_spawn()
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
        self.capture_frame()
        self.main_window.after(UPDATE_SPEED, self.game_loop)

    def start_game(self):
        self.game_loop()