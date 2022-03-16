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
    form_fields = ['window_width', 'window_height', 'cq_1', 'cq_2', 'cq_3', 'attention_check']

    def is_displayed(self):
        return self.round_number == 1


class AttentionFail(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.player.attention_check != "apple"


class TrialPage(Page):
    form_model = 'player'
    form_fields = ['trial_belief_A', 'trial_confidence_A', 'trial_donation_A',
                   'trial_belief_B', 'trial_confidence_B', 'trial_donation_B']

    def is_displayed(self):
        return self.round_number == 1

    def js_vars(self):
        return dict(
            sec_intro=Constants.sec_intro,
            sec_per_matrix=Constants.sec_per_matrix,
            sec_to_answer=Constants.sec_to_answer,
        )


class Donation(Page):
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
        player.comparison_id = int(project['id'])
        player.comparison_type = project['comparison']
        cheap_project_first = self.participant.vars['cheap_project_first'][self.round_number - 1]
        path = "global/img/matrices/matrix_"

        # use cheap_project_first variable to determine which project is displayed on the left
        if cheap_project_first == 1:
            # get characteristics of project A from parameters
            price_a = int(project['price_1'])
            player.num_x_A = int(project['num_X_1'])
            img_a_number = self.participant.vars['img_a'][self.round_number - 1]
            image_a = path + str(player.num_x_A) + "_" + str(img_a_number) + ".png"
            #print(image_a)

            # get characteristics of project B from parameters
            price_b = int(project['price_2'])
            player.num_x_B = int(project['num_X_2'])
            img_b_number = self.participant.vars['img_b'][self.round_number - 1]
            image_b = path + str(player.num_x_B) + "_" + str(img_b_number) + ".png"
            #print(image_b)

            # store parameters of project A in data set
            player.price_A = price_a
            player.efficiency_A = float(project['efficiency_1'])
            player.img_A = img_a_number

            # store parameters of project B in data set
            player.price_B = price_b
            player.efficiency_B = float(project['efficiency_2'])
            player.img_B = img_b_number

        else:
            # get characteristics of project A from parameters
            price_a = int(project['price_2'])
            player.num_x_A = int(project['num_X_2'])
            img_a_number = self.participant.vars['img_a'][self.round_number - 1]
            image_a = path + str(player.num_x_A) + "_" + str(img_a_number) + ".png"
            #print(image_a)

            # get characteristics of project B from parameters
            price_b = int(project['price_1'])
            player.num_x_B = int(project['num_X_1'])
            img_b_number = self.participant.vars['img_b'][self.round_number - 1]
            image_b = path + str(player.num_x_B) + "_" + str(img_b_number) + ".png"
            #print(image_b)

            # store parameters of project A in data set
            player.price_A = price_a
            player.efficiency_A = float(project['efficiency_2'])
            player.img_A = img_a_number

            # store parameters of project B in data set
            player.price_B = price_b
            player.efficiency_B = float(project['efficiency_1'])
            player.img_B = img_b_number

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
            if abs(player.num_x_belief_A - player.num_x_A) <= 10:
                player.current_belief_A_payoff = player.belief_bonus
            else:
                player.current_belief_A_payoff = 0

            # bonus payment for belief B
            if abs(player.num_x_belief_B - player.num_x_B) <= 10:
                player.current_belief_B_payoff = player.belief_bonus
            else:
                player.current_belief_B_payoff = 0

            # bonus payment for joint donation
            player.current_donation_payoff = Constants.endowment - (player.donation_A * player.price_A) - \
                                             (player.donation_B * player.price_B)

            # randomly assign one of the three vars as final payoff in the payment round
            urn = [0, 1, 2]
            payoff_decision = ["belief_A", "belief_B", "donation"]
            current_payoffs = [player.current_belief_A_payoff, player.current_belief_B_payoff,
                               player.current_donation_payoff]
            if self.round_number == self.participant.vars['payment_round']:
                payout = random.choice(urn)
                player.payoff = current_payoffs[payout]
                player.payoff_decision = payoff_decision[payout]

        else:            # if not all fields are filled, set time_out var to 1
            player.time_out = 1


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['altruism', 'giving_type', 'finishing_time']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Thanks(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


# page_sequence = [Welcome, NoPhone, Instructions, AttentionFail, TrialPage, Donation, Questionnaire, Feedback, Thanks]
page_sequence = [Donation]
