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
from typing import List, Union
from hanabython.Classes.Color import Color
from hanabython.Classes.Colored import Colored
from hanabython.Classes.Configuration import Configuration
from hanabython.Classes.ConfigurationEndRule import ConfigurationEndRule
from hanabython.Classes.PlayerHuman import PlayerHuman
from hanabython.Classes.Board import Board
from hanabython.Classes.DrawPile import DrawPile
from hanabython.Classes.DiscardPile import DiscardPile
from hanabython.Classes.Hand import Hand
from hanabython.Classes.Action import Action
from hanabython.Classes.Player import Player


class Game(Colored):
    """
    A game of Hanabi.

    :param Configuration cfg:
    :param list players:
    """

    def debug(self, o: object) -> None:
        if self.debug_mode:
            print('GAME: ' + str(o))

    def __init__(self, cfg: Configuration, players: List[Player],
                 debug_mode: bool = False):
        # General initializations
        self.debug('General initializations')
        self.players = players
        self.debug_mode = debug_mode
        self.n_players = len(self.players)
        self.cfg = cfg
        self.board = Board(cfg)
        self.draw_pile = DrawPile(cfg)
        self.discard_pile = DiscardPile(cfg)
        self.n_clues = cfg.n_clues
        self.n_misfires = 0
        self.hand_size = cfg.hand_size_rule.f(self.n_players)
        self.hands = [Hand() for _ in self.players]
        self.remaining_turns = None  # For normal end-of-game rule
        self._lose = False
        self._win = False
        self.broadcast_init()
        # Deal
        self.debug('Dealing cards')
        self.broadcast_begin_dealing()
        for i in range(self.hand_size):
            for i_p, p in enumerate(self.players):
                self.draw(i_p)
        self.broadcast_end_dealing()
        self.debug('Cards are dealt')

    def colored(self) -> str:
        return 'This is a game of Hanabi.'

    def broadcast_init(self) -> None:
        for i, p in enumerate(self.players):
            p.receive_init(cfg=copy(self.cfg), player_names=(
                [self.players[j].name for j in range(i, self.n_players)]
                + [self.players[j].name for j in range(i)]
            ))

    def broadcast_begin_dealing(self) -> None:
        for p in self.players:
            p.receive_begin_dealing()

    def broadcast_end_dealing(self) -> None:
        for p in self.players:
            p.receive_end_dealing()

    def draw(self, i_drawer: int) -> None:
        card = self.draw_pile.give()
        if card is not None:
            self.hands[i_drawer].receive(card)
        if (self.cfg.end_rule == ConfigurationEndRule.NORMAL
                and self.draw_pile.n_cards == 0
                and self.remaining_turns is None):
            self.remaining_turns = self.n_players + 1
        for i, p in enumerate(self.players):
            if i == i_drawer:
                p.receive_i_draw()
            else:
                p.receive_partner_draws(self.rel(i_drawer, i), copy(card))

    def discard(self, i_discarder: int, k: int) -> None:
        card = self.hands[i_discarder].give(k)
        self.discard_pile.receive(card)
        self.n_clues += 1
        for i, p in enumerate(self.players):
            p.receive_someone_throws(self.rel(i_discarder, i), k, card)

    def play_card(self, i_player: int, k: int) -> None:
        card = self.hands[i_player].give(k)
        success = self.board.try_to_play(card)
        if success:
            if card.v == self.cfg.highest[self.cfg.i_from_c(card.c)]:
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

    def give_clue(self, i_cluer: int, i_clued: int,
                  clue: Union[int, Color]) -> None:
        self.n_clues -= 1
        bool_list = self.hands[i_clued].match(clue)
        for i, p in enumerate(self.players):
            p.receive_someone_clues(self.rel(i_cluer, i), self.rel(i_clued, i),
                                    copy(clue), copy(bool_list))

    def rel(self, who: int, fro: int) -> int:
        return (who - fro) % self.n_players

    def lose(self) -> int:
        for i, p in enumerate(self.players):
            p.receive_lose(score=0)
        return 0

    def game_over(self) -> int:
        for i, p in enumerate(self.players):
            p.receive_game_over(score=self.board.score)
        return self.board.score

    def win(self) -> int:
        for i, p in enumerate(self.players):
            p.receive_win(score=self.board.score)
        return self.board.score

    def play(self) -> int:
        self.debug("The game begins.")
        i_active_player = -1
        while True:
            self.debug("Enter the big 'while' loop.")
            i_active_player = (i_active_player + 1) % self.n_players
            active_player = self.players[i_active_player]
            self.debug("%s's turn begins" % active_player.name)
            # Check whether the game dies from natural causes.
            self.debug("Check end-of-game condition.")
            if (self.cfg.end_rule == ConfigurationEndRule.NORMAL
                    and self.remaining_turns is not None):
                self.remaining_turns -= 1
                for p in self.players:
                    p.receive_remaining_turns(self.remaining_turns)
                if self.remaining_turns == 0:
                    self._win = True
                    return self.game_over()
            elif self.cfg.end_rule == ConfigurationEndRule.CROWNING_PIECE:
                if len(self.hands[active_player]) == 0:
                    self._win = True
                    return self.game_over()
            self.debug("The game is not over, let us proceed.")
            # Require a legal action from the player
            # We do not check the 'out of bounds' problem, which will throw an
            # error anyway.
            self.debug("Ask %s for an action." % active_player.name)
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
            self.debug("%s proposed a legal action." % active_player.name)
            # Perform the action and inform everybody
            if action.category == Action.DISCARD:
                self.debug("It is a 'discard' action.")
                self.discard(i_discarder=i_active_player, k=action.k)
                self.draw(i_drawer=i_active_player)
            elif action.category == Action.PLAY:
                self.debug("It is a 'play' action.")
                self.play_card(i_player=i_active_player, k=action.k)
                if self.n_misfires == self.cfg.n_misfires:
                    self._lose = True
                else:
                    self.draw(i_drawer=i_active_player)
            elif action.category == Action.CLUE:
                self.debug("It is a 'clue' action.")
                self.give_clue(
                    i_cluer=i_active_player,
                    i_clued=(i_active_player + action.i) % self.n_players,
                    clue=action.clue)
            else:  # Forfeit
                self.debug("It is a 'forfeit' action.")
                self._lose = True
            self.debug("Inform %s that the turn is over." % active_player.name)
            active_player.receive_action_finished()
            self.debug("%s's turn is over." % active_player.name)
            if self._lose:
                return self.lose()
            if self._win:
                return self.win()


if __name__ == '__main__':
    fanfan = PlayerHuman(name='Fanfan')
    emilie = PlayerHuman(name='Emilie')
    pek = PlayerHuman(name='PEK')
    game = Game(Configuration.STANDARD, [fanfan, emilie, pek])
    game.play()
    # print(game.hands[alice])
    # print(game.hands[bob])
    # print(game.draw_pile)
    # print(game.discard_pile)
    # print()
