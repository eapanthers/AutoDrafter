from Player import Player
from PlayerList import PlayerList

import math
import pandas as pd
import numpy as np  # pip install --upgrade numpy==1.19.3 for correct installation
import random
from typing import List


def generate_picks(first_pick: int, num_rounds: int, num_teams: int) -> list:
    all_picks = []
    for r in range(num_rounds):
        if (r + 1) % 2 == 0:
            all_picks.append(num_teams * r + 1 + (num_teams - first_pick))
        else:
            all_picks.append(num_teams * r + 1 + (first_pick - 1))
    return all_picks


def get_definite_available(
    player_list: PlayerList, cur_pick: int, next_pick: int, player_compare: Player
) -> Player:
    return (
        player_list.players[next_pick - cur_pick]
        if player_list.players[next_pick - cur_pick].name != player_compare.name
        else player_list.players[next_pick - cur_pick + 1]
    )


def get_best_available(player_list: PlayerList) -> Player:
    return player_list.max


def argmax(items):
    max_indices = []
    max_item = max(items)
    for index, item in enumerate(items):
        if item == max_item:
            max_indices.append(index)
    return max_indices


def sim_picks(
    qb_list: PlayerList,
    rb_list: PlayerList,
    wr_list: PlayerList,
    te_list: PlayerList,
    data: pd.DataFrame,
    cur_pick: int,
    next_pick: int,
    already_picked: list,
    randomness: float,
) -> List[Player]:
    picked_players = [Player(1, 1, name) for name in already_picked]
    middle_players = []
    for row in data.iterrows():
        if row[1][1] not in already_picked:
            if row[1][8] <= cur_pick:  # always set to picked
                if row[1][5] == "QB":
                    cur_qb = qb_list.find_player_by_name(row[1][1])[0]
                    cur_qb.picked = True
                    picked_players.append(cur_qb)
                elif row[1][5] == "RB":
                    cur_rb = rb_list.find_player_by_name(row[1][1])[0]
                    cur_rb.picked = True
                    picked_players.append(cur_rb)
                elif row[1][5] == "WR":
                    cur_wr = wr_list.find_player_by_name(row[1][1])[0]
                    cur_wr.picked = True
                    picked_players.append(cur_wr)
                else:
                    cur_te = te_list.find_player_by_name(row[1][1])[0]
                    cur_te.picked = True
                    picked_players.append(cur_te)
            elif cur_pick < row[1][8] < next_pick + math.sqrt(next_pick):
                if row[1][5] == "QB":
                    cur_qb = qb_list.find_player_by_name(row[1][1])[0]
                    prob_picked = 1 - cur_qb.get_prob_available(
                        cur_pick, next_pick, randomness
                    )
                    rand = np.random.uniform(0, 1)
                    if rand < prob_picked:
                        cur_qb.picked = True
                        picked_players.append(cur_qb)
                    else:
                        middle_players.append(cur_qb)
                elif row[1][5] == "RB":
                    cur_rb = rb_list.find_player_by_name(row[1][1])[0]
                    prob_picked = 1 - cur_rb.get_prob_available(
                        cur_pick, next_pick, randomness
                    )
                    rand = np.random.uniform(0, 1)
                    if rand < prob_picked:
                        cur_rb.picked = True
                        picked_players.append(cur_rb)
                    else:
                        middle_players.append(cur_rb)
                elif row[1][5] == "WR":
                    cur_wr = wr_list.find_player_by_name(row[1][1])[0]
                    prob_picked = 1 - cur_wr.get_prob_available(
                        cur_pick, next_pick, randomness
                    )
                    rand = np.random.uniform(0, 1)
                    if rand < prob_picked:
                        cur_wr.picked = True
                        picked_players.append(cur_wr)
                    else:
                        middle_players.append(cur_wr)
                else:
                    cur_te = te_list.find_player_by_name(row[1][1])[0]
                    prob_picked = 1 - cur_te.get_prob_available(
                        cur_pick, next_pick, randomness
                    )
                    rand = np.random.uniform(0, 1)
                    if rand < prob_picked:
                        cur_te.picked = True
                        picked_players.append(cur_te)
                    else:
                        middle_players.append(cur_te)
    if len(picked_players) == next_pick:
        qb_list.remove_picked()
        rb_list.remove_picked()
        wr_list.remove_picked()
        te_list.remove_picked()
        return picked_players
    elif len(picked_players) < next_pick:
        sampled_players = random.sample(middle_players, next_pick - len(picked_players))
        for player in sampled_players:
            player.picked = True
        qb_list.remove_picked()
        rb_list.remove_picked()
        wr_list.remove_picked()
        te_list.remove_picked()
        return picked_players + sampled_players
    else:
        for player in picked_players[next_pick:]:
            player.picked = False
        qb_list.remove_picked()
        rb_list.remove_picked()
        wr_list.remove_picked()
        te_list.remove_picked()
        return picked_players[:next_pick]


