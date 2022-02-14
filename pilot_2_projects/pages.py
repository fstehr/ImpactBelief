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
        cheap_project_first = self.participant.vars['cheap_project_first'][self.round_number - 1]
        # print("low_cost_project_first is", cheap_project_first)
        path = "global/img/matrices/"

        # use cheap_project_first variable to determine which project is displayed on the left
        if cheap_project_first == 1:
            # get characteristics of project A from parameters
            price_a = int(project['price_1'])
            player.num_x_A = int(project['num_X_1'])
            image_a = path + project['image_title_1']

            # get characteristics of project B from parameters
            price_b = int(project['price_2'])
            player.num_x_B = int(project['num_X_2'])
            image_b = path + project['image_title_2']

            # store parameters of project A in data set
            player.price_A = price_a
            player.efficiency_A = float(project['efficiency_1'])

            # store parameters of project B in data set
            player.price_B = price_b
            player.efficiency_B = float(project['efficiency_2'])

        else:
            # get characteristics of project A from parameters
            price_a = int(project['price_2'])
            image_a = path + project['image_title_2']
            player.price_A = price_a
            player.num_x_A = int(project['num_X_2'])
            player.efficiency_A = float(project['efficiency_2'])

            # get characteristics of project B from parameters
            price_b = int(project['price_1'])
            image_b = path + project['image_title_1']
            player.price_B = price_b
            player.num_x_B = int(project['num_X_1'])
            player.efficiency_B = float(project['efficiency_1'])

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
        if sum(fields_filled) == len(fields_filled):
            player.time_out = 0

            # bonus payment for belief A
            if abs(player.num_x_belief_A - player.num_x_A) <= 5:
                player.current_belief_A_payoff = player.belief_bonus
            else:
                player.current_belief_A_payoff = player.belief_bonus

            # bonus payment for belief B
            if abs(player.num_x_belief_B - player.num_x_B) <= 10:
                player.current_belief_B_payoff = player.belief_bonus
            else:
                player.current_belief_B_payoff = player.belief_bonus

            # bonus payment for joint donation
            player.current_donation_payoff = Constants.endowment - (player.donation_A * player.price_A) - \
                                             (player.donation_B * player.price_B)

            # randomly assign one of the three vars as final payoff in the payment round
            current_payoffs = [player.current_belief_A_payoff, player.current_belief_B_payoff,
                               player.current_donation_payoff]
            if self.round_number == self.participant.vars['payment_round']:
                player.payoff = random.choice(current_payoffs)
        else:            # if not all fields are filled, set time_out var to 1
            player.time_out = 1


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
