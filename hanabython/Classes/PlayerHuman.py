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
from Classes.PlayerBase import PlayerBase
from Classes.Action import Action
from Classes.ActionClue import ActionClue
from Classes.ActionPlay import ActionPlay
from Classes.ActionDiscard import ActionDiscard
from Classes.ActionForfeit import ActionForfeit
from IPython.display import clear_output
from time import sleep


class PlayerHuman(PlayerBase):

    def __init__(self, name):
        super().__init__(name)

    def choose_action(self):
        """
        Choose an action.

        :return: the action chosen by the player.
        :rtype: Action
        """
        print('\n' * 40)
        # The "clear_output" is here for usage in Jupyter.
        sleep(0.1) # Essential line to prevent strange behavior in Jupyter!
        clear_output()
        sleep(0.1) # Essential line to prevent strange behavior in Jupyter!
        input('%s is going to play (hit Enter).\n' % self.name)
        print(self.colored())
        while True:
            cat_str = input('\nWhat action? (C = Clue, P = Play, '
                            'D = Discard, F = Forfeit)\n')
            try:
                cat = {'C': Action.CLUE, 'P': Action.PLAY,
                       'D': Action.DISCARD, 'F': Action.FORFEIT}[
                    cat_str[0].capitalize()
                ]
                break
            except KeyError:
                pass
        if cat == Action.CLUE:
            if self.n_players == 2:
                i = 1
            else:
                while True:
                    i_str = input('What player? (1 = next player, etc.)\n')
                    try:
                        i = int(i_str)
                        break
                    except ValueError:
                        pass
            while True:
                clue_str = input('What clue? (B, G, ..., 1, 2, ...)\n')
                try:
                    clue = int(clue_str)
                    break
                except ValueError:
                    pass
                try:
                    clue = [
                        c for c in self.cfg.colors if c.symbol == clue_str][0]
                    break
                except IndexError:
                    pass
            return ActionClue(i=i, clue=clue)
        if cat in {Action.PLAY, Action.DISCARD}:
            while True:
                k_str = input('What card? (1 = leftmost, etc.)\n')
                try:
                    k = int(k_str) - 1
                    break
                except ValueError:
                    pass
            if cat == Action.PLAY:
                return ActionPlay(k=k)
            else:
                return ActionDiscard(k=k)
        return ActionForfeit()

    def receive_action_finished(self):
        """
        Receive a message: the action of the player is finished.
        """
        print(self.recent_events)
        if len(self.recent_events) > 0:
            input("Your turn is over (hit Enter).\n")
        super().receive_action_finished()

    def receive_lose(self, score):
        """
        Receive a message: the game is lost (misfires or forfeit).
        """
        super().receive_lose(score)
        print(self.recent_events)

    def receive_game_over(self, score):
        """
        Receive a message: the game is over and is neither really lost
        (misfires, forfeit) nor a total victory (maximal score).
        """
        super().receive_game_over(score)
        print(self.recent_events)

    def receive_win(self, score):
        """
        Receive a message: the game is won (total victory).
        """
        super().receive_win(score)
        print(self.recent_events)