def ff_viterbi(
    num_qbs: int,
    num_rbs: int,
    num_wrs: int,
    num_tes: int,
    picks: list,
    league_type: str = "standard",
    randomness: int = 10,
) -> List[Player]:

    cur_qbs_drafted = 0
    cur_rbs_drafted = 0
    cur_wrs_drafted = 0
    cur_tes_drafted = 0

    num_qbs_to_draft = num_qbs - cur_qbs_drafted
    num_rbs_to_draft = num_rbs - cur_rbs_drafted
    num_wrs_to_draft = num_wrs - cur_wrs_drafted
    num_tes_to_draft = num_tes - cur_tes_drafted

    states = ["qb", "rb", "wr", "te"]
    transition_table = {
        "qb": [
            max(1 - cur_qbs_drafted / num_qbs, 0),
            max(1 - cur_qbs_drafted / num_qbs, 0),
            max(1 - cur_qbs_drafted / num_qbs, 0),
            max(1 - cur_qbs_drafted / num_qbs, 0),
        ],
        "rb": [
            max(1 - cur_rbs_drafted / num_rbs, 0),
            max(1 - cur_rbs_drafted / num_rbs, 0),
            max(1 - cur_rbs_drafted / num_rbs, 0),
            max(1 - cur_rbs_drafted / num_rbs, 0),
        ],
        "wr": [
            max(1 - cur_wrs_drafted / num_wrs, 0),
            max(1 - cur_wrs_drafted / num_wrs, 0),
            max(1 - cur_wrs_drafted / num_wrs, 0),
            max(1 - cur_wrs_drafted / num_wrs, 0),
        ],
        "te": [
            max(1 - cur_tes_drafted / num_tes, 0),
            max(1 - cur_tes_drafted / num_tes, 0),
            max(1 - cur_tes_drafted / num_tes, 0),
            max(1 - cur_tes_drafted / num_tes, 0),
        ],
    }

    qb_df = pd.read_csv(f"fantasyCSVs/standard_qb.csv", delimiter=",")
    if league_type.lower() == "standard":
        rb_df = pd.read_csv(f"fantasyCSVs/standard_rb.csv", delimiter=";")
        wr_df = pd.read_csv(f"fantasyCSVs/standard_wr.csv", delimiter=";")
        te_df = pd.read_csv(f"fantasyCSVs/standard_te.csv", delimiter=",")
    else:
        rb_df = pd.read_csv(f"fantasyCSVs/ppr_rb.csv", delimiter=";")
        wr_df = pd.read_csv(f"fantasyCSVs/ppr_wr.csv", delimiter=";")
        te_df = pd.read_csv(f"fantasyCSVs/ppr_te.csv", delimiter=",")

    all_df = rb_df
    all_df = all_df.append(qb_df).append(wr_df).append(te_df)
    sorted_df = all_df.sort_values(by="ADP")

    all_rbs = PlayerList()
    for i, row in rb_df.iterrows():
        new_player = Player(row[8], row[7], row[1])
        all_rbs.add(new_player)

    all_qbs = PlayerList()
    for i, row in qb_df.iterrows():
        new_player = Player(row[8], row[7], row[1])
        all_qbs.add(new_player)

    all_wrs = PlayerList()
    for i, row in wr_df.iterrows():
        new_player = Player(row[8], row[7], row[1])
        all_wrs.add(new_player)

    all_tes = PlayerList()
    for i, row in te_df.iterrows():
        new_player = Player(row[8], row[7], row[1])
        all_tes.add(new_player)

    sequences = {"draft1": picks}
    for seq_id in sequences.keys():
        all_picked = []
        sequence = sequences[seq_id]

        v_table = [[[0] for i in range(len(sequence))] for i in range(len(states))]
        prev_table = [
            [[None] for i in range(len(sequence) - 1)] for i in range(len(states))
        ]
        drafted_table = [
            [[None] for i in range(len(sequence))] for i in range(len(states))
        ]
        drafted_players = [
            [[None] for i in range(len(sequence))] for i in range(len(states))
        ]

        picked_players = sim_picks(
            all_qbs,
            all_rbs,
            all_wrs,
            all_tes,
            sorted_df,
            1,
            sequence[0] - 1,
            all_picked,
            randomness,
        )
        all_picked = [p.name for p in picked_players]
        print(f"The players drafted before your first pick are {all_picked}.")

        for i in range(len(states)):
            if states[i] == "qb":
                v_table[i][0] = math.log(
                    max(
                        get_best_available(all_qbs).proj_points
                        - all_qbs.find_adp(sequence[1])[0].proj_points,
                        0.01,
                    )
                )
                drafted_table[i][0] = [0]
                best_player = get_best_available(all_qbs)
                drafted_players[i][0] = best_player
            elif states[i] == "rb":
                v_table[i][0] = math.log(
                    max(
                        get_best_available(all_rbs).proj_points
                        - all_rbs.find_adp(sequence[1])[0].proj_points,
                        0.01,
                    )
                )
                drafted_table[i][0] = [1]
                best_player = get_best_available(all_rbs)
                drafted_players[i][0] = best_player
            elif states[i] == "wr":
                v_table[i][0] = math.log(
                    max(
                        get_best_available(all_wrs).proj_points
                        - all_wrs.find_adp(sequence[1])[0].proj_points,
                        0.01,
                    )
                )
                drafted_table[i][0] = [2]
                best_player = get_best_available(all_wrs)
                drafted_players[i][0] = best_player
            elif states[i] == "te":
                v_table[i][0] = math.log(
                    max(
                        get_best_available(all_tes).proj_points
                        - all_tes.find_adp(sequence[1])[0].proj_points,
                        0.01,
                    )
                )
                drafted_table[i][0] = [3]
                best_player = get_best_available(all_tes)
                drafted_players[i][0] = best_player

        print(f"Your picks are: {sequence}.")
        for i in range(1, len(sequence)):
            picked_players = sim_picks(
                all_qbs,
                all_rbs,
                all_wrs,
                all_tes,
                sorted_df,
                sequence[i - 1] + 1,
                sequence[i] - 1,
                all_picked,
                randomness,
            )

            all_picked = [p.name for p in picked_players]
            for pos in range(len(states)):
                cur_qbs_drafted = 0
                cur_rbs_drafted = 0
                cur_wrs_drafted = 0
                cur_tes_drafted = 0
                probabilities = []
                if states[pos] == "qb":
                    e = all_qbs
                elif states[pos] == "rb":
                    e = all_rbs
                elif states[pos] == "wr":
                    e = all_wrs
                elif states[pos] == "te":
                    e = all_tes
                for drafted in drafted_table[pos][i - 1]:
                    if drafted == 0:
                        cur_qbs_drafted += 1
                    elif drafted == 1:
                        cur_rbs_drafted += 1
                    elif drafted == 2:
                        cur_wrs_drafted += 1
                    else:
                        cur_tes_drafted += 1
                transition_table["qb"] = [
                    max(1 - cur_qbs_drafted / num_qbs, 0),
                    max(1 - cur_qbs_drafted / num_qbs, 0),
                    max(1 - cur_qbs_drafted / num_qbs, 0),
                    max(1 - cur_qbs_drafted / num_qbs, 0),
                ]
                transition_table["rb"] = [
                    max(1 - cur_rbs_drafted / num_rbs, 0),
                    max(1 - cur_rbs_drafted / num_rbs, 0),
                    max(1 - cur_rbs_drafted / num_rbs, 0),
                    max(1 - cur_rbs_drafted / num_rbs, 0),
                ]
                transition_table["wr"] = [
                    max(1 - cur_wrs_drafted / num_wrs, 0),
                    max(1 - cur_wrs_drafted / num_wrs, 0),
                    max(1 - cur_wrs_drafted / num_wrs, 0),
                    max(1 - cur_wrs_drafted / num_wrs, 0),
                ]
                transition_table["te"] = [
                    max(1 - cur_tes_drafted / num_tes, 0),
                    max(1 - cur_tes_drafted / num_tes, 0),
                    max(1 - cur_tes_drafted / num_tes, 0),
                    max(1 - cur_tes_drafted / num_tes, 0),
                ]
                for state in range(len(states)):
                    try:
                        if i <= len(sequences):
                            probabilities.append(
                                v_table[state][i - 1]
                                + math.log(
                                    get_best_available(e).proj_points
                                    - e.find_adp(sequence[i + 1])[0].proj_points
                                )
                                + math.log(transition_table[states[state]][pos])
                            )
                        else:
                            probabilities.append(
                                v_table[state][i - 1]
                                + math.log(get_best_available(e).proj_points)
                                + math.log(transition_table[states[state]][pos])
                            )
                    except ValueError as err:
                        probabilities.append(
                            -math.inf
                        )  # probabilities contains the probability of going from pos into state, so index is which state entered

                v_table[pos][i] = max(probabilities)
                max_idx = argmax(probabilities)  # where it should be coming from
                prev_table[pos][i - 1] = max_idx
                drafted_table[pos][i] = drafted_table[pos][i - 1]
                drafted_table[pos][i].append(max_idx[0])
                if pos == 0:
                    best_player = get_best_available(all_qbs)
                    for player in drafted_players[pos][i]:
                        if player:
                            if player.name == best_player.name:
                                all_qbs.remove(best_player)
                    best_player = get_best_available(all_qbs)
                    drafted_players[pos][i] = best_player
                elif pos == 1:
                    best_player = get_best_available(all_rbs)
                    for player in drafted_players[pos][i]:
                        if player:
                            if player.name == best_player.name:
                                all_rbs.remove(best_player)
                    best_player = get_best_available(all_rbs)
                    drafted_players[pos][i] = best_player
                elif pos == 2:
                    best_player = get_best_available(all_wrs)
                    for player in drafted_players[pos][i]:
                        if player:
                            if player.name == best_player.name:
                                all_wrs.remove(best_player)
                    best_player = get_best_available(all_wrs)
                    drafted_players[pos][i] = best_player
                else:
                    best_player = get_best_available(all_tes)
                    for player in drafted_players[pos][i]:
                        if player:
                            if player.name == best_player.name:
                                all_tes.remove(best_player)
                    best_player = get_best_available(all_tes)
                    drafted_players[pos][i] = best_player

        players = []
        max_values = []
        for state in range(len(v_table)):
            max_values.append(
                v_table[state][len(sequence) - 1]
            )
        last_state = argmax(max_values)[0]
        players.append(drafted_players[last_state][len(sequence) - 1])
        index = len(sequence) - 2
        while index >= 0:
            beta = prev_table[last_state][index][0]
            players.append(drafted_players[beta][index])
            last_state = beta
            index -= 1

        players = players[::-1]
    return players


