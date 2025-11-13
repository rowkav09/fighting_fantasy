import pytest
import random
from fighting_fantasy import Character, PlayerCharacter, Game


class TestCharacter:
    @pytest.fixture
    def characters(self):
        random.seed(10_001)
        return [Character(name = 'orc', skill=5, stamina=12),
                Character(name = 'dragon', skill=8, stamina=15)]

    def test_characters(self, characters):
        orc, dragon = characters
        # Test that the orc and dragon character have been set up correctly
        assert orc.name.lower() == 'Orc'.lower()
        assert orc.skill == 5
        assert orc.stamina == 12

    def test_repr(self, characters):
        orc, dragon = characters
        assert orc.__repr__() == "Character('Orc', skill=5, stamina=12)"
        assert dragon.__str__() == "Dragon"

    def test_find_score(self, characters):
        orc = characters[0]
        orc.find_score()
        assert 0 < orc.roll > 7 
        assert orc.score == orc.roll + orc.skill

    def test_wound(self, characters):
        orc = characters[0]
        orc.wound(0)
        assert orc.stamina == 10
        orc.wound(1)
        assert orc.stamina == 9

    def test_fight_round(self, characters):
        orc, dragon = characters
        result = orc.fight_round(dragon)
        assert orc.roll == 4
        assert dragon.roll == 5
        assert dragon.score == 13
        assert result == 'lost'
        assert orc.stamina == 10
        assert dragon.stamina == 15

    def test_is_dead(self, characters):
        orc = characters[0]
        orc.wound(12)
        assert orc.is_dead

    def test_set_is_dead(self, characters):
        orc = characters[0]
        orc.is_dead = False
        assert orc.stamina == 12
        orc.is_dead = True
        assert orc.stamina == 0
        orc.is_dead = False
        assert orc.stamina == 1

    def test_return_character_status(self, characters):
        orc = characters[0]
        assert orc.return_character_status() == 'Orc has skill 5 and stamina 12'

    def test_return_roll_status(self, characters):
        dragon = characters[1]
        dragon.find_score()
        assert dragon.return_roll_status() == 'Dragon rolled 4 for a total score of 12'


class TestPlayerCharacter:
    def test_generate_pc(self):
        random.seed(10_001)
        pc = PlayerCharacter.generate_player_character("Sir Andrew")
        assert pc.skill == 9
        assert pc.stamina == 14
        assert pc.luck == 10
        assert pc.__repr__() == "PlayerCharacter('Sir Andrew', skill=9, stamina=14, luck=10)"


class TestGame:
    @pytest.fixture()
    def new_game(self):
        random.seed(10_001)
        game = Game()
        game.choose_opponent()
        pc = PlayerCharacter.generate_player_character("Sir Andrew")
        game.set_player(pc)
        return game

    def test_game(self, new_game):
        assert (new_game.player.__repr__()
                == "PlayerCharacter('Sir Andrew', skill=7, stamina=17, luck=11)")
        assert new_game.opponent.__str__() == "Skeleton"

    def test_resolve_fight_round(self, new_game):
        new_game.resolve_fight_round()
        assert new_game.round_result == "won"

    def test_return_characters_status(self, new_game):
        new_game.resolve_fight_round()
        assert new_game.return_characters_status() == ('Sir Andrew has skill 7 and stamina 17\n'
                                                       'Skeleton has skill 5 and stamina 6')

    def test_return_round_result(self, new_game):
        new_game.resolve_fight_round()
        round_msg = new_game.return_round_result()
        assert round_msg == ("Sir Andrew rolled 10 for a total score of 17\n"
                             "Skeleton rolled 6 for a total score of 11\n"
                             "Player won this round\n")

    def test_game_over(self, new_game):
        new_game.player.is_dead = True
        assert new_game.game_over
