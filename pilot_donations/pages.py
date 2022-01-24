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
    form_fields = ['window_width', 'window_height', 'attention_check']

    def is_displayed(self):
        return self.round_number == 1


class Donation(Page):
    form_model = 'player'
    form_fields = ['donation_A']
    # form_fields = ['donation_A', 'donation_B']

    def vars_for_template(self):
        player = self.player
        num_projects = len(Constants.paras)
        project_number = player.round_number
        endowment = player.endowment

        # get current project from list of 'parameters'
        project = self.participant.vars['parameters'][self.round_number - 2]
        price_a = int(project['price_A'])
        num_doses_a = int(project['num_doses_A'])
        # price_b = int(project['price_B'])
        # num_doses_b = int(project['num_doses_B'])


        player.num_doses_A = num_doses_a
        player.price_A = price_a
        player.efficiency_A = float(project['efficiency_A'])
        # player.num_doses_B = num_doses_b
        # player.price_B = price_b
        # player.efficiency_B = int(project['efficiency_B'])

        return {'project_number': project_number, 'num_projects': num_projects,
                'endowment': endowment, 'num_doses_a': num_doses_a, 'price_a': price_a}
        # return {'price_a': price_a, 'price_b': price_b}

    def before_next_page(self):
        player = self.player
        player.current_payoff = player.endowment - (player.donation_A * player.price_A)
        if self.round_number == self.participant.vars['payment_round']:
            player.payoff = player.current_payoff


class Questionnaire(Page):
    form_model = 'player'
    form_fields = [ 'altruism', 'giving_type', 'finishing_time']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Thanks(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Questionnaire]
# page_sequence = [Welcome, Instructions, BeliefIntro, Belief, Feedback, Thanks]

