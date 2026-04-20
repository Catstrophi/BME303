from Game_Variables import Antiviral_TICK, Antiviral_EFFECT, UPDATE_SPEED

class Antiviral:
    def __init__(self, window):
        self.window = window
        self.num_Antiviral = 0

    def apply(self, total_ticks, current_spawn_amount):
        # Define Antiviral (Ensures it doesn't trigger on tick 0)
        if total_ticks > 0 and total_ticks % Antiviral_TICK == 0:
            current_spawn_amount *= Antiviral_EFFECT
            self.window.config(bg="green")
            self.window.itemconfig("grid_line", outline="green")
            self.window.after(UPDATE_SPEED * 2, lambda: self.window.config(bg="white"))
            self.window.after(UPDATE_SPEED * 2, lambda: self.window.itemconfig("grid_line", outline="lightgrey"))

            self.num_Antiviral = self.num_Antiviral + 1

        return current_spawn_amount