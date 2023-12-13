# Project Overview

> Note: The test cases do not fully encompass the functionality of everything
> described in all the milestones. You should **NOT** assume that if the
> auto-grader gives you full correctness score, that you have completed all the
> assignment requirements.  You should manually test your work to ensure you are
> meeting all the requirements, and/or create additional test cases to testing
> anything that isn't already tested.

We will build a Command-Line tool that lets you organize a tournament! Say you
want to organize a dance-off, a chess competition, or any other kind of
competition you can think of. Our tool will help you do that.

Your tournament's information will be saved in a file, so we can modify it
later.

We will also use the Eventbrite API to schedule all the games in our tournament!

We will provide you with a lot of code already, but it's up to you to make the
following key features happen over the following milestones

## Milestone 1: Understanding the code you are provided

### `main.py`

This is where we define our Command Line Interface (CLI for short). This is
where we start our tool, and you should run this now and get familiar with how
it works.

In particular, right now it will break, a lot. We will improve on it throughout
the milestones

In particular, make sure you are comfortable with the experience:

- We first ask the user if they want to create a new tournament or edit an
  existing one.

### `game.py` and `tournament.py`

These are our main abstractions, so make sure to read through them carefully.

The `Game` class keeps track of basic information about a `Game`: When the event
starts, when the event ends, and the two players competing.

The `Tournament` class keeps track of higher-level information about the
tournament such as its name, and all the scheduled games.

### `eventbrite_client.py`

This is the class that knows how to use the Eventbrite API. No need to read
through it yet, we will have a whole milestone dedicated to it.

### `untested_helpers.py`

As you will have noticed looking at the other files, many of them import
functions from the untested_helpers.py file

Your first task is to write unit tests for _every_ function defined in
untested_helpers.py.

As a rule of thumb, you should not blindly trust any untested code provided to
you, and this applies to this project as well. Read through the comments on each
function, and write corresponding unit tests before moving on to Milestone 2

Create a new file called `milestone1_tests1.py` and set up your tests there. Do
not overwrite or modify the provided `test.py`

## Milestone 2: Saving and Loading tournaments

### Part 1: gathering the right data

Let's look at the `tournament_setup` method in `main.py`.

1. We first ask for a tournament name.
2. We then ask for the participant count - this may be useful, as for our style
   of tournament to work, we need the number of participants to be a power of
   two.
3. We then create an empty list.
4. Then we ask our tournament object to create the games using that empty list.

That will not work. Let's fix these two issues:

#### Valid participant count

Complete the `request_participant_count` function in `main.py`. This function
should request user input; but only accept numbers that are power of two.

You can draw inspiration from the `request_integer_input` method, and use any
helpers already available in the code.

#### Valid participants

Complete the `request_participants` function in `main.py`. This function should
return a list of participants. That list should have as many items as the
participant count, and all those items must be unique.

You will prompt the user for participants but should repeat that prompt if the
participant was already provided.

You should be able to generate a similar experience as the two examples below:

```text
> How many participants? 2
> Please provide a participant: Magnus
> Please provide a participant: Fabiano
> Done
```

```text
> How many participants? 2
> Please provide a participant: Magnus
> Please provide a participant: Magnus
> Please provide a participant: Fabiano
> Done
```

Note how when we entered Magnus a second time, we received another prompt.
That's what your code should be able to do.

### Part 2: Saving the game

#### The abstraction

We're finally getting into the heart of the tournament, so let's think about our
abstractions in more detail.

A `Game` can refer to any sport or activity that engages two players or two
teams. Our `Game` objects will need to keep track of a few important
information:

- Player 1 and Player 2. These are simple strings that tell us who will be
  participating in a game.
- A start time and an end time. Each game should know when it begins, and when
  it should end.
- A name: This is a short description of the game that we can display. In
  particular, this should tell us how the game fits into the competition. a
  game's name could be "Round of 32 Game 5" or "Final Game 1"

A `Tournament` is a collection of games. First of all, though, we want to give
our tournament a name: This tells us what the event is: Are we doing a race? a
freestyle dance competition? are we playing Scrabble?

