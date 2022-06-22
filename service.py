import random
import string

from fastapi import Body

import database as db


# matches_list_db = db.get_database("matches")
# players_list_db = db.get_database("players")


# USER MANAGEMENT #

def create_new_user(data):
    users_list_db = db.get_database("users")
    data_id = asign_id(users_list_db, "U-")
    return db.create_data("users", data_id,
                          {'name': str([*data.values()][0]),
                           'email': str([*data.values()][1]),
                           'id': data_id})


def get_user(email: dict):
    user_found = False
    users_list_db = db.get_database("users")
    for user in users_list_db:
        user_dict: dict = user.val()
        for i in range(len([*user_dict.values()])):
            if [*user_dict.keys()][i] == "email":
                if [*user_dict.values()][i] == [*email.values()][0]:
                    user_found = True
        if user_found:
            return user_dict
    return


# LEAGUES MANAGEMENT #

def create_new_league(data: dict):
    leagues_list_db = db.get_database("leagues")
    data_id = asign_id(leagues_list_db, "L-")
    create_league = db.create_data("leagues", data_id, {'name': str([*data.values()][0]), 'id': data_id})
    if create_league:
        add_league_to_user(data_id, "owner", str([*data.values()][1]))
    return create_league


def espectate_new_league(data: dict):
    leagues_list_db = db.get_database("leagues")
    result = ""
    for league in leagues_list_db:
        if league.key() == [*data.values()][0]:
            add_league_to_user(league.key(), "spectator", str([*data.values()][1]))
            result = league.key()

    return result


def add_league_to_user(data_id, where: string, ownerId: string):
    result = ""
    if where == "owner":
        result = db.get_db_instance().child("users").child(ownerId).child("ownLeaguesId").push(data_id)

    if where == "spectator":
        result = db.get_db_instance().child("users").child(ownerId).child("spectatorLeaguesId").push(data_id)

    return result


def get_league(data: dict):
    leagues_list_db = db.get_database("leagues")
    for league in leagues_list_db:
        if league.key() == [*data.values()][0]:
            return league.val()


def get_leagues(data: dict):
    ownLeaguesId: dict = {}
    spectatorLeaguesId: dict = {}

    for i in range(len([*data.keys()])):
        if [*data.keys()][i] == "ownLeaguesId":
            ownLeaguesId = [*data.values()][i]
        if [*data.keys()][i] == "espectatorLeaguesId":
            spectatorLeaguesId = [*data.values()][i]

    ownLeagues: list = []
    spectatorLeagues: list = []

    if len([*ownLeaguesId.values()]) > 0:
        find_league(ownLeaguesId, ownLeagues)
    if len([*spectatorLeaguesId.values()]) > 0:
        find_league(spectatorLeaguesId, spectatorLeagues)

    return {'ownLeagues': ownLeagues, 'spectatingLeagues': spectatorLeagues}


def find_league(listOfIds: dict, whereToAdd: list):
    leagues_list_db = db.get_database("leagues")
    for i in range(len([*listOfIds.values()])):
        for league in leagues_list_db:
            if league.key() == [*listOfIds.values()][i]:
                whereToAdd.append(league.val())
    return whereToAdd


# PLAYERS REQUESTS #

def create_new_player(data: dict):
    player_id = asign_id(db.get_database("players"), "P-")
    medium: float = (int([*data.values()][1]) + int([*data.values()][2]) + int([*data.values()][3])) / 3
    create_player = db.create_data("players", player_id,
                                   {'id': player_id, 'name': str([*data.values()][0]),
                                    'matches': [""], 'goals': [0], 'medium': [medium],
                                    'shooter': [int([*data.values()][1])],
                                    'center': [int([*data.values()][2])], 'defense': [int([*data.values()][3])]
                                    })
    if create_player:
        add_player_to_league(player_id, [*data.values()][4])
    return create_player


def get_player(data: dict):
    players_list_db = db.get_database("players")
    for player in players_list_db:
        print([*data.values()][0])
        if player.key() == [*data.values()][0]:
            return player.val()
    return ""


def get_players(data: dict):
    players_id: dict = [*data.values()][0]

    print(players_id)

    players: list = []

    if len([*players_id.values()]) > 0:
        find_player_dict(players_id, players)

    return players


def find_player_dict(listOfIds: dict, whereToAdd: list):
    players_list_db = db.get_database("players")
    for i in range(len([*listOfIds.values()])):
        for player in players_list_db:
            if player.key() == [*listOfIds.values()][i]:
                whereToAdd.append(player.val())
    return whereToAdd


def find_player_list(listOfIds: list, whereToAdd: list):
    players_list_db = db.get_database("players")
    for i in range(len(listOfIds)):
        for player in players_list_db:
            if player.key() == listOfIds[i]:
                whereToAdd.append(player.val())
    return whereToAdd


def add_player_to_league(player_id, leagueId):
    db.get_db_instance().child("leagues").child(leagueId).child("playersId").push(player_id)

def add_stats_to_player(player_id, shooting, center, defense, goal, medium, match_id):
    db.get_db_instance().child("players").child(player_id).child("shooter").push(shooting)
    db.get_db_instance().child("players").child(player_id).child("defense").push(center)
    db.get_db_instance().child("players").child(player_id).child("center").push(defense)
    db.get_db_instance().child("players").child(player_id).child("goals").push(goal)
    db.get_db_instance().child("players").child(player_id).child("medium").push(medium)
    db.get_db_instance().child("players").child(player_id).child("matches").push(match_id)
# MATCHES REQUESTS #


