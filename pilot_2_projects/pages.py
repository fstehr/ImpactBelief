from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
import random


class Welcome(Page):
    form_model = 'player'
    form_fields = ['starting_time', 'is_mobile']

    def is_displayed(self):
        return self.round_number == 1


class NoPhone(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.is_mobile


class Instructions(Page):
    form_model = 'player'
    form_fields = ['window_width', 'window_height', 'attention_check']

    def is_displayed(self):
        return self.round_number == 1


class AttentionFail(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.attention_check != "apple"


class Belief(Page):
    form_model = 'player'
    form_fields = ['num_x_belief_A', 'confidence_belief_A', 'donation_A',
                   'num_x_belief_B', 'confidence_belief_B', 'donation_B', 'page_loaded']

    def js_vars(self):
        return dict(
            sec_intro=Constants.sec_intro,
            sec_per_matrix=Constants.sec_per_matrix,
            sec_to_answer=Constants.sec_to_answer,
        )

    def vars_for_template(self):
        player = self.player

        # get current project from list of 'parameters'
        endowment = Constants.endowment
        project = self.participant.vars['parameters'][self.round_number - 1]
        # print("project is", project)
        project_A_first = self.participant.vars['project_A_first'][self.round_number - 1]
        # print("project_A_first is", project_A_first)

        # get characteristics of project A from parameters
        price_a = int(project['price_A'])
        num_doses_a = int(project['num_doses_A'])
        player.num_x_A = int(project['num_X_A'])
        image_a = "global/img/matrices/"
        image_a += project['image_title_A']

        # get characteristics of project B from parameters
        price_b = int(project['price_B'])
        num_doses_b = int(project['num_doses_B'])
        player.num_x_B = int(project['num_X_B'])
        image_b = "global/img/matrices/"
        image_b += project['image_title_B']

        # store parameters of project A in data set
        player.price_A = price_a
        player.efficiency_A = float(project['efficiency_A'])

        # store parameters of project B in data set
        player.price_B = price_b
        player.efficiency_B = float(project['efficiency_B'])

        return {'endowment': endowment, 'img_a': image_a, 'img_b': image_b,
                'price_a': price_a, 'price_b': price_b}

    def before_next_page(self):
        player = self.player
        # store all answers in a list
        fields = [player.num_x_belief_A, player.num_x_belief_B]
        fields_filled = []  # define a list with all boolean values indicating whether a field was filled or not
        for field in fields:
            fields_filled.append(bool(field))  # appends False if field value is None

        # check that no field was empty
        if sum(fields_filled) != len(fields_filled):
            player.time_out = 1
        else:
            player.time_out = 0

        # bonus payment for belief A
        if abs(player.num_x_belief_A - player.num_x_A) <= 10:
            player.current_belief_A_payoff = player.belief_bonus
        else:
            player.current_belief_A_payoff = player.belief_bonus

        # bonus payment for belief B
        if abs(player.num_x_belief_B - player.num_x_B) <= 10:
            player.current_belief_B_payoff = player.belief_bonus
        else:
            player.current_belief_B_payoff = player.belief_bonus

        # bonus payment for joint donation
        player.current_donation_payoff = player.endowment - (player.donation_A * player.price_A) - \
                                         (player.donation_B * player.price_B)

        current_payoffs = [player.current_belief_A_payoff, player.current_belief_B_payoff,
                           player.current_donation_payoff]

        if self.round_number == self.participant.vars['payment_round']:
            player.payoff = random.choice(current_payoffs)


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['altruism', 'giving_type', 'finishing_time']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Thanks(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Belief]
# page_sequence = [Welcome, Instructions, BeliefIntro, Belief, Feedback, Thanks]
