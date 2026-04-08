import tkinter as tk
import random
import matplotlib.pyplot as plt
from Game_Variables import UPDATE_SPEED
from Bone_GameV4 import Bone_Game


def plot_results(game_control, game_vaccine):

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle('Bone Defense: Control vs. Vaccine Comparison', fontsize=16)

    for i in range(len(game_control.history_time)):
        game_control.history_time[i] = (game_control.history_time[i] * UPDATE_SPEED) / 1000

    for i in range(len(game_vaccine.history_time)):
        game_vaccine.history_time[i] = (game_vaccine.history_time[i] * UPDATE_SPEED) / 1000

    # Top Graph: Number of Enemies
    ax1.plot(game_control.history_time, game_control.history_enemies, color='black', label='Control (No Vaccine)')
    ax1.plot(game_vaccine.history_time, game_vaccine.history_enemies, color='blue', label='Experimental (With Vaccine)')
    ax1.set_title('Active Enemies Over Time')
    ax1.set_ylabel('Number of Enemies')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Middle Graph: Bone Healing %
    ax2.plot(game_control.history_time, game_control.history_healing, color='black', label='Control (No Vaccine)')
    ax2.plot(game_vaccine.history_time, game_vaccine.history_healing, color='blue', label='Experimental (With Vaccine)')
    ax2.set_title('Bone Healing Progress')
    ax2.set_ylabel('Healing Completion (%)')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()

    # Bottom Graph: Heal Speed Penalty
    ax3.plot(game_control.history_time, game_control.history_heal_speed, color='black', label='Control (No Vaccine)')
    ax3.plot(game_vaccine.history_time, game_vaccine.history_heal_speed, color='blue', label='Experimental (With Vaccine)')
    ax3.set_title('Healing Delay (Infection Penalty)')
    ax3.set_xlabel('Time (S)')
    ax3.set_ylabel('Ticks Required per Heal (Lower is Faster)')
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.legend()

    plt.tight_layout()
    plt.show()


def main():
    root = tk.Tk()
    root.title("Bone Defense - Independent Clocks")

    same_random_index_code = random.randint(0, 1000000)

    # Tracker for when both games finish
    games_finished = 0

    # The callback function given to both games
    def check_all_finished():

        nonlocal games_finished
        games_finished += 1

        if games_finished == 2:
            plot_results(game_control, game_vaccine)

    # Control Game Frame
    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)
    tk.Label(left_frame, text="Control (No Vaccine)", font=("Arial", 16, "bold")).pack()
    game_control = Bone_Game(left_frame, enable_vaccine=False, rindex_code=same_random_index_code, is_finished=check_all_finished)

    # Experimental Game Frame
    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    tk.Label(right_frame, text="Experimental (With Vaccine)", font=("Arial", 16, "bold")).pack()
    game_vaccine = Bone_Game(right_frame, enable_vaccine=True, rindex_code=same_random_index_code, is_finished=check_all_finished)

    # Start Game
    game_control.start_game()
    game_vaccine.start_game()

    root.mainloop()


if __name__ == "__main__":
    main()