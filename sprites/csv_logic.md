# Csv structure
To mantain the information of what sprite does what, instead of hardcoding it on code, we are going to generate
a csv file per spritesheet.

The csv file will have the following structure:
- The first line will indicate the size of the sprite and the spacement between them (if needed)
- The following lines will specify the purpose of the sprite and the placement in the following manner:
    - First, the action will be specified as a string, such as walking, running, idle, etc.
    - The second value will correspond to the orientation of the sprite(left, right, up, down).
    - The three values that follow the sprite orientation specify:
        - The x index where the animation beigns inside the spritesheet. 
        - The y index where the animation begins inside the spritesheet.
        - The number of sprites that constitute the animation.

One line can have multiple orientation specifications, but only one action can be linked to a line.

+ Maybe add a parameter that sets the time between animations?

