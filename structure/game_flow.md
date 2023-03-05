# Basic overlook 

- Director: controls the event loop and handles the global state.
- Controller(s): transforms pygame events into our encoding, using events defined in ControllerInterface.
- Scenes: drawable objects capable of managing input.
    - Menu: primarly composed of buttons, with the main purpose of guiding the user throw different options.
    - Level: handles the elements of an actual game level.
      Includes the map generation, the drawing of the levels, the npcs behavior, the user input, and the player control (delegating on the player object).

- Player: manages the logic of the player using the ControllerInteface events as inputs to change its state.
    It delegates the selection of the right sprite to the Sprite_hanlder using the ActionEnum as the reference
    for all the possible actions that the player can do (animations must exist for each action)

- SpriteSheet: class to load spritesheets using different methods.

- Sprite_handler: takes care of selecting the right image for the action that the entity is performing based on the state = (ActionEnum, orientation) and the animation_step (time between animations) previously defined.
The internal representation is an *action dictionary* where every key(ActionEnum) is attached to an *orientation dictionary* that for each orientation has a list of pg.Surfaces with the animation sequence.

- Enemy: future work


# Usual game control flow
Director.running_loop()
    Level.handle_event(event_list)
        actions = self.controller.get_input(event_list)
        self.player.handle_input(actions)
    Level.update()
        self.player.update()
    Level.draw(self.screen)
        self.floor_tiles.draw_offsetted(self.player, screen) #the player is in this sprite_group
            screen.blit(sprite.image, offset_pos)


# Player internal design
In every frame the player **update** method is executed and the **handle_input** even if no input has been generated. 

For every frame we need to do the following things regarding the player:

- Apply the input (if it exists) changing the player internal state

- Update the player internal state taking into account the input and the previous player state.

- Update the player position using the internal state of the player (as well as the player image)

- Draw the player (this is delegated to the sprite group to which the player belongs)
    -> To make sure this works accordingly we just need to keep the self.image attribute of the player updated.



















