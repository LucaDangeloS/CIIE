# CSV structure for regular spritesheets
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
Example:
width,16,height,32
walk,down,0,0,3,left,0,1,3,up,0,2,3,right,0,3,3
idle,down,3,0,3,left,3,1,3,up,3,2,3,right,3,3,3

+ Maybe add a parameter that sets the time between animations?

# CSV structure for irregular spritesheets
Here the sprites will be indicated individually by pixel values.
The file will consist of a series of lines which have the following structure:
- The first value will be the name of the action that the entity is performing
- The second value will be the orientation
- The third value will be a number that indicates the amount of animations there are.
- The following values will be the rectangles dimensions (x,y,w,h) that surround said animations.




