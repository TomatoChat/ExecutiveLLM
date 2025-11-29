from axelrod import Action, Player


class MyMimic(Player):
    """
    Cooperate on the first move, then copy the opponent's last move.
    """

    name = "My Mimic"

    classifier = {
        "memory_depth": float("inf"),  # can remember infinite history
        "stochastic": True,  # stochastic strategies are allowed
        "inspects_source": False,  # does not inspect source
        "manipulates_source": False,  # does not manipulate source
        "manipulates_state": False,  # does not manipulate state
    }

    def strategy(self, opponent):
        if len(self.history) == 0:
            return Action.C  # Action.D

        return opponent.history[-1]
