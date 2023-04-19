from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Slider
from slider_task.pages import SliderTaskPage
from time import time
import random, csv, math


class Welcome(Page):    # Welcome page that is displayed to everybody at the beginning of the experiment
    def is_displayed(self):
        return self.round_number == 1 \
                or self.round_number == (Constants.num_rounds_BDM + 1) \
                   or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

    def vars_for_template(self):
        return {'first_treatment_round': (Constants.num_rounds_BDM + 1),
                'mode': self.session.config['mode']}


class IntroductionWaitForAll(WaitPage):   # Wait for all players before a new part is started
    wait_for_all_groups = True
    body_text = "Waiting for the other participants."

    def is_displayed(self):
        return self.round_number == 1 \
               or self.round_number == (Constants.num_rounds_BDM + 1) \
               or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)


class IntroParts(Page):   # Introduction page that asks subjects to read the paper instructions. Password that is needed to continue is verbally announced
    form_model = 'player'
    form_fields = ['password']

    def password_error_message(self, value):   # error message if the password for the respective round is not correct
        if self.round_number == 1:
            if value != Constants.password1:
                return 'Please enter the correct password.'
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if value != Constants.password3:
                return 'Please enter the correct password.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if value != Constants.password4:
                return 'Please enter the correct password.'

    def is_displayed(self):
        return self.round_number == 1 \
               or self.round_number == (Constants.num_rounds_BDM + 1) \
               or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

    def before_next_page(self):
        if self.round_number == 1:
            self.player.prepare_sliders(num=Constants.trialsliders, min=0, max=100)
            self.player.slider_solving_time = time()

    def vars_for_template(self):
        return {'first_treatment_round': (Constants.num_rounds_BDM + 1)}


class SlidersTrial(SliderTaskPage):
    Constants = Constants
    Slider = Slider

    def is_displayed(self):
        return self.round_number == 1


class CalcPricesWaitPage(WaitPage):
    body_text = "Waiting for the other participants."

    def after_all_players_arrive(self):
        self.group.current_price()


class IntroBDM(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):   # reset the field value to None, in order not to display any value that might have been recorded in the same round
        self.player.password = None


class BeforeBDMWait(Page):
    form_model = 'player'
    form_fields = ['password']

    def is_displayed(self):
        return self.round_number == 1

    def password_error_message(self, value):   # error message if the password for the respective round is not correct
        if self.round_number == 1:
            if value != Constants.password2:
                return 'Please enter the correct password.'


class SlidersBDM(Page):
    form_model = 'player'
    form_fields = ['sliders_WTP']

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds_BDM

    # dynamically set the minimum value for sliders_WTP to what was entered in the first round to enforce consistency
    def sliders_WTP_min(self):
        if self.round_number == 1:
            return 0
        else:
            return self.player.in_round(self.round_number - 1).sliders_WTP

    def vars_for_template(self):   # pass this value to the template to also display the new lower bound in the second round
        if self.round_number == 1:
            WTP_sliders_previous_BDM = None
        else:
            WTP_sliders_previous_BDM = self.player.in_round(self.round_number - 1).sliders_WTP
        return {'WTP_sliders_previous_BDM': WTP_sliders_previous_BDM}


