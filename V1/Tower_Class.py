"""
Creates a tower class. Takes in window, health, damage, attack range, and position.
There will be two positional variables:
        cell_x/cell_y - this is referring to the grid coordinate system.
                Used to calculate distance between enemy and tower

        pixel_x/pixel_y - this is referring to the pixels. Python doesn't know what the grid is
        since I defined each grid to be x amount of pixels.
                Used to draw new shapes and objects on the window

First creates what a tower is, creates the range, and adds the hp.

Then it defines the attack and take damage function.
    It checks all enemies on the board. If any of them are are within a certain range do x amount of damage to them
    It removes x amount of damage from health and updates the health

Then it creates a function of place tower. I want the tower above and below the shaft but within the knobs of the bone.
    Then I automatically space them evenly
"""

import math

class Tower:

    # Initializes Tower class
    def __init__(self, window, health, damage, atk_range, cell_x, cell_y, cell_size):
        self.window = window
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.health = health
        self.damage = damage
        self.atk_range = atk_range
        self.cell_size = cell_size

        # pixel x/y is the amount of pixels to the location, cell x/y is the amount of cells
        self.pixel_x = cell_x * cell_size
        self.pixel_y = cell_y * cell_size

        # How much they should shift since python creates a rectangle by the top left and bottom_right.
        offset = (cell_size * 3) / 2

        # Creates the two and adds the hp on it
        self.shape = window.create_rectangle(self.pixel_x - offset, self.pixel_y - offset, self.pixel_x + offset, self.pixel_y + offset, fill="grey", outline="")
        self.hp = window.create_text(self.pixel_x, self.pixel_y, text=str(self.health), fill="black", font=("Arial", 7, "bold"))

    # Defines the attack function
    def attack(self, enemies):

        # First check if its still standing, issue with tick update creating a "ghost" tower
        if self.health <= 0:
            return

        # Takes in a list of all the enemies and checks each enemy
        for enemy in enemies:

            # Uses the Chebyshev Distance for more efficiency. Calculate distance between tower and enemy
            # If within range, enemy will take damage, create a laser to show the attack, then remove laser
            if max(abs(self.cell_x - enemy.cell_x), abs(self.cell_y - enemy.cell_y)) <= self.atk_range:
                enemy.take_damage(self.damage)
                laser = self.window.create_line(self.pixel_x, self.pixel_y, enemy.pixel_x, enemy.pixel_y, fill="orange", width=2)
                self.window.after(100, lambda: self.window.delete(laser))
                break

    # Tower takes damage
    def take_damage(self, amount):
        self.health -= amount

        # If the health is 0, remove the tower
        if self.health <= 0:
            self.window.delete(self.shape)
            self.window.delete(self.hp)

        # Update the health
        else:
            self.window.itemconfig(self.hp, text=f"{self.health}")

# Add towers to the grid
def add_towers(window, health, damage, atk_range, total_towers, cell_size):

    # Creates a list of all the tower objects
    tower_list = []

    # Splits the towers evenly for top and bottom
    top_count = math.ceil(total_towers / 2)
    bottom_count = math.floor(total_towers / 2)

    # Create a tower
    def create_tower(count, y_pos):

        # The bx bounds
        left_bound = 32
        right_bound = 67

        # Splitting up the distance evenly
        space_between = (right_bound - left_bound) / count

        # Add all towers. x position is calculated by adding a space between the x and then offsets it to find the center
        for i in range(count):
            x_pos = int(left_bound + (i * space_between) + (space_between / 2))
            tower_list.append(Tower(window, health, damage, atk_range, x_pos, y_pos, cell_size))

    # Creates the towers on top and bottom
    create_tower(top_count, 40)
    create_tower(bottom_count, 59)

    return tower_list
