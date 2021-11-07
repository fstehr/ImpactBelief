from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Welcome(Page):
    form_model = 'player'
    form_fields = ['starting_time', 'is_mobile']

    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    form_model = 'player'
    form_fields = ['attention_check']

    def is_displayed(self):
        return self.round_number == 1


class BeliefIntro(Page):
    def is_displayed(self):
        return self.round_number == 1


class Belief(Page):
    form_model = 'player'
    form_fields = ['num_x_belief_A', 'num_x_belief_min_A', 'num_x_belief_max_A',
                   'num_x_belief_B', 'num_x_belief_min_B', 'num_x_belief_max_B']

    def js_vars(self):
        return dict(
            sec_intro=Constants.sec_intro,
            sec_per_matrix=Constants.sec_per_matrix,
        )

class Feedback(Page):
    form_model = 'player'
    form_fields = ['fun', 'difficult', 'comments', 'finishing_time']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Thanks(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Welcome, Instructions, BeliefIntro, Belief, Feedback, Thanks]
