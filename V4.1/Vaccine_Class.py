from Game_Variables import VACCINE_TICK, VACCINE_EFFECT, UPDATE_SPEED

class Vaccine:
    def __init__(self, window):
        self.window = window
        self.num_vaccine = 0

    def apply(self, total_ticks, current_spawn_amount):
        # Define Vaccine (Ensures it doesn't trigger on tick 0)
        if total_ticks > 0 and total_ticks % VACCINE_TICK == 0:
            current_spawn_amount *= VACCINE_EFFECT
            self.window.config(bg="green")
            self.window.itemconfig("grid_line", outline="green")
            self.window.after(UPDATE_SPEED * 2, lambda: self.window.config(bg="white"))
            self.window.after(UPDATE_SPEED * 2, lambda: self.window.itemconfig("grid_line", outline="lightgrey"))

            self.num_vaccine = self.num_vaccine + 1

        return current_spawn_amount