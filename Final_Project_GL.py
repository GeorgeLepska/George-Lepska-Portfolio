"""
George Lepska
Intro to Programming: Section 6
4/17
"""

import time
import random

#character enters a room
#going to give character a scenerio (theres and items, theres a monster, etc
#if you get an item, it will increase health, strength, other stat
#if theres a monster {health: 3, strength:1}
#play game multiple times because each scenario is random and much can happen during game

def speak(text):
    """
    signature: int -> int
    delays the speed in which the text is presented
    """
    for line in text:
        print(line)
        time.sleep(text[line])
        
def battle(player, monster_name, monster):
    """
    signature: none -> dict
    how battle works in game. as player battles mob, the player health and mob health
    constantly update in dict form based on the strength. If player wins battle, player progresses
    to next stage, if player loses battle, end game message appears.
    """
    speak({f'As you enter, you notice a {monster_name} in the room ready for battle!':2})
    speak({'You begin to approach the monster.':1})
    monster_health, monster_strength = monster
    health = player['health']
    while player['health'] > 0 and monster_health > 0:
        speak({f'Your health: {player["health"]}':0.5,
              f'Monster health: {monster_health}':0.5})
        side = attack()
        damage = random.randint(1, player['strength'])
        speak({f'You attack to the {side}!':1,
              f'You deal {damage} damage!':1})
        monster_health -= player['strength']
        if monster_health > 0:
            damage = random.randint(1, monster_strength)
            speak({f'The monster attacks!':1,
                  f'It deals {damage} damage!':1})
            player['health'] -= monster_strength
    if monster_health <= 0:
        speak({'You deliver a blow that slays the monster!':1})
        player['health'] = health
        return True
    return False

def attack():
    """
    signature: int -> int
    user inputs what direction they want their player to attack. returns error
    statement if it is left, l, right, r is not inputted
    """
    l = ['left', 'l']
    r = ['right', 'r']
    side = input('Quick, which direction will you attack?!\n', )
    while side.lower() not in l and side.lower() not in r:
        speak({'Not a valid input! Try again!':0.25})
        side = input()
    if side.lower() in l:
        return 'left'
    else:
        return 'right'


def left_right():
    """
    signature: int -> int
    user inputs what door they want to open. returns error
    statement if it is left, l, right, r is not inputted
    """
    l = ['left', 'l']
    r = ['right', 'r']
    speak({'In front of you are two doors to the left and right.':0.25,
           'Which door will you take? (left/right)':0.25})
    turn = input()
    while turn.lower() not in l and turn.lower() not in r:
        speak({'Not a valid input! Try again!':0.5})
        turn = input()
    if turn.lower() in l:
        return 'left'
    else:
        return 'right'


def startgame():
    """
    signature: int -> int
    user inputs their name. program returns name. user inputs if they are ready.
    if user says yes, program says lets go on. if user doesn;t say yes. the program
    says too bad. lets go on.
    """
    player = {'name': '', 'health': 3, 'strength': 1}
    speak({'Welcome to The Labyrinth! In this game, '
           'you will move your player through a series of rooms'
           ' encoutering monsters, solving riddles, and collecting items along the way.'
           ' If you survive 6 stages, then you are freed. '
           'If not, then you lose.':4})
    name = input('What is your name?\n', )
    player['name'] = name
    speak({f"Hi, {player['name']}":2, 'Are you ready?':0.5})
    yes = input()
    yesdict = ['yes', 'yep', 'alright', 'yeah', 'yessir', 'ye', 'ok', 'okay', 'y']
    if yes.lower() in yesdict:
        speak({'Lets go on!':1})
    else:
        speak({'Too bad. Lets go on!':1})
    playgame(player)

