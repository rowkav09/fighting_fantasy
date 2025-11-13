import random


def roll():
    return random.randint(1,6)


class Character:
    def __init__(self,is_dead: bool = False,score:int = 0,roll:int = 0,stamina:int = 10,skill:int = 0,name: str = 'player'):
        self._is_dead = is_dead
        self.score = score
        self.roll = roll
        self._stamina = stamina
        self.skill = skill
        self.name = name

    def __repr__(self):
        return f"Character('{self.name.capitalize()}', skill={self.skill}, stamina={self.stamina})"

    def __str__(self):
        return f"{self.name.capitalize()}"

    @property
    def stamina(self):
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        self._stamina = max(0, value)

    @property
    def is_dead(self):
        return self._is_dead

    @is_dead.setter
    def is_dead(self, value):
        self._is_dead = value
        if value:
            self._stamina = 0
        else:
            if self._stamina == 0:
                self._stamina = 1

    def find_score(self):
        self.roll = random.randint(1,12)
        self.score = self.roll + self.skill

    def wound(self,amount: int = 0):
        self.stamina -= amount
        if self.stamina <= 0:
            self.is_dead = True
        return self.stamina

    def fight_round(self, dragon):
        self.find_score()
        dragon.find_score()
        if self.score > dragon.score:
            dragon.wound(2)
            result = 'won'
        elif self.score < dragon.score:
            self.wound(2)
            result = 'lost'
        else:
            result = 'draw'
        return result

    def return_character_status(self):
        return f"{self.name.capitalize()} has skill {self.skill} and stamina {self.stamina}"

    def return_roll_status(self,a:int = 1,b:int = 6):
        self.roll = random.randint(a,b)
        total = self.roll + self.skill
        return f"{self.name.capitalize()} rolled {self.roll} for a total score of {total}"


class PlayerCharacter(Character):
    def __init__(self, name:str, skill:int, stamina:int, luck:int):
        super().__init__(name=name, skill=skill, stamina=stamina)
        self.luck = luck

    def __repr__(self):
        return f"PlayerCharacter('{self.name}', skill={self.skill}, stamina={self.stamina}, luck={self.luck})"

    @classmethod
    def generate_player_character(cls, param):
        skill = roll() + 3
        stamina = roll() + roll() + 4
        luck = roll() + 4
        return cls(param, skill, stamina, luck)


class Game:
    def __init__(self,game_over:bool = False,round_result: bool = False,opponent: str = '',player:str = ''):
        self.game_over = game_over
        self.round_result = round_result
        self.opponent = opponent
        self.player = player

    def choose_opponent(self):
        enemies = [
            Character(name='Goblin', skill=4, stamina=6),
            Character(name='Orc', skill=6, stamina=8),
            Character(name='Skeleton', skill=5, stamina=6),
            Character(name='Troll', skill=7, stamina=10)
        ]
        self.opponent = random.choice(enemies)

    def set_player(self, pc):
        self.player = pc

    def resolve_fight_round(self):
        self.player.find_score()
        self.opponent.find_score()

        if self.player.score > self.opponent.score:
            self.opponent.wound(2)
            self.round_result = "won"
        elif self.player.score < self.opponent.score:
            self.player.wound(2)
            self.round_result = "lost"
        else:
            self.round_result = "draw"

        if self.player.is_dead or self.opponent.is_dead:
            self.game_over = True

    def return_characters_status(self):
        return (f"{self.player.name} has skill {self.player.skill} and stamina {self.player.stamina}\n"
                f"{self.opponent.name} has skill {self.opponent.skill} and stamina {self.opponent.stamina}")

    def return_round_result(self):
        player_line = f"{self.player.name} rolled {self.player.roll} for a total score of {self.player.score}\n"
        opp_line = f"{self.opponent.name} rolled {self.opponent.roll} for a total score of {self.opponent.score}\n"
        if self.round_result == "won":
            res = "Player won this round"
        elif self.round_result == "lost":
            res = "Player lost this round"
        else:
            res = "This round was a draw"
        return player_line + opp_line + res + "\n"
