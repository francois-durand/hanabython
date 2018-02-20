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
from Classes.Colored import Colored
from Classes.ActionForfeit import ActionForfeit


class Player(Colored):
    """
    A player for Hanabi.

    :param str name: the name of the player.

    To define a subclass, the only real requirement is to implement the function
    :meth:`choose_action`.

    >>> antoine = Player('Antoine')
    >>> print(antoine)
    Antoine
    """

    def __init__(self, name):
        self.name = name

    def colored(self):
        return self.name

    def receive_init(self, cfg, player_names):
        """
        Receive a message: the game starts.

        :param Configuration cfg: the configuration of the game.
        :param player_names: the names of the players, rotated so that this
            player corresponds to index 0.
        """
        pass

    def receive_begin_dealing(self):
        """
        Receive a message: the initial dealing of hands begins.
        """
        pass

    def receive_end_dealing(self):
        """
        Receive a message: the initial dealing of hands is over.

        The hands themselves are not communicated in this message. Drawing
        cards, including for the initial hands, is always handled by
        :meth:`receive_i_draw` and :meth:`receive_partner_draws`.
        """
        pass

    def receive_remaining_turns(self, remaining_turns):
        """
        Receive a message: the number of remaining turns is now known.

        This happens with the normal rule for end of game: as soon as the
        discard pile is empty, we know how many turns are left. "Turn" means
        that one player gets to play (not all of them).

        :param int remaining_turns: the number of turns left.
        """
        pass

    def receive_i_draw(self):
        """
        Receive a message: this player tries to draw a card.

        A card is actually drawn only if the draw pile is not empty.
        """
        pass

    def receive_partner_draws(self, i_drawer, card):
        """
        Receive a message: another player tries to draw a card.

        A card is actually drawn only if the draw pile is not empty.

        :param int i_drawer: the position of the player who draws (relatively
            to this player).
        :param Card card: the card drawn.
        """
        pass

    def receive_someone_throws(self, i_thrower, k, card):
        """
        Receive a message: a player willingly discards a card.

        It is not necessary to check whether this action is legal: the Game
        will only send this message when it is the case.

        :param int i_thrower: the position of the player who throws (relatively
            to this player).
        :param int k: position of the card in the hand.
        :param Card card: the card thrown.
        """
        pass

    def receive_someone_plays(self, i_player, k, card):
        """
        Receive a message: a player tries to play a card on the board.

        This can be a success or a misfire.

        :param int i_player: the position of the player who plays the card
            (relatively to this player).
        :param int k: position of the card in the hand.
        :param Card card: the card played.
        """
        pass

    def receive_someone_clues(self, i_cluer, i_clued, clue, bool_list):
        """
        Receive a message: a player gives a clue to another.

        It is not necessary to check whether this action is legal: the Game
        will only send this message when it is the case.

        :param int i_cluer: the position of the player who gives the clue
            (relatively to this player).
        :param int i_clued: the position of the player who receives the clue
            (relatively to this player).
        :param int|Color clue: the clue (value or color).
        :param list bool_list: a list of boolean that indicates what cards
            match the clue given.
        """
        pass

    def receive_someone_forfeits(self, i_forfeiter):
        """
        Receive a message: a player forfeits.

        :param int i_forfeiter: the position of the player who forfeits
            (relatively to this player).
        """
        pass

    # noinspection PyMethodMayBeStatic
    def choose_action(self):
        """
        Choose an action.

        :return: the action chosen by the player.
        :rtype: Action
        """
        return ActionForfeit()

    def receive_action_legal(self):
        """
        Receive a message: the action chosen is legal.
        """
        pass

    def receive_action_finished(self):
        """
        Receive a message: the action of the player is finished.
        """
        pass

    def receive_lose(self, score):
        """
        Receive a message: the game is lost (misfires or forfeit).
        """
        pass

    def receive_game_over(self, score):
        """
        Receive a message: the game is over and is neither really lost
        (misfires, forfeit) nor a total victory (maximal score).
        """
        pass

    def receive_win(self, score):
        """
        Receive a message: the game is won (total victory).
        """
        pass

if __name__ == '__main__':
    my_antoine = Player(name='Antoine')
    my_antoine.test_str()

    import doctest
    doctest.testmod()