The `Tournament` object will be responsible for creating all the necessary
`Game` objects. To do that though, it will need some extra information:

- A start date: This lets us know when the first games should be scheduled. (In
  the provided code, this is hard-coded to start the day after you create the
  tournament in the CLI)
- An interval: This lets us know how many days to wait between rounds (This is
  hard-coded to be two days in the provided code).
- A game duration: This lets us know how long each game should run, so we can
  compute the end time for games. (This is also currently hard-coded)

The kind of tournament we will create is called a [single-elimination
tournament](https://en.wikipedia.org/wiki/Single-elimination_tournament). We
trust this `Tournament` class to know how to create all the right games, given
the info above and a list of participants.

Let's make sure that information is saved so we can reload it. Our format for
this will be as follows.

- When saving, create a file with the name: `tournament_name.games`.
- In the file, write each of the games stored in the tournament.

Read through the `Game` class, and look at the `to_json_string` method, you can
use it to complete the `Tournament` class' `save` method

You should be able to create a tournament now, let's call it test_tournament,
then see that a test_tournament.games file was created, which contains all the
games needed

By this stage, the `test_save_tournament` should be passing when you run unit
tests

### Part 3: Loading the game

What good is saving if we can't load? Our CLI is already set up to ask the user
to provide a tournament name. we need to complete the `load_tournament` method:

This method should look for the right file. If we want to load the
_summer_event_ tournament, then we will look for `summer_event.games`

Once found, we should read and recreate all the games stored in the file. You
can use the `from_json_string` method of the `Game` class to support that.

You can then return a new tournament object that contains all those games!

You should select option #2 in the CLI, and see that after closing the program,
you can load a tournament and see all its games!

By this stage, the `test_load_tournament` should be passing when you run unit
tests

## Milestone 3: Updating the tournament

As the tournament progresses, and we play games, we will want to update games
with no known players.

Look at the `tournament_changes()` method in `main.py` and read through it
carefully. We will continue where we left off from the previous milestone:

- Complete the `update_game` method in the `Tournament` class.
- This method should rely on the `update` method in the `Game` class.
- Don't forget that we need all of this saved on file! make sure that the file
  for your tournament is updated accordingly

By this stage, the `test_tournament_update` and `test_game_update` should be
passing when you run unit tests

## Milestone 4: To the internet

Let's step away from thinking about games and tournaments and files and all of
that. One of our goals is to schedule events for our games on the internet, and
this milestone will focus on just that. If this was a team project, a team
member could've started here!

### Part 1: Getting set up with the Eventbrite API

- Go to [eventbrite.com](eventbrite.com) and create an account, then Sign In
- Under Account settings, click on Developer Links and go to the API Keys page
- Click the "Create API Key" button in the top right
- Fill out the form to request an API key, and submit it
  - For the application URL, enter https://kibo.school
  - For the application name, enter Kibo Programming 2 Project
  - For the description, enter Project for Programming 2
- Wait a few seconds,
- Click "Show API Key, client secret, and tokens"
- Copy the "private token".
- Create a file inside the files directory of the project (right next to the
  files like cli.py) called apikey.txt.
- Paste the "private token" into the apikey.txt file and save it.
- Note that apikey.txt will be ignored by git. You can't git add it and it won't
  be uploaded as part of your project.

(There will be some Python code that reads the contents of apikey.txt.  Please
reach out for assistance if you are having trouble with this part, it's just a
matter of navigating the Eventbrite website.)

Once you have `apikey.txt` set up, go ahead and run `event_brite_client.py`. If
everything goes well, you should see:

- Some string showing up in the console - that is the ID of the event we just
  created
- If you visit your Eventbrite page
  [here](https://www.eventbrite.com/organizations/home), you should see that a
  Test event was scheduled for May 2024!

### Part 2: Updating events

We provided a function to create events - You are welcome!

It is also here to serve as a _reference_, so you can create the function to
**update** events on your own!

For this milestone, you have to complete the `update_event` method of the
`EventBriteAPIHelper` class:

- Make sure to carefully read how the `create_event` method works first.
- Then build up the `update_event` method. Note that the URL you need to send
  the request to is documented
  [here](https://www.eventbrite.com/platform/api#/reference/event/update/update-an-event)
- Your method does not need to return anything.

Before moving forward, test this by running your method with the ID of the event
you've already created as an input!

By this stage, `test_update_event` should be passing when you run unit tests.

## Milestone 5: Putting it all together

At this stage, we have games and tournaments that we can save locally and it all
works ok. We have a class that knows how to create an event and how to update
it. Let's bring this all together so we have a fully working program!

### Part 1: The Scheduler class & Scheduling the tournament

To set up events for the tournament, we have created a file called
`scheduler.py`. Functions within this file will receive games as input, and call
the right methods from `EventBriteAPIHelper` to create the corresponding event.

Let's start with the `schedule_tournament` function. This should take a
tournament as an input, then _extract_ information from all its games, passing
them to the `create_event` method of `EventBriteAPIHelper`.

The big question is: When should we call the `schedule_tournament` method? That is up to
you to figure out. At the end of this step though you should be able to create a
brand new tournament, then go to your [Eventbrite
page](https://www.eventbrite.com/organizations/home) and see all the
corresponding events!

### Part 2: Updating Events

The next step is to finish the `update_game_event` method.... but wait

wait wait wait

We may have a problem here. To update a game, we need to know its event ID! We
could get the IDs from the calls to `create_event`, but we don't right now! We
have some work to do:

- Modify the `Game` `__init__` method so it can take an **optional** parameter
  for event_id
- Modify the `to_json_string` and `from_json_string` methods to also store the
  event_id
- Make sure that as you call `schedule_tournament`, each game is updated with
  its event_id.

You should be able to see the event ID stored within your local save file.

Once you've accomplished this, then finishing `update_game_event` should be very
similar to the work you did in the previous step. With this, you should be
able to create tournaments, load them, modify their games, and have all your
changes reflected on Eventbrite. Well done!

By this point, the `test_schedule_tournament` and `test_update_game_event` tests
should be passing. Congratulations on being done!

## Grading

### Correctness and Completeness (85 points)

Milestone 1:

- unit tests for power_of_two - **5 Points**
- unit_tests for compute_round_name  **5 Points**

Milestone 2:

- correct implementation of `request_participant_count`  **5 Points**
- correct implementation of `request_participants`  **5 Points**
- correct implementation of `save` **10 Points**
- correct implementation of `load` **10 Points**

Milestone 3:

- correct implementation of `game.update` **5 Points**
- correct implementation of `tournament.update_game` **5 Points**

Milestone 4:

- correct implementation of `update` **15 Points**

Milestone 5:

- correct revision of `Game` **5 Points**
- correct implementation of `scheduler.schedule_tournament` **10 Points**
- correct implementation of `scheduler.update_game_event` **5 Points**

### Coding Style (15 points)

| Criteria                            | Proficient                                        | Competent                                          | Developing                                       |
|-------------------------------------|---------------------------------------------------|----------------------------------------------------|--------------------------------------------------|
| **Coding Style**   ||||
| 1. Indentation and Formatting       | Code is consistently well-indented and follows PEP 8 formatting guidelines. | Code is mostly well-indented and follows PEP 8 guidelines with minor deviations. | Code lacks consistent indentation and does not follow PEP 8 guidelines. |
| 2. Naming Conventions               | Meaningful and consistent variable/function/class names following PEP 8 conventions. | Mostly meaningful names, with occasional inconsistencies. | Variable/function/class names are unclear or inconsistent. |
| 3. Comments and Documentation       | Comprehensive comments and clear documentation for major functions and complex logic. | Adequate comments explaining major sections of code. | Lack of comments or insufficient documentation. |
| 4. Appropriate Use of Language Constructs | Demonstrates advanced understanding and appropriate use of Python language constructs (e.g., list comprehensions, generators). | Generally applies language constructs correctly, with occasional lapses. | Misuses or misunderstands key language constructs. |