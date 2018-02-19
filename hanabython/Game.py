# -*- coding: utf-8 -*-
"""
Copyright François Durand
fradurand@gmail.com

This file is part of Hanabython.

    Hanabython is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Hanabython is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Hanabython.  If not, see <http://www.gnu.org/licenses/>.
"""
from copy import copy
from Configuration import Configuration
from PlayerHuman import PlayerHuman
from Board import Board
from DrawPile import DrawPile
from DiscardPile import DiscardPile
from Hand import Hand
from Action import Action


class Game:
    """
    A game of Hanabi.

    :param Configuration cfg:
    :param list players:
    """

    def __init__(self, cfg, players):
        # General initializations
        self.players = players
        self.n_players = len(self.players)
        self.cfg = cfg
        self.board = Board(cfg)
        self.draw_pile = DrawPile(cfg)
        self.discard_pile = DiscardPile(cfg)
        self.n_clues = cfg.n_clues
        self.n_misfires = 0
        self.hand_size = cfg.hand_size(self.n_players)
        self.hands = [Hand() for _ in self.players]
        self.remaining_turns = None  # For normal end-of-game rule
        self._lose = False
        self._win = False
        self.broadcast_init()
        # Deal
        self.broadcast_begin_dealing()
        for i in range(self.hand_size):
            for i_p, p in enumerate(self.players):
                self.draw(i_p)
        self.broadcast_end_dealing()

    def broadcast_init(self):
        for i, p in enumerate(self.players):
            p.receive_init(cfg=copy(self.cfg), player_names=(
                [self.players[j].name for j in range(i, self.n_players)]
                + [self.players[j].name for j in range(i)]
            ))

    def broadcast_begin_dealing(self):
        for p in self.players:
            p.receive_begin_dealing()

    def broadcast_end_dealing(self):
        for p in self.players:
            p.receive_end_dealing()

    def draw(self, i_drawer):
        card = self.draw_pile.give()
        if card is not None:
            self.hands[i_drawer].receive(card)
        if (self.cfg.end_rule == Configuration.END_NORMAL
                and self.draw_pile.n_cards == 0
                and self.remaining_turns is None):
            self.remaining_turns = self.n_players + 1
        for i, p in enumerate(self.players):
            if i == i_drawer:
                p.receive_i_draw()
            else:
                p.receive_partner_draws(self.rel(i_drawer, i), copy(card))

    def discard(self, i_discarder, k):
        card = self.hands[i_discarder].give(k)
        self.discard_pile.receive(card)
        self.n_clues += 1
        for i, p in enumerate(self.players):
            p.receive_someone_throws(self.rel(i_discarder, i), k, card)

    def play_card(self, i_player, k):
        card = self.hands[i_player].give(k)
        success = self.board.try_to_play(card)
        if success:
            if card.v == self.cfg.highest[card.c]:
                self.n_clues = min(self.n_clues + 1, self.cfg.n_clues)
            if self.board.score == self.cfg.max_score:
                self._win = True
            # TODO: terminer la partie quand il n'y a plus aucune carte posable.
        else:
            self.discard_pile.receive(card)
            self.n_misfires += 1
        for i, p in enumerate(self.players):
            p.receive_someone_plays(
                self.rel(i_player, i), k, copy(card))

    def give_clue(self, i_cluer, i_clued, clue):
        self.n_clues -= 1
        bool_list = self.hands[i_clued].match(clue)
        for i, p in enumerate(self.players):
            p.receive_someone_clues(self.rel(i_cluer, i), self.rel(i_clued, i),
                                    copy(clue), copy(bool_list))

    def rel(self, who, fro):
        return (who - fro) % self.n_players

    def lose(self):
        for i, p in enumerate(self.players):
            p.receive_lose(score=0)
        return 0

    def game_over(self):
        for i, p in enumerate(self.players):
            p.receive_game_over(score=self.board.score)
        return self.board.score

    def win(self):
        for i, p in enumerate(self.players):
            p.receive_win(score=self.board.score)
        return self.board.score

    def play(self):
        i_active_player = -1
        while True:
            i_active_player = (i_active_player + 1) % self.n_players
            active_player = self.players[i_active_player]
            # Check whether the game dies from natural causes.
            if (self.cfg.end_rule == Configuration.END_NORMAL
                    and self.remaining_turns is not None):
                self.remaining_turns -= 1
                for p in self.players:
                    p.receive_remaining_turns(self.remaining_turns)
                if self.remaining_turns == 0:
                    self._win = True
                    return self.game_over()
            elif self.cfg.end_rule == Configuration.END_CROWNING_PIECE:
                if len(self.hands[active_player]) == 0:
                    self._win = True
                    return self.game_over()
            # Require a legal action from the player
            # We do not check the 'out of bounds' problem, which will throw an
            # error anyway.
            is_action_legal = False
            while not is_action_legal:
                action = active_player.choose_action()
                if action.category == Action.DISCARD:
                    is_action_legal = self.n_clues < self.cfg.n_clues
                elif action.category == Action.CLUE:
                    is_action_legal = (
                        self.n_clues > 0 and action.i % self.n_players != 0)
                else:
                    is_action_legal = True
            active_player.receive_action_legal()
            # Perform the action and inform everybody
            if action.category == Action.DISCARD:
                self.discard(i_discarder=i_active_player, k=action.k)
                self.draw(i_drawer=i_active_player)
            elif action.category == Action.PLAY:
                self.play_card(i_player=i_active_player, k=action.k)
                if self.n_misfires == self.cfg.n_misfires:
                    self._lose = True
                else:
                    self.draw(i_drawer=i_active_player)
            elif action.category == Action.CLUE:
                self.give_clue(
                    i_cluer=i_active_player,
                    i_clued=(i_active_player + action.i) % self.n_players,
                    clue=action.clue)
            else:  # Forfeit
                self._lose = True
            active_player.receive_action_finished()
            if self._lose:
                return self.lose()
            if self._win:
                return self.win()


if __name__ == '__main__':
    fanfan = PlayerHuman(name='Fanfan')
    emilie = PlayerHuman(name='Emilie')
    pek = PlayerHuman(name='PEK')
    game = Game(Configuration.CONFIG_STANDARD, [fanfan, emilie, pek])
    game.play()
    # print(game.hands[alice])
    # print(game.hands[bob])
    # print(game.draw_pile)
    # print(game.discard_pile)
    # print()
