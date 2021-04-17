from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from .models import Slider
from slider_task.pages import SliderTaskPage



class Intro(Page):
    def is_displayed(self):
        return self.round_number == 1

class IntroWelcome(Page):
    def is_displayed(self):
        return self.round_number == 1


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


class Belief(Page):
    form_model = 'player'
    form_fields = ['num_x_belief']

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

        return {'task_number': task_number, 'img_to_show': image, 'project': player.project_id, 'price_to_show': player.price}

    def before_next_page(self):
        player = self.player
        player.current_payoff = Constants.beliefs_fixed_payment + max(0, Constants.beliefs_fixed_payment - 0.00375*((player.num_x_belief-player.num_x_true)**2))
        # print("current payoff is", player.current_payoff, "= 150 + max(0,150 - 0.00375*(", player.num_x_belief, "-", player.num_x_true, ")^2")
        if self.round_number == self.participant.vars['payment_round']:
            player.payoff = player.current_payoff

        # store belief in participant vars in the position of the project id to make it easily callable on donation page
        if player.part == 1:
            self.participant.vars['beliefs_part1'][player.project_id-1] = player.num_x_belief
            # belief_list = self.participant.vars['beliefs_part1']
            # print("Belief list in current treatment is", belief_list)
        elif player.part == 3:
            self.participant.vars['beliefs_part3'][player.project_id - 1] = player.num_x_belief
            # belief_list = self.participant.vars['beliefs_part3']
            # print("Belief list in current treatment is", belief_list)


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
        player.num_x_true = int(project['num_x'])   # store true num of xs again in dataset in same row as donation

        # Look-Up indicated belief from the correct list of participant vars & store again in dataset in current row
        if player.part == 2:
            player.num_x_belief = self.participant.vars['beliefs_part1'][player.project_id-1]
        elif player.part == 4:
            player.num_x_belief = self.participant.vars['beliefs_part3'][player.project_id-1]

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
    form_fields = ['plane_belief']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Outro(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        final_payoff = self.participant.payoff
        final_payoff_plus_part_fee = self.participant.payoff_plus_participation_fee()

        return {'final_payoff_display': final_payoff, 'final_payoff_plus_part_fee_display': final_payoff_plus_part_fee}


page_sequence = [
    Intro,
    Sliders,
    Belief,
    Donation,
    Outro
    ]
