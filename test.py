import unittest

from tournament import Tournament
from game import Game

class TestTournamentCLI(unittest.TestCase):
    from main import request_participant_count, request_participants

    def test_request_participant_count(self):
        pass

    def test_request_participants(self):
        pass

class TestGame(unittest.TestCase):
    # Milestone 3
    def test_game_update(self):
        test_game = Game("test", "start_time", "end_time", "unknown", "unknown")

        test_game.update("Team A", "Team B")
        assert test_game.player1 == "Team A"
        assert test_game.player2 == "Team B"

        test_game.update("Team C", "")
        assert test_game.player1 == "Team C"
        assert test_game.player2 == "Team B"

        test_game.update("", "Team D")
        assert test_game.player1 == "Team C"
        assert test_game.player2 == "Team D"

class TestTournament(unittest.TestCase):
    # Milestone 2
    def test_save_tournament(self):
        test_game = Game("test", "start_time", "end_time", "Team A", "Team B")
        test_game_two = Game("test", "start_time", "end_time", "unknown", "unknown")

        test_tournament = Tournament("test", [test_game, test_game_two])

        # utility mock provided by unittest to handle file opening
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            test_tournament.save()
            mock_file.assert_called_once_with('test.games', 'w')
            mock_file().write.assert_called_once_with(test_game.to_json_string())
            mock_file().write.assert_called_once_with(test_game_two.to_json_string())

    def load_tournament(self):
        test_game = Game("test", "start_time", "end_time", "Team A", "Team B")
        test_game_two = Game("test", "start_time", "end_time", "unknown", "unknown")

        # utility mock provided by unittest to handle file opening
        with patch('builtins.open', unittest.mock.mock_open(read_data = f'{test_game.to_json_string()}\n{test_game_two.to_json_string()}'))) as mock_file:
            new_tournament = Tournament.load_tournament("test")

            mock_file.assert_called_once_with('test.games', 'r')
            assert len(new_tournament.games) == 2
            assert new_tournament.games[0].to_json_string() == test_game.to_json_string()
            assert new_tournament.games[1].to_json_string() == test_game_two.to_json_string()
    
    # Milestone 3
    def test_tournament_update(self):
        test_game = Game("test", "start_time", "end_time", "Team A", "Team B")
        test_game_two = Game("test", "start_time", "end_time", "unknown", "unknown")

        test_tournament = Tournament("test", [test_game, test_game_two])

        test_tournament.update(1, "", "New Player")
        assert test_game_two.player2 == "New Player"
        assert test_game_two.player1 == "unknown"
        assert test_game.player1 == "Team A"
        assert test_game.player2 == "Team B"

        with self.assertRaises(IndexError):
            test_tournament.update(2, "A", "B")

class TestEvenBriteClient(unittest.TestCase):
    from event_brite_client import EventBriteAPIHelper

    def test_update_event(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data = "fake_api_key")):
            client = EventBriteAPIHelper()

            client.update_event('some_id', 'new title', 'new description', 'new start_time', 'new end_time')

            request = Mock()

            request.urlopen.assertCalledWith(None)

class TestScheduler(unittest.TestCase):
    sys.modules['event_brite_client'] = Mock()
    from scheduler import Scheduler

    def test_schedule_tournament(self):
        test_game = Game("test", "start_time", "end_time", "Team A", "Team B")
        test_game_two = Game("test", "start_time", "end_time", "unknown", "unknown")

        test_tournament = Tournament("test", [test_game, test_game_two])

        scheduler = Scheduler()
        scheduler.schedule_tournament()

        assert scheduler.client.create_event.call_count == len(tournament.games)

    def test_update_game_event(self):
        test_game = Game("test", "start_time", "end_time", "Team A", "Team B")
        scheduler = Scheduler()

        scheduler.update_game(test_game)

        scheduler.client.update_event.assert_called_once()

if __name__ == "__main__":
    unittest.main()
