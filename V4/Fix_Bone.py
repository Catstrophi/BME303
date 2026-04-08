"""
This is an algorithm to fix the bone.

We first get the coordinates for the fracture sites, this is seperated from left and right

First, we when we rebuild the bone, we want to differentiate between the black outline and white bone
    So if the fracture repair y value is the very top or bottom, we make it black
    else we make it white

    We start from the very top and go down row by row.
    If the y value is in the fracture sites, we run

    we just add 1 to the x and determien if its black or white

    for the left side we go 1 past the center and the right is one less than the center
    alternates from left to right
"""

def fix_bone(window, cell_size, walls, left_piece_edge, right_piece_edge):
    center_x = (24 + 75) // 2

    for y in list(left_piece_edge.keys()):
        # Left side
        if left_piece_edge[y] < center_x:
            left_piece_edge[y] += 1
            new_x = left_piece_edge[y]

            # If it's the top or bottom edge, and it hasn't reached the center, paint the new edge black
            if (y == 46 or y == 53) and new_x != center_x + 1:
                window.create_rectangle(new_x * cell_size, y * cell_size, (new_x + 1) * cell_size,
                                        (y + 1) * cell_size, fill="black", outline="")

                walls.add((new_x, y))

            # Otherwise paint it white
            else:
                window.create_rectangle(new_x * cell_size, y * cell_size, (new_x + 1) * cell_size,
                                        (y + 1) * cell_size, fill="lightgray", outline="")

            return True

        # Right side
        if y in right_piece_edge and right_piece_edge[y] > center_x:
            right_piece_edge[y] -= 1
            new_x = right_piece_edge[y]


            # If it's the top or bottom edge, and it hasn't reached the center, paint the new edge black
            if (y == 46 or y == 53) and new_x != center_x - 1:
                window.create_rectangle(new_x * cell_size, y * cell_size, (new_x + 1) * cell_size,
                                        (y + 1) * cell_size, fill="black", outline="")

                walls.add((new_x, y))

            # Otherwise paint it white
            else:
                window.create_rectangle(new_x * cell_size, y * cell_size, (new_x + 1) * cell_size,
                                        (y + 1) * cell_size, fill="lightgray", outline="")

            return True
    return False