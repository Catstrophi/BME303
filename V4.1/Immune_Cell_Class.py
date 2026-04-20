"""
Creates a Immune_cell class. Takes in window, health, damage, attack range, and position.
There will be two positional variables:
        cell_x/cell_y - this is referring to the grid coordinate system.
                Used to calculate distance between virus and Immune_cell

        pixel_x/pixel_y - this is referring to the pixels. Python doesn't know what the grid is
        since I defined each grid to be x amount of pixels.
                Used to draw new shapes and objects on the window

First creates what a Immune_cell is, creates the range, and adds the hp.

Then it defines the attack and take damage function.
    It checks all viruses on the board. If any of them are are within a certain range do x amount of damage to them
    It removes x amount of damage from health and updates the health

Then it creates a function of place Immune_cell. I want the Immune_cell above and below the shaft but within the knobs of the bone.
    Then I automatically space them evenly
"""

import math

class Immune_cell:

    # Initializes Immune_cell class
    def __init__(self, window, health, damage, atk_range, cell_x, cell_y, cell_size):
        self.window = window
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.health = health
        self.damage = damage
        self.atk_range = atk_range
        self.cell_size = cell_size

        # pixel x/y is the amount of pixels to the location, cell x/y is the amount of cells
        self.pixel_x = cell_x * self.cell_size
        self.pixel_y = cell_y * self.cell_size

        # How much they should shift since python creates a rectangle by the top left and bottom_right.
        offset = (cell_size * 3) / 2

        # Creates the two and adds the hp on it
        self.shape = window.create_rectangle(self.pixel_x - offset, self.pixel_y - offset, self.pixel_x + offset, self.pixel_y + offset, fill="grey", outline="")
        self.hp = window.create_text(self.pixel_x, self.pixel_y, text=str(self.health), fill="black", font=("Arial", 7, "bold"))

    # Defines the attack function
    def attack(self, viruses):

        # First check if it's still standing, issue with tick update creating a "ghost" Immune_cell
        if self.health <= 0:
            return

        # Takes in a list of all the viruses and checks each virus
        for virus in viruses:

            # Uses the Chebyshev Distance for more efficiency. Calculate distance between Immune_cell and virus
            # If within range, virus will take damage, create a laser to show the attack, then remove laser
            if max(abs(self.cell_x - virus.cell_x), abs(self.cell_y - virus.cell_y)) <= self.atk_range:
                virus.take_damage(self.damage)
                laser = self.window.create_line(self.pixel_x, self.pixel_y, virus.pixel_x, virus.pixel_y, fill="orange", width=2)
                self.window.after(100, lambda: self.window.delete(laser))
                break

    # Immune_cell takes damage
    def take_damage(self, amount):
        self.health -= amount

        # If the health is 0, remove the Immune_cell
        if self.health <= 0:
            self.window.delete(self.shape)
            self.window.delete(self.hp)

        # Update the health
        else:
            self.window.itemconfig(self.hp, text=f"{self.health}")

# Add Immune_cells to the grid
def add_Immune_cells(window, health, damage, atk_range, total_Immune_cells, cell_size, health_list=None):

    # Creates a list of all the Immune_cell objects
    Immune_cell_list = []
    if health_list is None:
        health_list = []
        for i in range(total_Immune_cells):
            health_list.append(health)

    else:
        total_Immune_cells = len(health_list)

    # Splits the Immune_cells evenly for top and bottom
    top_count = math.ceil(total_Immune_cells / 2)
    bottom_count = math.floor(total_Immune_cells / 2)
    health_list_top = health_list[:top_count]
    health_list_bottom = health_list[top_count:]

    # Create a Immune_cell
    def create_Immune_cell(count, y_pos, health_list):
        if count == 0:
            return

        # The x bounds
        left_bound = 32
        right_bound = 67

        # Splitting up the distance evenly
        space_between = (right_bound - left_bound) / count

        # Add all Immune_cells. x position is calculated by adding a space between the x and then offsets it to find the center
        for i in range(count):
            x_pos = int(left_bound + (i * space_between) + (space_between / 2))
            Immune_cell_list.append(Immune_cell(window, health_list[i], damage, atk_range, x_pos, y_pos, cell_size))

    # Creates the Immune_cells on top and bottom
    create_Immune_cell(top_count, 40, health_list_top)
    create_Immune_cell(bottom_count, 59, health_list_bottom)

    return Immune_cell_list