if __name__ == "__main__":
    print("What is your draft slot?")
    pick_index = int(input())
    print("How many rounds are in this draft? (The last two rounds will be removed to draft a kicker and D/ST)")
    num_rounds = int(input())
    num_rounds -= 2
    print("How many teams are in this draft?")
    num_teams = int(input())
    print(
        "What weight would you like assigned to drafting a QB? (1 - lowest, recommended)"
    )
    num_qbs = int(input())
    print(
        f"What weight would you like assigned to drafting a RB? ({math.ceil((num_rounds - 2 - num_qbs) / 2)} - recommended)"
    )
    num_rbs = int(input())
    print(
        f"What weight would you like assigned to drafting a WR? ({math.floor((num_rounds - 2 - num_qbs) // 2)} - recommended)"
    )
    num_wrs = int(input())
    print(
        f"What weight would you like assigned to drafting a TE? ({num_rounds - num_qbs - num_wrs - num_rbs} - recommended)"
    )
    num_tes = int(input())
    print("What type of scoring does this league use? (Either ppr or standard)")
    league_type = input()
    print(
        "How much randomness should there be when simulating picks? (1 - most random, 10 - least random)"
    )
    randomness = int(input())
    num_qbs = num_qbs - 1 if num_qbs > 1 else 1
    picks = generate_picks(pick_index, num_rounds, num_teams)
    players = ff_viterbi(
        num_qbs, num_rbs, num_wrs, num_tes, picks, league_type, randomness
    )
    print(
        f"Your optimal estimated selections are: {[player.name for player in players]}."
    )
