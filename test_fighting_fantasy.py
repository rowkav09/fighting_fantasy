import pytest
import random
from fighting_fantasy import Character, PlayerCharacter, Game


class TestCharacter:
    @pytest.fixture
    def characters(self):
        random.seed(10_001)
        return [Character(name='orc', skill=5, stamina=12),
                Character(name='dragon', skill=8, stamina=15)]

    def test_characters(self, characters):
        orc, dragon = characters
        assert orc.name.lower() == 'orc'
        assert orc.skill == 5
        assert orc.stamina == 12

    def test_repr(self, characters):
        orc, dragon = characters
        assert orc.__repr__() == "Character('Orc', skill=5, stamina=12)"
        assert dragon.__str__() == "Dragon"

    def test_find_score(self, characters):
        orc = characters[0]
        orc.find_score()
        assert 0 < orc.roll <= 12
        assert orc.score == orc.roll + orc.skill

    def test_wound(self, characters):
        orc = characters[0]
        orc.wound(0)
        assert orc.stamina == 12
        orc.wound(3)
        assert orc.stamina == 9

    def test_fight_round(self, characters):
        orc, dragon = characters
        random.seed(10_001)
        result = orc.fight_round(dragon)
        assert result in ['won', 'lost', 'draw']
        assert isinstance(result, str)

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
        msg = dragon.return_roll_status()
        assert 'Dragon rolled' in msg
        assert 'for a total score of' in msg


class TestPlayerCharacter:
    def test_generate_pc(self):
        random.seed(10_001)
        pc = PlayerCharacter.generate_player_character("Sir Andrew")
        assert isinstance(pc, PlayerCharacter)
        assert hasattr(pc, 'luck')
        assert pc.__repr__().startswith("PlayerCharacter('Sir Andrew'")


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
        assert isinstance(new_game.player, PlayerCharacter)
        assert isinstance(new_game.opponent, Character)

    def test_resolve_fight_round(self, new_game):
        new_game.resolve_fight_round()
        assert new_game.round_result in ["won", "lost", "draw"]

    def test_return_characters_status(self, new_game):
        new_game.resolve_fight_round()
        result = new_game.return_characters_status()
        assert new_game.player.name in result
        assert new_game.opponent.name in result

    def test_return_round_result(self, new_game):
        new_game.resolve_fight_round()
        round_msg = new_game.return_round_result()
        assert "rolled" in round_msg
        assert "total score" in round_msg

    def test_game_over(self, new_game):
        new_game.player.is_dead = True
        assert new_game.game_over or new_game.player.is_dead
