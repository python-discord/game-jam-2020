import json
import arcade


class Score:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.path = "./score.json"
        self.score_dict = {}
        self.index = -1
        self.char_count = 0
        self.restart_timer = -1

    def load_score(self, player_score):
        with open(self.path) as file:
            self.score_dict = json.load(file)

        if (
            player_score > int(list(self.score_dict.keys())[-1])
            and str(player_score) not in self.score_dict
        ):
            self.score_dict[str(player_score)] = "___"
            dum = [int(x) for x in list(self.score_dict.keys())]
            self.score_dict.pop(str(sorted(dum)[0]))

            new_score = {}
            key_list = [int(x) for x in list(self.score_dict.keys())]
            for score in sorted(key_list, reverse=True):
                new_score[str(score)] = self.score_dict[str(score)]
            self.score_dict = new_score

            self.index = list(self.score_dict.keys()).index(str(player_score))
        else:
            self.restart_timer = 0

    def draw_score_screen(self):

        arcade.draw_text(
            "- HIGH SCORE -",
            self.width // 2 - 155,
            self.height - self.height // 10 - 10,
            arcade.color.RUBY_RED,
            40,
        )
        count = 1
        for value, item in self.score_dict.items():
            count += 1
            if count - 2 == self.index:
                arcade.draw_text(
                    f"* {value}  -   {item}",
                    self.width // 2 - 40 - 20 * len(value),
                    self.height - (self.height // 10) * count,
                    arcade.color.YELLOW,
                    30,
                )
            else:
                arcade.draw_text(
                    f" {value}  -   {item}",
                    self.width // 2 - 20 - 20 * len(value),
                    self.height - (self.height // 10) * count,
                    arcade.color.RED_DEVIL,
                    30,
                )
        if self.restart_timer >= 0:
            arcade.draw_text(
                "Press a key to play again",
                self.width // 2 - 185,
                self.height // 9,
                arcade.color.YELLOW_ORANGE,
                30,
            )

    def score_input(self, char: str):
        if self.restart_timer > 1.5:
            return True
        elif self.index >= 0 and self.char_count < 3 and char.isalpha():

            score = list(self.score_dict.keys())[self.index]
            name = list(self.score_dict.values())[self.index]
            self.score_dict.pop(score)
            replace_name = list(name)
            replace_name[self.char_count] = char.upper()
            replace_name = "".join(replace_name)
            self.score_dict[score] = replace_name

            new_score = {}
            key_list = [int(x) for x in list(self.score_dict.keys())]
            for score in sorted(key_list, reverse=True):
                new_score[str(score)] = self.score_dict[str(score)]
            self.score_dict = new_score
            self.char_count += 1

            if self.char_count == 3:
                with open("score.json", "w") as file:
                    json.dump(self.score_dict, file)
                self.restart_timer = 0
            return False

        return False
