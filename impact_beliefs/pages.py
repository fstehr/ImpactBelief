from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from .models import Slider
from slider_task.pages import SliderTaskPage

import random


class IntroWelcome(Page):
    form_model = 'player'
    form_fields = ['starting_time']

    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    form_model = 'player'
    form_fields = ['window_width', 'window_height', 'gif_clicked', 'gif_watched', 'equation_clicked'] \
                  + ['cq{}'.format(i) for i in range(1, 5)]

    # display always in the first round of a new part.
    def is_displayed(self):
        return self.round_number == 1 \
               or self.round_number == len(Constants.paras) * (self.player.part - 1) + 2

    def vars_for_template(self):
        exchange_rate = int(1 / self.session.config['real_world_currency_per_point'])
        return {'exchange_rate': exchange_rate}


class Sliders(SliderTaskPage):
    Constants = Constants
    Slider = Slider

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        player = self.player
        player.current_payoff = Constants.endowment
        # print("current payoff is", player.current_payoff, "=", Constants.endowment, "-", player.price, "*", player.donation)
        if self.round_number == self.participant.vars['payment_round']:
            player.payoff = player.current_payoff


class TrialBelief(Page):
    form_model = 'player'
    form_fields = ['trial_belief_{}'.format(i) for i in range(1, 4)]

    def js_vars(self):
        return dict(
            sec_per_matrix=Constants.sec_per_matrix,
        )

    def is_displayed(self):
        return self.round_number == 2


class Introbelief(Page):
    def is_displayed(self):
        return self.round_number == 2


class Belief(Page):
    form_model = 'player'
    form_fields = ['num_x_belief']

    timeout_seconds = 3 + Constants.sec_per_matrix + Constants.sec_to_answer

    def is_displayed(self):
        player = self.player
        return player.part == 1 or player.part == 3

    def vars_for_template(self):
        player = self.player
        task_number = player.part + 1
        # get current project from list of 'parameters'
        project = self.participant.vars['parameters'][self.round_number - 2]
        player.project_id = int(project['project_id'])
        player.price = float(project['price_ECU'])
        player.num_x_true = int(project['num_x'])
        if player.part == 1:
            image = "img/"
            image += project['image_title_1']
        elif player.part == 3:
            image = "img/"
            image += project['image_title_2']
        # print("The current project is", project)

        return {'task_number': task_number, 'img_to_show': image, 'project': player.project_id,
                'price_to_show': player.price}

    def js_vars(self):
        return dict(
            sec_per_matrix=Constants.sec_per_matrix,
        )

    def before_next_page(self):
        player = self.player
        timeout_happened = self.timeout_happened

        player.current_payoff = Constants.beliefs_fixed_payment + max(0, Constants.beliefs_fixed_payment - 0.00375 * (
                (player.num_x_belief - player.num_x_true) ** 2))
        # print("current payoff is", player.current_payoff, "= 150 + max(0,150 - 0.00375*(", player.num_x_belief, "-", player.num_x_true, ")^2")
        if self.round_number == self.participant.vars['payment_round']:
            if timeout_happened:
                player.payoff = 0
            else:
                player.payoff = player.current_payoff

        if timeout_happened:
            player.timeout = True
            self.participant.vars['timeout_counter'] += 1
        print("time out counter is ", self.participant.vars['timeout_counter'])


        # store belief in participant vars in the position of the project id to make it easily callable on donation page
        if player.part == 1:
            self.participant.vars['beliefs_part1'][player.project_id - 1] = player.num_x_belief
            # belief_list = self.participant.vars['beliefs_part1']
            # print("Belief list in current treatment is", belief_list)
        elif player.part == 3:
            self.participant.vars['beliefs_part3'][player.project_id - 1] = player.num_x_belief
            # belief_list = self.participant.vars['beliefs_part3']
            # print("Belief list in current treatment is", belief_list)

    def app_after_this_page(self, upcoming_apps):
        if self.participant.vars['timeout_counter'] == 2:
            return "payment_info"


class Donation(Page):
    form_model = 'player'
    form_fields = ['donation']

    def is_displayed(self):
        player = self.player
        return player.part == 2 or player.part == 4

    def vars_for_template(self):
        player = self.player
        task_number = player.part + 1
        project = self.participant.vars['parameters'][self.round_number - 2]
        player.project_id = int(project['project_id'])
        player.price = float(project['price_ECU'])
        player.num_x_true = int(project['num_x'])  # store true num of xs again in dataset in same row as donation

        # Look-Up indicated belief from the correct list of participant vars & store again in dataset in current row
        if player.part == 2:
            player.num_x_belief = self.participant.vars['beliefs_part1'][player.project_id - 1]
        elif player.part == 4:
            player.num_x_belief = self.participant.vars['beliefs_part3'][player.project_id - 1]

        return {'task_number': task_number, 'project': player.project_id, 'price_to_show': player.price,
                'belief': player.num_x_belief, 'num_X_true': player.num_x_true}

    def js_vars(self):
        player = self.player

        if player.treatment == "Info":
            carbon_emissions = player.num_x_true * Constants.real_world_kg_co2_per_x
        else:
            carbon_emissions = player.num_x_belief * Constants.real_world_kg_co2_per_x

        car_km = carbon_emissions * Constants.car_km_per_kg_co2
        return dict(
            display_km=car_km,
            display_co2=carbon_emissions,
        )

    def before_next_page(self):
        player = self.player
        # store belief in participant vars in the position of the project id to make it easily callable on donation page
        player.current_payoff = Constants.endowment - (player.price * player.donation)
        # print("current payoff is", player.current_payoff, "=", Constants.endowment, "-", player.price, "*", player.donation)
        if self.round_number == self.participant.vars['payment_round']:
            player.payoff = player.current_payoff


class CarbonBelief(Page):
    form_model = 'player'

    def get_form_fields(player):
        fields = ['co2_belief_car', 'co2_belief_plane', 'co2_belief_renewables', 'co2_belief_hybrid',
                  'co2_belief_vegan', 'co2_belief_laundry', 'co2_belief_recycle', 'co2_belief_dryer',
                  'co2_belief_led']
        random.shuffle(fields)
        return fields

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class CostBelief(Page):
    form_model = 'player'

    def get_form_fields(player):
        fields = ['cost_belief_car', 'cost_belief_plane', 'cost_belief_renewables', 'cost_belief_hybrid',
                  'cost_belief_vegan', 'cost_belief_laundry', 'cost_belief_recycle', 'cost_belief_dryer',
                  'cost_belief_led']
        random.shuffle(fields)
        return fields

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'levelOfEducation', 'political', 'income', 'employment', 'finishing_time']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Belief,
    IntroWelcome,
    Questionnaire
]