def create_new_match(data: dict):
    players_list: list = []
    test: dict = [*data.values()][0]
    print([*test.values()][0])
    players_list = find_player_list([*test.values()][0], players_list)
    players_mediums: list = []

    for player in players_list:
        player_dict: dict = player
        for i in range(len([*player_dict.values()])):
            if [*player_dict.keys()][i] == "medium":
                player_medium_counter = 0
                for medium in [*player_dict.values()][i]:
                    player_medium_counter = + medium
                player_medium_counter = player_medium_counter / len([*player_dict.values()][i])
                players_mediums.append(player_medium_counter)

    medium_for_team = 0

    for medium in players_mediums:
        medium_for_team += medium
    medium_for_team = medium_for_team / 2
    print(medium_for_team)

    less_difference: int = 10
    first_team: list = []
    second_team: list = []

    for i in range(30):
        team: list = []
        positions: list = []
        while len(team) <= len(players_mediums) / 2 - 1:
            is_good = True
            random_number = random.randint(0, len(players_mediums) - 1)
            if len(positions) > 0:
                for already_used in positions:
                    if already_used == random_number:
                        is_good = False
            if is_good:
                team.append(players_mediums[random_number])
                positions.append(random_number)
        total_medium = 0
        for participant in team:
            total_medium = total_medium + participant
        difference = total_medium - medium_for_team
        if difference < 0:
            difference = difference * (-1)
        if difference < less_difference:
            first_team = team
            less_difference = difference
            print(positions)
            team2: list = []
            for i in range(len(players_mediums)):
                if buscar_en_lista(positions, i):
                    print("Numero " + str(i) + " esta dentro")
                else:
                    print("Numero " + str(i) + " no esta dentro")
                    team2.append(players_mediums[i])
            second_team = team2
    print(less_difference)
    print(players_mediums)
    print(first_team)
    print(second_team)

    full_players_fist_team: list = []
    full_players_second_team: list = []

    for player in players_list:
        player_dict: dict = player
        for i in range(len([*player_dict.values()])):
            if [*player_dict.keys()][i] == "medium":
                if buscar_en_lista(first_team, [*player_dict.values()][i][0]):
                    for i in range(len([*player_dict.values()])):
                        if [*player_dict.keys()][i] == "id":
                            full_players_fist_team.append([*player_dict.values()][i])
                else:
                    for i in range(len([*player_dict.values()])):
                        if [*player_dict.keys()][i] == "id":
                            full_players_second_team.append([*player_dict.values()][i])

    print(full_players_fist_team)
    print(full_players_second_team)
    match_id = asign_id(db.get_database("matches"), "M-")
    league_id: dict = [*data.values()][0]
    result = add_new_match(match_id, full_players_fist_team, full_players_second_team)
    add_match_to_league(match_id, [*league_id.values()][1])
    return result


def add_match_to_league(match_id, leagueId):
    db.get_db_instance().child("leagues").child(leagueId).child("matchesId").push(match_id)


def add_new_match(match_id, team1, team2):
    return db.create_data("matches", match_id, {'id': match_id, 'team1': team1, 'team2': team2})


def get_matches(data: dict):
    matches_id: dict = [*data.values()][0]

    matches: list = []

    if len([*matches_id.values()]) > 0:
        find_match_dict(matches_id, matches)
    return matches


def find_match_dict(listOfIds: dict, whereToAdd: list):
    matches_list_db = db.get_database("matches")
    for i in range(len([*listOfIds.values()])):
        for match in matches_list_db:
            if match.key() == [*listOfIds.values()][i]:
                whereToAdd.append(match.val())
    return whereToAdd


def end_match(data: dict):
    id_match = [*data.values()][0]
    print(id_match)
    max_shooting = 0
    mvp_shooting = ""
    max_center = 0
    mvp_center = ""
    max_defense = 0
    mvp_defense = ""
    mvp = 0
    player_mvp = ""
    team1_goals = 0
    team2_goals = 0
    list = [*data.values()][1]
    for i in range(len(list)):
        player_dict: dict = list[i]
        print(player_dict)
        shooting = int([*player_dict.values()][2])
        if shooting > max_shooting:
            max_shooting = shooting
            mvp_shooting = [*player_dict.values()][1] + " - " + str(shooting)
        center = int([*player_dict.values()][4])
        if center > max_center:
            max_center = center
            mvp_center = [*player_dict.values()][1] + " - " + str(center)
        defense = int([*player_dict.values()][3])
        if defense > max_defense:
            max_defense = defense
            mvp_defense = [*player_dict.values()][1] + " - " + str(defense)
        goals = int([*player_dict.values()][5])
        if  i >= len(list)/2:
            team2_goals = team2_goals + goals
        else:
            team1_goals = team1_goals + goals
        medium = (shooting + center + defense)/3
        if medium > mvp:
            mvp = medium
            player_mvp = [*player_dict.values()][1] + " - " + str(mvp)
        print(medium)
        add_stats_to_player([*player_dict.values()][0], shooting, center, defense, goals, medium, id_match)
    result = str(team1_goals) + " - " + str(team2_goals)

    update = update_match(id_match, result, player_mvp, mvp_shooting, mvp_center, mvp_defense)
    return update


def update_match(match_id, result, player_mvp, shooter, center, defense):
    return db.get_db_instance().child("matches").child(match_id).update(
        {'id': match_id, 'result': result, 'mvp': player_mvp, 'shooter': shooter, 'center': center, 'defense': defense})


# ID MANAGEMENT #


def asign_id(list: list, prefix: string):
    code_works = False
    final_code = ""
    while not code_works:
        same_code = False
        code = generate_id(prefix)
        for item in list:
            print(item.key())
            if item.key() == code:
                same_code = True
        if not same_code:
            code_works = True
            final_code = code
    print("final-code" + final_code)
    return final_code


def generate_id(prefix: string):
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
    return prefix + x


def buscar_en_lista(list, item):
    for i in range(len(list)):
        if list[i] == item:
            return True
    return False