def doriddle(player, riddle, answer):
    """
    signature: int -> int
    program gives user riddle. If user guesses riddle right, program displays a
    message for player to move on. If player messes up 3 times, user loses one
    health.
    """
    speak({'In the middle of the room, you notice a large figure. As you approach '
           'it, you realize that it is a sphinx! The sphinx gives you a riddle. you have 3 guesses.': 4})
    speak({riddle:3,
           'The sphinx stares at you anticipating an answer.':0.25})
    guess = 0
    while guess <= 2:
        i = input()
        if answer in i.lower():
            speak({'Correct!': 1,
                   f'The Answer is {answer}.': 1,
                    'You move on with your journey.': 1})
            return
        speak({'Incorrect!': 1})
        guess += 1
        if guess <= 2:
            speak({'Try again': 1})
    speak({'The sphinx waives her hands, and you feel your health dissapate!':2})
    speak({'You lose one health!':0.5})
    player['health'] -= 1
    return

def losegame(player, turn_count):
    """
    signature: none -> dict. If player loses game, defeat message is displayed and
    dict is displayed giving player stats.
    """
    speak({'As you grow weary, you realize that there is no escape. '
           'The labrinth swallows you up and you wither away. You are defeated!':3})
    speak({f'Your health was {player["health"]}':1})
    speak({f'Your strength was {player["strength"]}':1})
    speak({f'Your items {player["items"]}':1})
    speak({f'You lasted {turn_count} turns':1})
    speak({f'Good game! {player["name"]}':1})
    return

    

def playgame(player):
    """
    signature: none -> none.
    there are 4 different scenarios. riddles, monsters, items and empty room.
    In riddle, correct answer is key in dict and riddle is value. In monsters,
    mob type is key and stats are values, in items, item type is key and states are values.
    if player survives 6 stages of picking up items, fighting mobs, and solving riddles,
    end message is displayed. if not, defeat message is displayed.
    """
    riddles = {'darkness': 'The more of this there is, the less you see. What is it?',
               'egg': 'What has to be broken before you can use it?',
               'sponge': 'What is full of holes but still holds water?',
               'echo': 'What can’t talk but will reply when spoken to?',
               'hole': 'What gets bigger the more you take away?',
               'coin': 'What has a head and a tail, but no body?'}
    monsters = {'Troll': (2, 1),
                'Phantom': (2, 2),
                'Ghoul': (4, 1),
                'Spider': (2, 1),
                'Cyclops': (2, 2),
                'Minotaur': (3, 2)}
    items = {'Bow and Arrow': (0,1),
             'longsword': (0,1),
             'Beef Stew': (1,0),
             'Med Kit': (2,0),
             'Armor': (1,1),
             'Battle Axe': (0,2)}
    player['items'] = []
    turns = ['riddle', 'monster', 'item', 'empty']
    turn_count = 1
    while turn_count < 7:
        speak({f'Player Stats':0.25})
        for k, v in player.items():  
            speak({f'{k}: {v}':0.1})
        speak({'You enter a room.' :2})
        turn = turns[random.randint(0, 3)]
        if turn == 'riddle' and len(riddles) > 0:
            answer, riddle = random.choice(list(riddles.items()))
            riddles.pop(answer)
            doriddle(player, riddle, answer)
        elif turn == 'monster' and len(monsters) > 0:
            monster, stats = random.choice(list(monsters.items()))
            monsters.pop(monster)
            outcome = battle(player, monster, stats)
            if not outcome:
                losegame(player, turn_count)
                return
        elif turn == 'item' and len(items) > 0:
            item, stats = random.choice(list(items.items()))
            items.pop(item)
            player['items'].append(item)
            health, strength = stats
            speak({f'You picked up a {item}!':0.5})
            if health > 0:
                player['health'] += health
                speak({f'{item} gives you {health} health.':1})
            if strength > 0:
                player['strength'] += strength
                speak({f'{item} gives you {strength} strength.':1})
        else:
            speak({'The room is empty.':1})
        left_right()
        turn_count += 1
    win_game(player)

def win_game(player):
    """
    signature: none -> dict
    If player wins, victory message is displayed and player stats are displayed
    in dict.
    """
    speak({'You enter a room. As you walk around, you notice a small beam of light'
           'at the end of room! As you approach the light, you realize '
           'it is the exit of the labrinth! Congratulations! You win!' :5})
    speak({f'Your health was {player["health"]}.':1})
    speak({f'Your strength was {player["strength"]}.':1})
    speak({f'The items you collected were {player["items"]}.':1})
    speak({f'Good game {player["name"]}!':1})
    return

startgame()