class ControlQuestions(Page):
    form_model = 'player'
    form_fields = ['q1_answer_1', 'q2_answer_1', 'q3_answer_1', 'q4_answer_1', 'q5_answer_1', 'q6_answer_1', 'q7_answer_1', 'q8_answer_1']

    def is_displayed(self):
        return self.round_number == (Constants.num_rounds_BDM + 1) \
               or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

    def vars_for_template(self):        # Display different control questions for different treatments

        self.player.time_on_first_control_question_screen = time()   # get the time stamp when page is entered

        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.treatment == 'Individual':
                return {
                    'q1_label': '{}'.format(Constants.question_ind[0]),
                    'q2_label': '{}'.format(Constants.question_ind[1]),
                    'q3_label': '{}'.format(Constants.question_ind[2]),
                    'q4_label': '{}'.format(Constants.question_ind[3]),
                    'q5_label': '{}'.format(Constants.question_ind[4]),
                    'q6_label': '{}'.format(Constants.question_ind[5]),
                    'q7_label': '{}'.format(Constants.question_ind[6]),
                    'q8_label': '{}'.format(Constants.question_ind[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_ind[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_ind[5]),
                }
            if self.player.treatment == 'Risk':
                return {
                    'q1_label': '{}'.format(Constants.question_risk[0]),
                    'q2_label': '{}'.format(Constants.question_risk[1]),
                    'q3_label': '{}'.format(Constants.question_risk[2]),
                    'q4_label': '{}'.format(Constants.question_risk[3]),
                    'q5_label': '{}'.format(Constants.question_risk[4]),
                    'q6_label': '{}'.format(Constants.question_risk[5]),
                    'q7_label': '{}'.format(Constants.question_risk[6]),
                    'q8_label': '{}'.format(Constants.question_risk[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_risk[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_risk[5]),
                }
            if self.player.treatment == 'Harm':
                return {
                    'q1_label': '{}'.format(Constants.question_harm[0]),
                    'q2_label': '{}'.format(Constants.question_harm[1]),
                    'q3_label': '{}'.format(Constants.question_harm[2]),
                    'q4_label': '{}'.format(Constants.question_harm[3]),
                    'q5_label': '{}'.format(Constants.question_harm[4]),
                    'q6_label': '{}'.format(Constants.question_harm[5]),
                    'q7_label': '{}'.format(Constants.question_harm[6]),
                    'q8_label': '{}'.format(Constants.question_harm[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_harm[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_harm[5]),
                }
            if self.player.treatment == 'Responsibility':
                return {
                    'q1_label': '{}'.format(Constants.question_resp[0]),
                    'q2_label': '{}'.format(Constants.question_resp[1]),
                    'q3_label': '{}'.format(Constants.question_resp[2]),
                    'q4_label': '{}'.format(Constants.question_resp[3]),
                    'q5_label': '{}'.format(Constants.question_resp[4]),
                    'q6_label': '{}'.format(Constants.question_resp[5]),
                    'q7_label': '{}'.format(Constants.question_resp[6]),
                    'q8_label': '{}'.format(Constants.question_resp[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_resp[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_resp[5]),
                }
        else:
            if self.player.treatment == 'Individual':
                return {
                    'q1_label': '{}'.format(Constants.question_ind[8]),
                    'q2_label': '{}'.format(Constants.question_ind[9]),
                    'q3_label': '{}'.format(Constants.question_ind[10]),
                    'q4_label': '{}'.format(Constants.question_ind[11]),
                    'q5_label': '{}'.format(Constants.question_ind[12]),
                    'q6_label': '{}'.format(Constants.question_ind[13]),
                    'q7_label': '{}'.format(Constants.question_ind[14]),
                    'q8_label': '{}'.format(Constants.question_ind[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_ind[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_ind[13]),
                }
            if self.player.treatment == 'Risk':
                return {
                    'q1_label': '{}'.format(Constants.question_risk[8]),
                    'q2_label': '{}'.format(Constants.question_risk[9]),
                    'q3_label': '{}'.format(Constants.question_risk[10]),
                    'q4_label': '{}'.format(Constants.question_risk[11]),
                    'q5_label': '{}'.format(Constants.question_risk[12]),
                    'q6_label': '{}'.format(Constants.question_risk[13]),
                    'q7_label': '{}'.format(Constants.question_risk[14]),
                    'q8_label': '{}'.format(Constants.question_risk[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_risk[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_risk[13]),
                }
            if self.player.treatment == 'Harm':
                return {
                    'q1_label': '{}'.format(Constants.question_harm[8]),
                    'q2_label': '{}'.format(Constants.question_harm[9]),
                    'q3_label': '{}'.format(Constants.question_harm[10]),
                    'q4_label': '{}'.format(Constants.question_harm[11]),
                    'q5_label': '{}'.format(Constants.question_harm[12]),
                    'q6_label': '{}'.format(Constants.question_harm[13]),
                    'q7_label': '{}'.format(Constants.question_harm[14]),
                    'q8_label': '{}'.format(Constants.question_harm[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_harm[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_harm[13]),
                }
            if self.player.treatment == 'Responsibility':
                return {
                    'q1_label': '{}'.format(Constants.question_resp[8]),
                    'q2_label': '{}'.format(Constants.question_resp[9]),
                    'q3_label': '{}'.format(Constants.question_resp[10]),
                    'q4_label': '{}'.format(Constants.question_resp[11]),
                    'q5_label': '{}'.format(Constants.question_resp[12]),
                    'q6_label': '{}'.format(Constants.question_resp[13]),
                    'q7_label': '{}'.format(Constants.question_resp[14]),
                    'q8_label': '{}'.format(Constants.question_resp[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_resp[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_resp[13]),
                }

    def before_next_page(self):  # update time variable to record the time spent on the page
        self.player.time_on_first_control_question_screen = time() - self.player.time_on_first_control_question_screen
        self.player.time_on_second_control_question_screen = time()  # get the time stamp when page is entered
        return self.player.check_correct()


class ControlQuestionsCorrected(Page):

    form_model = 'player'
    form_fields = ['q1_answer_2', 'q2_answer_2', 'q3_answer_2', 'q4_answer_2', 'q5_answer_2', 'q6_answer_2', 'q7_answer_2', 'q8_answer_2']

    def is_displayed(self):
        return self.round_number == (Constants.num_rounds_BDM + 1) \
               or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

    def q1_answer_2_error_message(self, value):   # define error messages if an answer was not correct
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q1_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[0]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[0]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[0]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[0]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q1_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[8]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[8]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[8]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[8]):
                    return 'Please check your answer.'

    def q2_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q2_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[1]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[1]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[1]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[1]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q2_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[9]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[9]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[9]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[9]):
                    return 'Please check your answer.'

    def q3_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q3_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[2]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[2]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[2]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[2]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q3_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[10]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[10]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[10]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[10]):
                    return 'Please check your answer.'

    def q4_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q4_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[3]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[3]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[3]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[3]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q4_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[11]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[11]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[11]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[11]):
                    return 'Please check your answer.'

    def q5_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q5_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[4]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[4]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[4]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[4]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q5_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[12]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[12]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[12]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[12]):
                    return 'Please check your answer.'

    def q6_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q6_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[5]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[5]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[5]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[5]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q6_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[13]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[13]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[13]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[13]):
                    return 'Please check your answer.'

    def q7_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q7_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[6]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[6]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[6]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[6]):
                    return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q7_correct == 0:
                if self.player.treatment == "Individual" and value != int(Constants.solution_ind[14]):
                    return 'Please check your answer.'
                if self.player.treatment == "Risk" and value != int(Constants.solution_risk[14]):
                    return 'Please check your answer.'
                if self.player.treatment == "Harm" and value != int(Constants.solution_harm[14]):
                    return 'Please check your answer.'
                if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[14]):
                    return 'Please check your answer.'

    def q8_answer_2_error_message(self, value):
        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.q8_correct == 0:
                if self.player.q7_correct == 0:
                    if self.player.treatment == "Individual" and value != int(Constants.solution_ind[7]):
                        return 'Please check your answer.'
                    if self.player.treatment == "Risk" and value != int(Constants.solution_risk[7]):
                        return 'Please check your answer.'
                    if self.player.treatment == "Harm" and value != int(Constants.solution_harm[7]):
                        return 'Please check your answer.'
                    if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[7]):
                        return 'Please check your answer.'
        if self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.q8_correct == 0:
                if self.player.q7_correct == 0:
                    if self.player.treatment == "Individual" and value != int(Constants.solution_ind[15]):
                        return 'Please check your answer.'
                    if self.player.treatment == "Risk" and value != int(Constants.solution_risk[15]):
                        return 'Please check your answer.'
                    if self.player.treatment == "Harm" and value != int(Constants.solution_harm[15]):
                        return 'Please check your answer.'
                    if self.player.treatment == "Responsibility" and value != int(Constants.solution_resp[15]):
                        return 'Please check your answer.'

    def vars_for_template(self):  # Display those questions again that were not answered correctly  and include a helptext which explains the answer
        # self.player.time_on_second_control_question_screen = time()   # get the time stamp when page is entered

        if self.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.treatment == 'Individual':
                return {
                    'q1_label': '{}'.format(Constants.question_ind[0]),
                    'q2_label': '{}'.format(Constants.question_ind[1]),
                    'q3_label': '{}'.format(Constants.question_ind[2]),
                    'q4_label': '{}'.format(Constants.question_ind[3]),
                    'q5_label': '{}'.format(Constants.question_ind[4]),
                    'q6_label': '{}'.format(Constants.question_ind[5]),
                    'q7_label': '{}'.format(Constants.question_ind[6]),
                    'q8_label': '{}'.format(Constants.question_ind[7]),
                    'q1_helptext': '{}'.format(Constants.helptext_ind[0]),
                    'q2_helptext': '{}'.format(Constants.helptext_ind[1]),
                    'q3_helptext': '{}'.format(Constants.helptext_ind[2]),
                    'q4_helptext': '{}'.format(Constants.helptext_ind[3]),
                    'q5_helptext': '{}'.format(Constants.helptext_ind[4]),
                    'q6_helptext': '{}'.format(Constants.helptext_ind[5]),
                    'q7_helptext': '{}'.format(Constants.helptext_ind[6]),
                    'q8_helptext': '{}'.format(Constants.helptext_ind[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_ind[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_ind[5]),
                }
            if self.player.treatment == 'Risk':
                return {
                    'q1_label': '{}'.format(Constants.question_risk[0]),
                    'q2_label': '{}'.format(Constants.question_risk[1]),
                    'q3_label': '{}'.format(Constants.question_risk[2]),
                    'q4_label': '{}'.format(Constants.question_risk[3]),
                    'q5_label': '{}'.format(Constants.question_risk[4]),
                    'q6_label': '{}'.format(Constants.question_risk[5]),
                    'q7_label': '{}'.format(Constants.question_risk[6]),
                    'q8_label': '{}'.format(Constants.question_risk[7]),
                    'q1_helptext': '{}'.format(Constants.helptext_risk[0]),
                    'q2_helptext': '{}'.format(Constants.helptext_risk[1]),
                    'q3_helptext': '{}'.format(Constants.helptext_risk[2]),
                    'q4_helptext': '{}'.format(Constants.helptext_risk[3]),
                    'q5_helptext': '{}'.format(Constants.helptext_risk[4]),
                    'q6_helptext': '{}'.format(Constants.helptext_risk[5]),
                    'q7_helptext': '{}'.format(Constants.helptext_risk[6]),
                    'q8_helptext': '{}'.format(Constants.helptext_risk[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_risk[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_risk[5]),
                }
            if self.player.treatment == 'Harm':
                return {
                    'q1_label': '{}'.format(Constants.question_harm[0]),
                    'q2_label': '{}'.format(Constants.question_harm[1]),
                    'q3_label': '{}'.format(Constants.question_harm[2]),
                    'q4_label': '{}'.format(Constants.question_harm[3]),
                    'q5_label': '{}'.format(Constants.question_harm[4]),
                    'q6_label': '{}'.format(Constants.question_harm[5]),
                    'q7_label': '{}'.format(Constants.question_harm[6]),
                    'q8_label': '{}'.format(Constants.question_harm[7]),
                    'q1_helptext': '{}'.format(Constants.helptext_harm[0]),
                    'q2_helptext': '{}'.format(Constants.helptext_harm[1]),
                    'q3_helptext': '{}'.format(Constants.helptext_harm[2]),
                    'q4_helptext': '{}'.format(Constants.helptext_harm[3]),
                    'q5_helptext': '{}'.format(Constants.helptext_harm[4]),
                    'q6_helptext': '{}'.format(Constants.helptext_harm[5]),
                    'q7_helptext': '{}'.format(Constants.helptext_harm[6]),
                    'q8_helptext': '{}'.format(Constants.helptext_harm[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_harm[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_harm[5]),
                }
            if self.player.treatment == 'Responsibility':
                return {
                    'q1_label': '{}'.format(Constants.question_resp[0]),
                    'q2_label': '{}'.format(Constants.question_resp[1]),
                    'q3_label': '{}'.format(Constants.question_resp[2]),
                    'q4_label': '{}'.format(Constants.question_resp[3]),
                    'q5_label': '{}'.format(Constants.question_resp[4]),
                    'q6_label': '{}'.format(Constants.question_resp[5]),
                    'q7_label': '{}'.format(Constants.question_resp[6]),
                    'q8_label': '{}'.format(Constants.question_resp[7]),
                    'q1_helptext': '{}'.format(Constants.helptext_resp[0]),
                    'q2_helptext': '{}'.format(Constants.helptext_resp[1]),
                    'q3_helptext': '{}'.format(Constants.helptext_resp[2]),
                    'q4_helptext': '{}'.format(Constants.helptext_resp[3]),
                    'q5_helptext': '{}'.format(Constants.helptext_resp[4]),
                    'q6_helptext': '{}'.format(Constants.helptext_resp[5]),
                    'q7_helptext': '{}'.format(Constants.helptext_resp[6]),
                    'q8_helptext': '{}'.format(Constants.helptext_resp[7]),
                    'q3_scenario': '{}'.format(Constants.scenario_resp[2]),
                    'q4_scenario': '{}'.format(Constants.scenario_resp[5]),
                }
        else:
            if self.player.treatment == 'Individual':
                return {
                    'q1_label': '{}'.format(Constants.question_ind[8]),
                    'q2_label': '{}'.format(Constants.question_ind[9]),
                    'q3_label': '{}'.format(Constants.question_ind[10]),
                    'q4_label': '{}'.format(Constants.question_ind[11]),
                    'q5_label': '{}'.format(Constants.question_ind[12]),
                    'q6_label': '{}'.format(Constants.question_ind[13]),
                    'q7_label': '{}'.format(Constants.question_ind[14]),
                    'q8_label': '{}'.format(Constants.question_ind[15]),
                    'q1_helptext': '{}'.format(Constants.helptext_ind[8]),
                    'q2_helptext': '{}'.format(Constants.helptext_ind[9]),
                    'q3_helptext': '{}'.format(Constants.helptext_ind[10]),
                    'q4_helptext': '{}'.format(Constants.helptext_ind[11]),
                    'q5_helptext': '{}'.format(Constants.helptext_ind[12]),
                    'q6_helptext': '{}'.format(Constants.helptext_ind[13]),
                    'q7_helptext': '{}'.format(Constants.helptext_ind[14]),
                    'q8_helptext': '{}'.format(Constants.helptext_ind[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_ind[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_ind[13]),
                }
            if self.player.treatment == 'Risk':
                return {
                    'q1_label': '{}'.format(Constants.question_risk[8]),
                    'q2_label': '{}'.format(Constants.question_risk[9]),
                    'q3_label': '{}'.format(Constants.question_risk[10]),
                    'q4_label': '{}'.format(Constants.question_risk[11]),
                    'q5_label': '{}'.format(Constants.question_risk[12]),
                    'q6_label': '{}'.format(Constants.question_risk[13]),
                    'q7_label': '{}'.format(Constants.question_risk[14]),
                    'q8_label': '{}'.format(Constants.question_risk[15]),
                    'q1_helptext': '{}'.format(Constants.helptext_risk[8]),
                    'q2_helptext': '{}'.format(Constants.helptext_risk[9]),
                    'q3_helptext': '{}'.format(Constants.helptext_risk[10]),
                    'q4_helptext': '{}'.format(Constants.helptext_risk[11]),
                    'q5_helptext': '{}'.format(Constants.helptext_risk[12]),
                    'q6_helptext': '{}'.format(Constants.helptext_risk[13]),
                    'q7_helptext': '{}'.format(Constants.helptext_risk[14]),
                    'q8_helptext': '{}'.format(Constants.helptext_risk[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_risk[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_risk[13]),
                }
            if self.player.treatment == 'Harm':
                return {
                    'q1_label': '{}'.format(Constants.question_harm[8]),
                    'q2_label': '{}'.format(Constants.question_harm[9]),
                    'q3_label': '{}'.format(Constants.question_harm[10]),
                    'q4_label': '{}'.format(Constants.question_harm[11]),
                    'q5_label': '{}'.format(Constants.question_harm[12]),
                    'q6_label': '{}'.format(Constants.question_harm[13]),
                    'q7_label': '{}'.format(Constants.question_harm[14]),
                    'q8_label': '{}'.format(Constants.question_harm[15]),
                    'q1_helptext': '{}'.format(Constants.helptext_harm[8]),
                    'q2_helptext': '{}'.format(Constants.helptext_harm[9]),
                    'q3_helptext': '{}'.format(Constants.helptext_harm[10]),
                    'q4_helptext': '{}'.format(Constants.helptext_harm[11]),
                    'q5_helptext': '{}'.format(Constants.helptext_harm[12]),
                    'q6_helptext': '{}'.format(Constants.helptext_harm[13]),
                    'q7_helptext': '{}'.format(Constants.helptext_harm[14]),
                    'q8_helptext': '{}'.format(Constants.helptext_harm[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_harm[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_harm[13]),
                }
            if self.player.treatment == 'Responsibility':
                return {
                    'q1_label': '{}'.format(Constants.question_resp[8]),
                    'q2_label': '{}'.format(Constants.question_resp[9]),
                    'q3_label': '{}'.format(Constants.question_resp[10]),
                    'q4_label': '{}'.format(Constants.question_resp[11]),
                    'q5_label': '{}'.format(Constants.question_resp[12]),
                    'q6_label': '{}'.format(Constants.question_resp[13]),
                    'q7_label': '{}'.format(Constants.question_resp[14]),
                    'q8_label': '{}'.format(Constants.question_resp[15]),
                    'q1_helptext': '{}'.format(Constants.helptext_resp[8]),
                    'q2_helptext': '{}'.format(Constants.helptext_resp[9]),
                    'q3_helptext': '{}'.format(Constants.helptext_resp[10]),
                    'q4_helptext': '{}'.format(Constants.helptext_resp[11]),
                    'q5_helptext': '{}'.format(Constants.helptext_resp[12]),
                    'q6_helptext': '{}'.format(Constants.helptext_resp[13]),
                    'q7_helptext': '{}'.format(Constants.helptext_resp[14]),
                    'q8_helptext': '{}'.format(Constants.helptext_resp[15]),
                    'q3_scenario': '{}'.format(Constants.scenario_resp[10]),
                    'q4_scenario': '{}'.format(Constants.scenario_resp[13]),
                }

    def before_next_page(self):
        self.player.time_on_second_control_question_screen = time() - self.player.time_on_second_control_question_screen


class GameStartWaitForAll(WaitPage):   # Wait for all players before a new part is started to be played
    wait_for_all_groups = True
    body_text = "Waiting for the other participants."

    def is_displayed(self):
        return self.round_number == (Constants.num_rounds_BDM + 1) \
               or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)


class BeliefsBuyers(Page):
    form_model = 'group'

    def get_form_fields(self):
        if self.player.id_in_group == 1:
            if self.round_number < (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
                return ['buy_belief']
            else:
                return ['buy_belief', 'compensation_belief']
        elif self.player.id_in_group == 2: # for buyer 2 get buyer 2 fields
            if self.round_number < (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
                return ['buy_belief_buyer2']
            else:
                return ['buy_belief_buyer2', 'compensation_belief_buyer2']

    def is_displayed(self):   # display this page only to buyers in any round after the BDM rounds
        return self.round_number > Constants.num_rounds_BDM and self.player.id_in_group < 3 # get only buyers

    def vars_for_template(self):
        harmed = self.group.get_player_by_role('Person B')
        harmed_sliders = harmed.num_sliders_ex_ante
        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)
        max_compensation = math.ceil(Constants.maxsliders / Constants.SlidersPerPoint)

        if self.round_number < first_round_part3:       # calculate the current round of the respective part to display it accordingly
            displayed_round_number = self.round_number - Constants.num_rounds_BDM
        else:
            displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1

        return {'harmed_sliders': harmed_sliders,
                'first_round_part3': first_round_part3,
                'displayed_round_number': displayed_round_number,
                'max_compensation': max_compensation}

    def js_vars(self):
        max_compensation = math.ceil(Constants.maxsliders / Constants.SlidersPerPoint)
        role = self.player.role()
        return dict(
            first_round_part3=(Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1),
            round_number=self.round_number,
            role=role,
            max_compensation = max_compensation,
        )


class BuyingDecision(Page):

    form_model = 'group'
    form_fields = ['buy_decision', 'information_taken']

    def is_displayed(self):   # display this page only to buyers in any round after the BDM rounds
        return self.round_number > Constants.num_rounds_BDM and self.player.id_in_group == 1

    def vars_for_template(self):
        harmed = self.group.get_player_by_role('Person B')
        harmed_sliders = harmed.num_sliders_ex_ante
        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

        if self.round_number < first_round_part3:       # calculate the current round of the respective part to display it accordingly
            displayed_round_number = self.round_number - Constants.num_rounds_BDM
        else:
            displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1

        return {'harmed_sliders': harmed_sliders,
                'first_round_part3': first_round_part3,
                'displayed_round_number': displayed_round_number}


class BuyingDecisionBuyer2(Page):

    form_model = 'group'
    form_fields = ['buy_decision_buyer2']

    def is_displayed(self):   # display this page only to the second buyer in the responsibility treatment in any round after the BDM rounds
        return self.round_number > Constants.num_rounds_BDM and self.player.treatment == 'Responsibility' and self.player.id_in_group == 2

    def vars_for_template(self):
        harmed = self.group.get_player_by_role('Person B')
        harmed_sliders = harmed.num_sliders_ex_ante
        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

        if self.round_number < first_round_part3:       # calculate the current round of the respective part to display it accordingly
            displayed_round_number = self.round_number - Constants.num_rounds_BDM
        else:
            displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1

        return {'harmed_sliders': harmed_sliders,
                'first_round_part3': first_round_part3,
                'displayed_round_number': displayed_round_number}


class BuyingBelief(Page):
    form_model = 'group'
    form_fields = ['buy_belief_harmed']

    def is_displayed(self):       # display this page only to the harmed person in any round after the BDM rounds
        return self.round_number > Constants.num_rounds_BDM \
               and self.player.treatment == 'Responsibility' and self.player.id_in_group == 3 \
               or (self.round_number > Constants.num_rounds_BDM and self.player.role() == 'Person B')

    def vars_for_template(self):
        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

        if self.round_number < first_round_part3:  # calculate the current round of the respective part to display it accordingly
            displayed_round_number = self.round_number - Constants.num_rounds_BDM
        else:
            displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1

        return {'first_round_part3': first_round_part3,
                'displayed_round_number': displayed_round_number}


class BuyingBeliefHarmed2(Page):
    form_model = 'group'
    form_fields = ['buy_belief_harmed2']

    def is_displayed(self):     # display this page only to the second harmed person in the Harm treatment in any round after the BDM rounds
        return self.round_number > Constants.num_rounds_BDM and self.player.role() == 'Person B2'

    def vars_for_template(self):
        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

        if self.round_number < first_round_part3:   # calculate the current round of the respective part to display it accordingly
            displayed_round_number = self.round_number - Constants.num_rounds_BDM
        else:
            displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1

        return {'first_round_part3': first_round_part3,
                'displayed_round_number': displayed_round_number}


class CompensationDecision(Page):

    form_model = 'group'
    form_fields = ['compensation_decision']

    def is_displayed(self):      # display this page only to the buyer in any round after part 2, when the person bought the good
        return self.player.role() == 'Person A' and self.round_number > (Constants.num_rounds_BDM + Constants.num_rounds_part1) \
               and self.group.buy_decision

    def vars_for_template(self):
        max_compensation = math.ceil(Constants.maxsliders / Constants.SlidersPerPoint)
        if self.player.treatment == 'Harm':
            sliders_per_point_harm = math.ceil(Constants.SlidersPerPoint / Constants.num_harmed)
        else:
            sliders_per_point_harm = None

        displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1   # calculate the current round of the respective part to display it accordingly

        return {'max_compensation': max_compensation,
                'sliders_per_point_harm': sliders_per_point_harm,
                'displayed_round_number': displayed_round_number
                }


class CompensationDecisionBuyer2(Page):
    form_model = 'group'
    form_fields = ['compensation_decision_buyer2']

    def is_displayed(self):          # display this page only to the second buyer in the responsibility treatment in any round after part 2, when the person bought the good
        return self.player.role() == 'Person A2' and self.round_number > (Constants.num_rounds_BDM + Constants.num_rounds_part1) \
               and self.group.buy_decision_buyer2

    def vars_for_template(self):
        max_compensation = math.ceil(Constants.maxsliders / Constants.SlidersPerPoint)
        displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1  # calculate the current round of the respective part to display it accordingly

        return {'max_compensation': max_compensation,
                'displayed_round_number': displayed_round_number}


class CompensationBelief(Page):
    form_model = 'group'
    form_fields = ['compensation_belief_harmed']

    def is_displayed(self):     # display this page only to the harmed person in the Harm treatment in any round after part 2, when the person believed the good was bought
        return self.player.role() == 'Person B' and self.round_number > (Constants.num_rounds_BDM + Constants.num_rounds_part1) \
               and self.group.buy_belief_harmed

    def vars_for_template(self):
        max_compensation = math.ceil(Constants.maxsliders / Constants.SlidersPerPoint)

        if self.player.treatment == 'Harm':
            sliders_per_point_harm = math.ceil(Constants.SlidersPerPoint / Constants.num_harmed)
        else:
            sliders_per_point_harm = None
        displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1 # calculate the current round of the respective part to display it accordingly

        return {'max_compensation': max_compensation,
                'sliders_per_point_harm': sliders_per_point_harm,
                'displayed_round_number': displayed_round_number}


class CompensationBeliefHarmed2(Page):
    form_model = 'group'
    form_fields = ['compensation_belief_harmed2']

    def is_displayed(self):  # display this page only to the second harmed person in the Harm treatment in any round after part 2, when the person believed the good was bought
        return self.player.role() == 'Person B2' and self.round_number > (Constants.num_rounds_BDM + Constants.num_rounds_part1) \
               and self.group.buy_belief_harmed2

    def vars_for_template(self):
        max_compensation = math.ceil(Constants.maxsliders / Constants.SlidersPerPoint)

        if self.player.treatment == 'Harm':
            sliders_per_point_harm = math.ceil(Constants.SlidersPerPoint / Constants.num_harmed)
        else:
            sliders_per_point_harm = None
        displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1  # calculate the current round of the respective part to display it accordingly

        return {'max_compensation': max_compensation,
                'sliders_per_point_harm': sliders_per_point_harm,
                'displayed_round_number': displayed_round_number}


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participants."

    def after_all_players_arrive(self):   # calculate payoffs for everyone in a group before the results are displayed
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):      # display this page in any round after the BDM rounds
        return self.round_number > Constants.num_rounds_BDM

    def vars_for_template(self):
        if self.round_number > Constants.num_rounds_BDM + Constants.num_rounds_part1: # Calculate total amount spent on compensation for the different scenarios
            if self.group.buy_decision and self.group.buy_decision_buyer2:   # if both buyers bought
                total_compensation = self.group.compensation_decision + self.group.compensation_decision_buyer2
            elif self.group.buy_decision and not self.group.buy_decision_buyer2:   # if only buyer 1 bought
                total_compensation = self.group.compensation_decision
            elif not self.group.buy_decision and self.group.buy_decision_buyer2:   # if only buyer 2 bought
                total_compensation = self.group.compensation_decision_buyer2
            elif not self.group.buy_decision and not self.group.buy_decision_buyer2:   # if no one bought
                total_compensation = 0
        else:
            total_compensation = None

        if self.player.treatment == 'Harm':
            sliders_per_point_harm = math.ceil(Constants.SlidersPerPoint/ Constants.num_harmed)
        else:
            sliders_per_point_harm = None

        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)
        if self.round_number < first_round_part3:        # calculate the current round of the respective part to display it accordingly
            displayed_round_number = self.round_number - Constants.num_rounds_BDM
        else:
            displayed_round_number = self.round_number - Constants.num_rounds_BDM - Constants.num_rounds_part1

        return {'first_round_part3': first_round_part3,
                'total_compensation': total_compensation,
                'sliders_per_point_harm': sliders_per_point_harm,
                'displayed_round_number': displayed_round_number}


class Questionnaire(Page):

    form_model = 'player'
    form_fields = ['gender', 'age',  # 'economics_student',
                   'risk_preference', 'altruism', 'responsible_consumption',
                   'responsible_purchase', 'offsetting_behavior', 'donation_behavior']  # , 'political_orientation']

    def is_displayed(self):         # display this page only in the final round
        return self.round_number == Constants.num_rounds


class MarketFairness(Page):

    form_model = 'player'
    form_fields = ['market_fairness_1', 'market_fairness_2', 'market_fairness_3', 'market_fairness_4', 'market_fairness_5', 'market_fairness_6']

    def is_displayed(self):         # display this page only in the final round
        return self.round_number == Constants.num_rounds

    def before_next_page(self):   # reset the field value to None, in order not to display any value that might have been recorded in the same round
        self.player.password = None


class BeforePaymentWait(Page):   # page to wait for instructions about the payment procedures. Password that is needed to continue is verbally announced
    form_model = 'player'
    form_fields = ['password']

    def password_error_message(self, value):   # error message if the password for the respective round is not correct
        if self.round_number == Constants.num_rounds:
            if value != Constants.password5:
                return 'Please enter the correct password'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class PaymentInfo(Page):            # Final payment info page which shows the selected round and also the behavior in that round

    def is_displayed(self):         # display this page only in the final round
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):    # get all variables that were stored in the participant variables in the payment round
        paying_round = self.session.vars['paying_round']
        first_round_part3 = (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1)

        if paying_round <= Constants.num_rounds_BDM:        # calculate the payment round of the respective part to display it accordingly
            displayed_paying_round = paying_round
        elif paying_round < first_round_part3:
            displayed_paying_round = paying_round - Constants.num_rounds_BDM
        else:
            displayed_paying_round = paying_round - Constants.num_rounds_BDM - Constants.num_rounds_part1

        if self.player.treatment == 'Responsibility':
            buying_decision_buyer2 = self.player.participant.vars['buying_decision_buyer2']
            compensation_buyer2 = self.player.participant.vars['compensation_decision_buyer2']
            total_compensation = self.player.participant.vars['total_compensation']
        else:
            buying_decision_buyer2 = None
            compensation_buyer2 = None
            total_compensation = None

        return {'paying_round': paying_round,
                'displayed_paying_round': displayed_paying_round,
                'first_round_part3': first_round_part3,
                'sliders_WTP': self.player.participant.vars['sliders_WTP'],
                'BDM_sliders': self.player.participant.vars['BDM_final_sliders'],
                'BDM_price': self.player.participant.vars['BDM_final_price'],
                'buying_decision': self.player.participant.vars['buying_decision'],
                'buying_decision_buyer2': buying_decision_buyer2,
                'buying_price': self.player.participant.vars['buying_price'],
                'compensation': self.player.participant.vars['compensation'],
                'compensation_buyer2': compensation_buyer2,
                'total_compensation': total_compensation,
                'final_sliders': self.player.participant.vars['final_sliders'],
                'final_payoff': self.player.participant.vars['final_payoff'],
                'exchange_rate': self.session.config['real_world_currency_per_point'],
                'rounded_euro_payoff': self.player.participant.vars['rounded_final_euro_payoff'],
                'mode': self.session.config['mode']
                }

    def before_next_page(self):     # prepare sliders in the last round for all players who have to solve any sliders
        if self.round_number == Constants.num_rounds and self.player.participant.vars['final_sliders'] > 0:
            self.player.prepare_sliders(num=self.player.participant.vars['final_sliders'], min=0, max=100)
            self.player.slider_solving_time = time()


class Sliders(SliderTaskPage):

    def is_displayed(self):      # display slider page in the last round for all players who have to solve any sliders
        return self.round_number == Constants.num_rounds and self.player.participant.vars['final_sliders'] > 0

    Constants = Constants
    Slider = Slider


class FinalScreen(Page):        # final screen in last round for all players which asks them to wait for their number to be called

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'mode': self.session.config['mode']}


    """""
    ControlQuestions,
    ControlQuestionsCorrected,
    
    Questionnaire,
    MarketFairness,
    """""


page_sequence = [
    Welcome,
    IntroductionWaitForAll,
    IntroParts,
    SlidersTrial,
    CalcPricesWaitPage,
    IntroBDM,
    BeforeBDMWait,
    SlidersBDM,
    ControlQuestions,
    ControlQuestionsCorrected,
    GameStartWaitForAll,
    BeliefsBuyers,
    BuyingDecision,
    BuyingDecisionBuyer2,
    BuyingBelief,
    BuyingBeliefHarmed2,
    CompensationDecision,
    CompensationDecisionBuyer2,
    CompensationBelief,
    CompensationBeliefHarmed2,
    ResultsWaitPage,
    Results,
    Questionnaire,
    MarketFairness,
    BeforePaymentWait,
    PaymentInfo,
    Sliders,
    FinalScreen,
 ]

""""page_sequence = [
    Welcome,
    IntroductionWaitForAll,
    IntroParts,
    SlidersTrial,
    CalcPricesWaitPage,
    IntroBDM,
    BeforeBDMWait,
    SlidersBDM,
    ControlQuestions,
    ControlQuestionsCorrected,
    GameStartWaitForAll,
    BeliefsBuyers,
    BuyingDecision,
    BuyingDecisionBuyer2,
    BuyingBelief,
    BuyingBeliefHarmed2,
    CompensationDecision,
    CompensationDecisionBuyer2,
    CompensationBelief,
    CompensationBeliefHarmed2,
    ResultsWaitPage,
    Results,
    Questionnaire,
    MarketFairness,
    BeforePaymentWait,
    PaymentInfo,
    Sliders,
    FinalScreen
]
"""