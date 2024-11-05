class OpeningTree:
    def __init__(self, state_dict):
        self.state = "init"
        self.state_dict = state_dict

    def move(opp_move):
        raise NotImplementedError
    
class VaudOpeningSystem(OpeningTree):
    def __init__(self) -> None:
        state_dict = {
            "init": {
                "init": "d2d4",
                "else": "d7d6"
            },
            "init_d2d4": {
                "e7e5": "d4e5",
                "g7g5": "c1g5",
                "else": "c1f4"
            },
            "init_d2d4_d4e5": {
                "d7d6": "e5d6",
                "b8c6": "g1f3"
            },
            "init_d2d4_c1f4": {
                "e7e5": "d4e5",
                "c7c5": "c2c3",
                "else": "e2e3"
            },
            "init_d2d4_c1f4_e2e3": {
                "else": "g1f3"
            },
            "init_d2d4_c1f4_e2e3_g1f3": {
                "else": "f1d3"
            },
            "init_d2d4_c1f4_e2e3_g1f3_f1d3": {
                "else": "c2c3"
            },
            "init_d2d4_c1f4_e2e3_g1f3_f1d3_c2c3": {
                "else": "b1d2"
            },
            "init_d2d4_c1f4_e2e3_g1f3_f1d3_c2c3_b1d2": {
                "else": "d1c2"
            },
            "init_d7d6": {
                "e4e5": "d6e5",
                "else": "g8f6"
            },
            "init_d7d6_g8f6": {
                "e4e5": "d6e5",
                "else": "g7g6"
            },
            "init_d7d6_g8f6_g7g6": {
                "e4e5": "d6e5",
                "else": "f8g7"
            },
            "init_d7d6_g8f6_g7g6_f8g7": {
                "e4e5": "d6e5",
                "else": "e8g8"
            },
        }
        super().__init__(state_dict)

    def move(self, opp_move):
        opp_move = str(opp_move)
        move = None
        if self.state in self.state_dict:
            if opp_move in self.state_dict[self.state]:
                move = self.state_dict[self.state][opp_move]
            elif "else" in self.state_dict[self.state]:
                move = self.state_dict[self.state]["else"]
        if not move:
            return "$END$"
        self.state += f"_{move}"
        return move
        