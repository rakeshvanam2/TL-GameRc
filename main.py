import os
import random
from pynput import keyboard


class RabbitGame():
    def __init__(self, map_length=50, debug=False):
        self.map_length = map_length
        self.debug = debug
        self.game_map = ["_" for _ in range(self.map_length)]
        self.game_state = {
            "carrot_picked": False,
            "game_complete": False,
            "game_esc_exit": False,
            "rabbit_hole_position_set": False,
            "rabbit_position_set": False
        }
        self.carrot_position = random.randint(0, self.map_length-1)
        self.game_map[self.carrot_position] = "c"

        # set random rabbit hole position and not place it on carrot or very next to carrot
        # otherwise rabbit cannot jump over two things
        self.rabbit_hole_position = random.randint(0, self.map_length-1)
        while not self.game_state["rabbit_hole_position_set"]:
            if (self.rabbit_hole_position != self.carrot_position and
                self.rabbit_hole_position != self.carrot_position - 1 and
                self.rabbit_hole_position != self.carrot_position + 1
            ):
                self.game_map[self.rabbit_hole_position] = "O"
                self.game_state["rabbit_hole_position_set"] = True
            else:
                self.rabbit_hole_position = random.randint(0, self.map_length - 1)

        # set random rabbit position not place it on carrot or hole
        self.rabbit_position = random.randint(0, self.map_length-1)
        while not self.game_state["rabbit_position_set"]:
            if (self.rabbit_position != self.carrot_position and
                self.rabbit_position != self.rabbit_hole_position
            ):
                self.game_map[self.rabbit_position] = "r"
                self.game_state["rabbit_position_set"] = True
            else:
                self.rabbit_position = random.randint(0, self.map_length - 1)

    def debug_init(self, carrot_position, rabbit_position, rabbit_hole_position):
        self.carrot_position = carrot_position
        self.rabbit_position = rabbit_position
        self.rabbit_hole_position = rabbit_hole_position
        self.game_map = ["_" for _ in range(self.map_length)]
        self.game_map[self.carrot_position] = "c"
        self.game_map[self.rabbit_position] = 'r'
        self.game_map[self.rabbit_hole_position] = 'O'

    def __on_press(self, key):
        try:
            if self.game_state["game_complete"] is False:
                if key == keyboard.KeyCode.from_char('p'):  # PICK OPTION
                    # check nearby for carrot and pick if not picked
                    if (self.rabbit_position - 1 == self.carrot_position or
                        self.rabbit_position + 1 == self.carrot_position) and (
                            self.game_state["carrot_picked"] is False
                    ):
                        self.game_map[self.carrot_position] = "_"
                        self.game_map[self.rabbit_position] = "R"
                        self.game_state["carrot_picked"] = True
                        self.carrot_position = -1  # carrot is now with rabbit
                    # also allow to drop the carrot if it is near hole
                    if (self.game_state["carrot_picked"] is True) and (
                            self.rabbit_position - 1 == self.rabbit_hole_position or
                            self.rabbit_position + 1 == self.rabbit_hole_position
                    ):
                        self.game_map[self.rabbit_position] = "r"
                        self.game_state["carrot_picked"] = False
                        self.game_state["game_complete"] = True
                        self.carrot_position = self.rabbit_hole_position  # carrot is in hole
                elif key == keyboard.KeyCode.from_char('j'):  # JUMP OPTION ONLY FOR RABBIT HOLE
                    # check nearby for rabbit hole
                    if (self.rabbit_position - 1 == self.rabbit_hole_position or
                        self.rabbit_position + 1 == self.rabbit_hole_position
                    ):
                        # make sure the hole is not at either end of the map
                        if (self.rabbit_hole_position != self.map_length - 1 and
                                self.rabbit_hole_position != 0):
                            if self.rabbit_position < self.rabbit_hole_position:
                                # if rabbit is left to hole, jump it to right
                                self.game_map[self.rabbit_position], self.game_map[self.rabbit_position + 2] = \
                                    "_", "R" if self.game_state["carrot_picked"] else "r"
                                self.rabbit_position = self.rabbit_position + 2  # update rabbit position to right
                            else:
                                # otherwise jump to left
                                self.game_map[self.rabbit_position], self.game_map[self.rabbit_position - 2] = \
                                    "_", "R" if self.game_state["carrot_picked"] else "r"
                                self.rabbit_position = self.rabbit_position - 2  # update rabbit position to left
                elif key == keyboard.KeyCode.from_char('a'):  # LEFT MOVE OPTION
                    # make sure the rabbit is not at beginning of the map
                    # cannot move across carrot or hole
                    if (self.rabbit_position != 0 and
                        self.rabbit_position - 1 != self.carrot_position and
                        self.rabbit_position - 1 != self.rabbit_hole_position
                    ):
                        # move to left
                        self.game_map[self.rabbit_position], self.game_map[self.rabbit_position - 1] = \
                            self.game_map[self.rabbit_position - 1], self.game_map[self.rabbit_position]
                        self.rabbit_position = self.rabbit_position - 1  # update rabbit position to left
                elif key == keyboard.KeyCode.from_char('d'):  # RIGHT MOVE OPTION
                    # make sure the rabbit is not at the end of the map
                    # cannot move across carrot or hole
                    if (self.rabbit_position != self.map_length - 1 and
                        self.rabbit_position + 1 != self.carrot_position and
                        self.rabbit_position + 1 != self.rabbit_hole_position
                    ):
                        # move to right
                        self.game_map[self.rabbit_position], self.game_map[self.rabbit_position + 1] = \
                            self.game_map[self.rabbit_position + 1], self.game_map[self.rabbit_position]
                        self.rabbit_position = self.rabbit_position + 1  # update rabbit position to right
                elif key == keyboard.Key.esc:
                    # let esc key exit on demand
                    self.game_state["game_complete"] = True
                    self.game_state["game_esc_exit"] = True

                # refresh screen
                os.system('cls' if os.name == 'nt' else 'clear')
                print("".join(self.game_map))
        except AttributeError as e:
            if not key == keyboard.Key.esc:
                print(e)
                print('special key {0} pressed'.format(key))

    def __on_release(self, key):
        # returning false will stop keyboard listener
        if key == keyboard.Key.esc:
            # esc_exit does not prompt to replay
            self.game_state["game_esc_exit"] = True
            return False
        elif self.game_state["game_complete"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            return False

    def start_game(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("".join(self.game_map))

        if not self.debug:
            with keyboard.Listener(
                    on_press=self.__on_press,
                    on_release=self.__on_release) as listener:
                listener.join()
        else:
            listener = keyboard.Listener(
                on_press=self.__on_press,
                on_release=self.__on_release)
            # Using start instead of `with` / `join` you create a
            # non-blocking thread allowing the main loop to start.
            listener.start()

        if self.game_state["game_esc_exit"]:
            print("Esc Exit")
            exit()

        if not self.debug:
            usr_input = str(input("Game Finished. Want to start over? (y/n) "))
            if usr_input[-1] == 'y' or usr_input[-1] == 'Y':
                return True
            elif usr_input[-1] == 'n' or usr_input[-1] == 'N':
                return False
            else:
                return False


def main():
    rabbit_game = RabbitGame()
    # for development purpose
    # rabbit_game.debug_init(carrot_position=40, rabbit_position=30, rabbit_hole_position=35)
    play_again = rabbit_game.start_game()
    while play_again is True:
        rabbit_game = RabbitGame()
        play_again = rabbit_game.start_game()
    exit()


if __name__ == "__main__":
    main()
