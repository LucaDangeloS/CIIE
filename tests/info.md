For collisions, to test for rectangles colliding:
    Rect.collidelist
(we could even create a Rect around the mouse and check if it's selecting a button)

A Quadtree could also be used for collision detection:
    https://en.wikipedia.org/wiki/Quadtree

For the mouse collision with rectangles:
    pygame.rect.Rect.collidepoint(<mouse_pos>)
(this must be called form a rect, like:)
    rect1 = Rect(x, y, w, h)    
    rect1.collidepoint(<mouse_pos>)


To draw a **circle**:
    pg.draw.circle(screen, color, pos, radius)


**Rectangle points**:
topleft     midtop      topright
midleft     center      midright
bottomleft  midbottom   bottomright




