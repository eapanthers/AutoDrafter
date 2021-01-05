from Player import Player
import sys
from typing import Optional, Tuple, List


def part(players: List[Player], low: int, high: int) -> int:
    i = low - 1
    pivot = players[high]

    for j in range(low, high):
        if players[j].proj_points > pivot.proj_points:
            i = i + 1
            players[i], players[j] = players[j], players[i]

    players[i + 1], players[high] = players[high], players[i + 1]
    return i + 1


def player_sort(players: List[Player], low: int, high: int) -> List[Player]:
    if len(players) == 1:
        return players
    if low < high:
        mid = part(players, low, high)

        player_sort(players, low, mid - 1)
        player_sort(players, mid + 1, high)


class PlayerList:
    def __init__(self):
        self.size = 0
        self.max = Player(sys.maxsize, 0, "Null")
        self.players = []

    def sort(self):
        player_sort(self.players, 0, self.size - 1)

    def get(self, index: int) -> Player:
        return self.players[index]

    def find_adp(self, adp: float) -> Optional[Tuple[Player, int]]:
        for idx, player in enumerate(self.players):
            if player.adp >= adp:
                return player, idx
        return None

    def remove(self, player: Player) -> None:
        remove_idx = None
        remove_player = None
        for idx, cur_player in enumerate(self.players):
            if player.name == cur_player.name:
                remove_idx = idx
                remove_player = cur_player
        self.players = (
            self.players[0:remove_idx] + self.players[remove_idx + 1 : self.size]
        )
        self.size -= 1
        if remove_player == self.max:
            self.max = self.players[0]

    def add(self, player: Player) -> None:
        if player.proj_points > self.max.proj_points:
            self.max = player
        self.players.append(player)
        self.size += 1

    def remove_picked(self) -> None:
        for player in self.players:
            if player.picked:
                self.remove(player)

    def find_player_by_name(self, name: str) -> Optional[Tuple[Player, int]]:
        for idx, cur_player in enumerate(self.players):
            if name == cur_player.name:
                return cur_player, idx
        return None
