import sys
from tournament import Tournament

def starting_menu():
    print("*************************************************************")
    print("Welcome to our tournament management tool!")
    print("You can press '1' to create a new tournament")
    print("You can press '2' to edit the games of an existing tournament")
    print("You can press any other key to exit\n")

    operation = input("What would you like to do? ")

    if operation == '1':
        tournament_setup()
    elif operation == '2':
        tournament_changes()
    else:
        print("Thanks for using our tool! exiting now...")
        sys.exit()

def tournament_setup():
    tournament_name = input("\nWhat would you like to call your tournament? ")
    tournament = Tournament(tournament_name)

    # This should be improved in milestone 2
    participant_count = input("How many participants will enter this tournament? ")

    # This should be improved in milestone 2
    participants = []

    print("\nYour tournament is ready to be scheduled. Creating calendar invites now!")

    tournament.create_games(participants)
    print(f'{tournament=}')

    tournament.save()


    starting_menu()

def tournament_changes():
    tournament_name = input("What tournament would you like to modify? ")

    try:
        tournament = Tournament.load_tournament(tournament_name)
    except:
        print("Could not find the tournament, try again!")
        starting_menu()

    if not tournament.has_games():
        print("The tournament we found has no games on record!, exiting")
        starting_menu()

    for i, game in enumerate(tournament.games):
        print(f'Press - {i} to edit {game}')

    game_id = -1
    while game_id < 0 or game_id >= len(tournament.games):
        game_id = request_integer_input("Which game do you want to modify?  ")

    player_1 = input("Please enter the new player 1, or type enter not to change it: ")
    player_2 = input("Please enter the new player 2, or type enter not to change it: ")

    print("-----------------------")
    print("Saving your changes now")
    print("-----------------------")

    tournament.update_game(game_id, player_1, player_2)

    starting_menu()


# Milestone 2 part 1
# Must return a list of UNIQUE participants equal to the count
def request_participants(count):
    pass

# Milestone 2 part 1
# Must ask for input and only accept multiples of two
def request_participant_count():
    pass

""" Helpers:
"""
def request_integer_input(message):
    int_input = input(message).strip()
    while not int_input.isnumeric():
        print("Sorry, please make sure to type in a number")
        int_input = input(message).strip()

    return int(int_input)

if __name__ == '__main__':
    starting_menu()
