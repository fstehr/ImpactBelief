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


class BeliefIntro(Page):
    def is_displayed(self):
        return self.round_number == 1


class Uncertainty(Page):
    form_model = 'player'
    form_fields = ['num_x_belief_A', 'confidence_belief_A']


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
        project = self.participant.vars['parameters'][self.round_number - 2]
        player.num_x_true_A = int(project['num_x_A'])
        image_a = "img/"
        image_a += project['image_title_A']

        player.num_x_true_B = int(project['num_x_B'])
        image_b = "img/"
        image_b += project['image_title_B']
        # print("The current project is", project)
        return {'img_A': image_a, 'img_B': image_b}

    def before_next_page(self):
        player = self.player
        # store all answers in a list
        fields = [player.num_x_belief_A, player.num_x_belief_min_A, player.num_x_belief_max_A,
                  player.num_x_belief_B, player.num_x_belief_min_B, player.num_x_belief_max_B]
        fields_filled = []   # define a list with all boolean values indicating whether a field was filled or not
        for field in fields:
            fields_filled.append(bool(field))   # appends False if field value is None

        # check that no field was empty
        if sum(fields_filled) != len(fields_filled):
            player.time_out = 1
        else:
            player.time_out = 0


class Feedback(Page):
    form_model = 'player'
    form_fields = ['fun', 'speed', 'difficult', 'comments', 'finishing_time']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Thanks(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Belief, Uncertainty]
# page_sequence = [Welcome, Instructions, BeliefIntro, Belief, Feedback, Thanks]
