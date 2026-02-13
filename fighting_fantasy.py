import random


def roll():
    return random.randint(1, 6)


class Character:
    def __init__(self, is_dead: bool = False, score: int = 0, roll: int = 0,
                 stamina: int = 10, skill: int = 0, name: str = 'player'):
        self._is_dead = is_dead
        self._stamina = stamina
        self.score = score
        self.roll = roll
        self.skill = skill
        self.name = name

    def __repr__(self):
        return f"Character('{self.name.capitalize()}', skill={self.skill}, stamina={self.stamina})"

    def __str__(self):
        return f"{self.name.capitalize()}"

    # ---- Property handling stamina & is_dead logic ----
    @property
    def stamina(self):
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        self._stamina = max(0, value)
        if self._stamina == 0:
            self._is_dead = True

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

    # ---- Core logic ----
    def find_score(self):
        self.roll = random.randint(1, 12)
        self.score = self.roll + self.skill

    def wound(self, amount: int = 0):
        self.stamina -= amount
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

    def return_roll_status(self, a: int = 1, b: int = 6):
        self.roll = random.randint(a, b)
        total = self.roll + self.skill
        return f"{self.name.capitalize()} rolled {self.roll} for a total score of {total}"


class PlayerCharacter(Character):
    def __init__(self, name: str, skill: int, stamina: int, luck: int):
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
    def __init__(self, game_over: bool = False, round_result: bool = False,
                 opponent: 'Character' = None, player: 'PlayerCharacter' = None):
        self.game_over = game_over
        self.round_result = round_result
        self.opponent = opponent
        self.player = player


    def choose_opponent(self):
        opponents = [
            Character(name='Skeleton', skill=5, stamina=6),
            Character(name='Goblin', skill=4, stamina=5),
            Character(name='Orc', skill=6, stamina=8)
        ]
        self.opponent = random.choice(opponents)

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
        msg = (f"{self.player.name} rolled {self.player.roll} for a total score of {self.player.score}\n"
               f"{self.opponent.name} rolled {self.opponent.roll} for a total score of {self.opponent.score}\n")

        if self.round_result == "won":
            msg += "Player won this round\n"
        elif self.round_result == "lost":
            msg += "Player lost this round\n"
        else:
            msg += "This round was a draw\n"
        return msg


def get_choice(prompt, valid_choices):
    """Helper function to get validated user input.
    
    Args:
        prompt: The prompt to display to the user
        valid_choices: List of valid single-character choices
    
    Returns:
        The validated choice
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        valid_str = "' or '".join(valid_choices)
        print(f"Invalid choice. Please enter '{valid_str}'.")


def print_banner(title):
    """Print a formatted banner with title.
    
    Args:
        title: The title text to display in the banner
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    """Main game loop for Fighting Fantasy."""
    print("=" * 60)
    print("Welcome to Fighting Fantasy!")
    print("=" * 60)
    print()
    
    # Get player name
    player_name = input("Enter your character's name: ").strip()
    if not player_name:
        player_name = "Hero"
        print("Using default name: Hero")
    
    # Generate player character
    player = PlayerCharacter.generate_player_character(player_name)
    print(f"\n{player}")
    print(f"Skill: {player.skill}, Stamina: {player.stamina}, Luck: {player.luck}")
    print()
    
    # Game statistics
    battles_won = 0
    battles_fought = 0
    
    # Main game loop
    while True:
        print_banner("A new opponent appears!")
        
        # Create new game with opponent (reset game state for each battle)
        game = Game()
        game.choose_opponent()
        game.set_player(player)
        
        print(f"\nYou encounter a {game.opponent.name}!")
        print(f"{game.opponent.name} - Skill: {game.opponent.skill}, Stamina: {game.opponent.stamina}")
        print()
        
        # Combat loop
        round_num = 1
        fled = False
        while not game.game_over:
            print(f"\n--- Round {round_num} ---")
            
            # Ask player if they want to fight or flee
            choice = get_choice("Do you want to (f)ight or (r)un away? ", ['f', 'r'])
            
            if choice == 'r':
                print(f"\nYou flee from the {game.opponent.name}!")
                print("Your adventure ends here...")
                fled = True
                break
            
            # Resolve combat round
            game.resolve_fight_round()
            print(game.return_round_result())
            print(game.return_characters_status())
            
            round_num += 1
        
        # Only count as a battle if player didn't flee
        if not fled:
            battles_fought += 1
        
        # Check outcome
        if fled:
            print_banner("GAME OVER")
            print(f"\nYou fought in {battles_fought} battle(s) and won {battles_won}.")
            break
        elif player.is_dead:
            print_banner("YOU HAVE DIED!")
            print(f"\nYou fought bravely in {battles_fought} battle(s) and won {battles_won}.")
            print("Your adventure has come to an end.")
            break
        elif game.opponent.is_dead:
            battles_won += 1
            print(f"\nVictory! You have defeated the {game.opponent.name}!")
            print(f"\nBattles fought: {battles_fought}, Battles won: {battles_won}")
            
            # Ask if player wants to continue
            continue_game = get_choice("\nDo you want to continue your adventure? (y/n): ", ['y', 'n'])
            if continue_game == 'n':
                print_banner("CONGRATULATIONS!")
                print(f"\nYou survived {battles_fought} battle(s) and won {battles_won}!")
                print(f"Final stats - Skill: {player.skill}, Stamina: {player.stamina}, Luck: {player.luck}")
                print("\nYou retire from adventuring as a legend!")
                break
    
    print("\nThank you for playing Fighting Fantasy!")


if __name__ == "__main__":
    main()
