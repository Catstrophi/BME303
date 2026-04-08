"""
Creates the enemy class. Takes in health, damage, attack range, and position
Like tower we create the enemy shape and adds the hp.

Then we create two functions the take damage and act

The first function take damage just updates the hp based on damage done like the tower.

The act function is different. It first defines how the enemy attack then defines how it moves.
    We have this together because we dont want the enemy to attack and move at the same time. Furthermore, I also created a pathfind
    algorithm so its easier to have these together.

        I want the enemy to pathfind to the center of the grid which is the center of the fracture.
        However, if there is a tower within x range, it goes to the tower instead.

act function:
    Takes as list of all the towers and checks if there is a tower nearby.
        If tower in its detection/attack range:
            It will attack the tower
        If there is not a tower in that range:
            It will follow the flow field.

Then we want to place this enemy. I want them to spawn randomly around the edge of the grid. So I randomly chose top, bottom,
        right, or left and place the enemy there.
"""

import random

class Enemy:
    def __init__(self, window, health, damage, detect_range, cell_x, cell_y, cell_size):
        self.window = window
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.health = health
        self.damage = damage
        self.detect_range = detect_range
        self.cell_size = cell_size
        self.pixel_x = cell_x* self.cell_size
        self.pixel_y = cell_y * self.cell_size

        offset = self.cell_size

        # Create the enemy shape
        self.shape = window.create_rectangle(self.pixel_x - offset, self.pixel_y - offset,
                                             self.pixel_x + offset, self.pixel_y + offset, fill="red", outline="")

        # Add the hp
        self.hp = window.create_text(self.pixel_x, self.pixel_y, text=str(self.health), fill="white", font=("Arial", 7, "bold"))

    # Take damage function
    def take_damage(self, amount):

        # Decrease health
        self.health -= amount

        # If hp = 0, remove enemy
        if self.health <= 0:
            self.window.delete(self.shape)
            self.window.delete(self.hp)

        # Update hp
        else:
            self.window.itemconfig(self.hp, text=str(self.health))

    def act(self, towers, flow_field):
        # If not health stop, same thing with towers, tick update is not good, creates "ghost enemy"
        if self.health <= 0:
            return

        # Checks if there is any nearby towers
        nearby_towers = []

        for tower in towers:
            dist_x = abs(self.cell_x - tower.cell_x)
            dist_y = abs(self.cell_y - tower.cell_y)

            # Uses the same Chebyshev Distance
            if dist_x > dist_y:
                current_dist = dist_x
            else:
                current_dist = dist_y

            if current_dist <= self.detect_range:
                nearby_towers.append(tower)

        # Goes through all the nearby towers we found
        if len(nearby_towers) > 0:
            target = None

            shortest_dist = 999  # Start with a very large number, this is reference for flow map

            for tower in nearby_towers:

                dist_x = abs(self.cell_x - tower.cell_x)
                dist_y = abs(self.cell_y - tower.cell_y)

                if dist_x > dist_y:
                    d = dist_x
                else:
                    d = dist_y

                if d < shortest_dist:
                    shortest_dist = d
                    target = tower

            # Apply damage and draw attack
            target.take_damage(self.damage)
            laser = self.window.create_line(self.pixel_x, self.pixel_y, target.pixel_x, target.pixel_y, fill="purple", width=3)
            # Delete laser after a short delay
            self.window.after(100, lambda: self.window.delete(laser))
            return  # Stop because we don't want to move when we attack

        # If there are no towers nearby we move

        # Sets basic conditions for the flow field
        best_dist = 999999
        best_cell_x = None
        best_cell_y = None

        # Check Up
        check_x = self.cell_x
        check_y = self.cell_y - 1
        if (check_x, check_y) in flow_field:
            if flow_field[(check_x, check_y)] < best_dist:
                best_dist = flow_field[(check_x, check_y)]
                best_cell_x = check_x
                best_cell_y = check_y

        # Check Down
        check_x = self.cell_x
        check_y = self.cell_y + 1
        if (check_x, check_y) in flow_field:
            if flow_field[(check_x, check_y)] < best_dist:
                best_dist = flow_field[(check_x, check_y)]
                best_cell_x = check_x
                best_cell_y = check_y

        # Check Left
        check_x = self.cell_x - 1
        check_y = self.cell_y
        if (check_x, check_y) in flow_field:
            if flow_field[(check_x, check_y)] < best_dist:
                best_dist = flow_field[(check_x, check_y)]
                best_cell_x = check_x
                best_cell_y = check_y

        # Check Right
        check_x = self.cell_x + 1
        check_y = self.cell_y
        if (check_x, check_y) in flow_field:
            if flow_field[(check_x, check_y)] < best_dist:
                best_dist = flow_field[(check_x, check_y)]
                best_cell_x = check_x
                best_cell_y = check_y

        # Move to the best position
        if best_cell_x is not None:
            self.cell_x = best_cell_x
            self.cell_y = best_cell_y

            # Recalculate pixel position
            self.pixel_x = self.cell_x * self.cell_size
            self.pixel_y = self.cell_y * self.cell_size

            # Move the rectangle and the text on the screen
            offset = self.cell_size

            self.window.coords(self.shape, self.pixel_x - offset, self.pixel_y - offset, self.pixel_x + offset,
                               self.pixel_y + offset)
            self.window.coords(self.hp, self.pixel_x, self.pixel_y)

"""
# Spawn enemy
def spawn_enemies(window, health, damage, detect_range, grid_size, count, cell_size):

    # Returns all enemies created
    enemies = []

    # Randomly spawn at the 4 edges of the grid, offset a little since it's a 2x2
    for i in range(count):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            cell_x = random.randint(1, grid_size - 2)
            cell_y = 1

        elif edge == 'bottom':
            cell_x = random.randint(1, grid_size - 2)
            cell_y = grid_size - 2

        elif edge == 'left':
            cell_x = 1
            cell_y = random.randint(1, grid_size - 2)

        elif edge == 'right':
            cell_x = grid_size - 2
            cell_y = random.randint(1, grid_size - 2)

        enemies.append(Enemy(window, health, damage, detect_range, cell_x, cell_y, cell_size))

    return enemies
"""
def spawn_single_enemy(window, health, damage, detect_range, grid_size, cell_size, random_index):
    # Randomly spawn at the 4 edges of the grid
    edge = random.choice(['top', 'bottom', 'left', 'right'])

    if edge == 'top':
        cell_x = random_index.randint(1, grid_size - 2)
        cell_y = 1
    elif edge == 'bottom':
        cell_x = random_index.randint(1, grid_size - 2)
        cell_y = grid_size - 2
    elif edge == 'left':
        cell_x = 1
        cell_y = random_index.randint(1, grid_size - 2)
    elif edge == 'right':
        cell_x = grid_size - 2
        cell_y = random_index.randint(1, grid_size - 2)

    return Enemy(window, health, damage, detect_range, cell_x, cell_y, cell_size)