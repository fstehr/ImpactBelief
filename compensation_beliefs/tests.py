from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random, math

class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == 1 or self.round_number == (Constants.num_rounds_BDM + 1) \
                   or self.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            yield (pages.Welcome)

        if self.subsession.round_number == 1:
            yield (pages.IntroParts, {'password': 2971})
        elif self.subsession.round_number == (Constants.num_rounds_BDM + 1):
            yield (pages.IntroParts, {'password': 6076})
        elif self.subsession.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            yield (pages.IntroParts, {'password': 4577})

        if self.subsession.round_number == 1:
            yield (pages.SlidersTrial)
            yield (pages.IntroBDM)
            yield (pages.BeforeBDMWait, {'password': 1942})

        if self.subsession.round_number <= Constants.num_rounds_BDM:
            yield (pages.SlidersBDM, {'sliders_WTP': 20})

        if self.subsession.round_number == (Constants.num_rounds_BDM + 1):
            if self.player.treatment == 'Individual':
                yield (pages.ControlQuestions, {'q1_answer_1': 1, 'q2_answer_1': 0, 'q3_answer_1': 146, 'q4_answer_1': 75,
                                                'q5_answer_1': 240, 'q6_answer_1': 75, 'q7_answer_1': 75, 'q8_answer_1': 0})
            elif self.player.treatment == 'Risk':
                yield (pages.ControlQuestions, {'q1_answer_1': 1, 'q2_answer_1': 0, 'q3_answer_1': 146, 'q4_answer_1': 75,
                                                'q5_answer_1': 1234, 'q6_answer_1': 75, 'q7_answer_1': 75, 'q8_answer_1': 0})
            elif self.player.treatment == 'Harm':
                yield (pages.ControlQuestions, {'q1_answer_1': 2, 'q2_answer_1': 0, 'q3_answer_1': 146, 'q4_answer_1': 75,
                                                'q5_answer_1': 120, 'q6_answer_1': 75, 'q7_answer_1': 75, 'q8_answer_1': 0})
            elif self.player.treatment == 'Responsibility':
                yield (pages.ControlQuestions, {'q1_answer_1': 1, 'q2_answer_1': 0, 'q3_answer_1': 146, 'q4_answer_1': 75,
                                                'q5_answer_1': 240, 'q6_answer_1': 75, 'q7_answer_1': 75, 'q8_answer_1': 0})

        elif self.subsession.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            if self.player.treatment == 'Individual':
                yield (pages.ControlQuestions, {'q1_answer_1': 0, 'q2_answer_1': 0, 'q3_answer_1': 120, 'q4_answer_1': 75,
                                                'q5_answer_1': 80, 'q6_answer_1': 129, 'q7_answer_1': 75, 'q8_answer_1': 0})
            elif self.player.treatment == 'Risk':
                yield (pages.ControlQuestions, {'q1_answer_1': 0, 'q2_answer_1': 0, 'q3_answer_1': 120, 'q4_answer_1': 75,
                                                'q5_answer_1': 80, 'q6_answer_1': 129, 'q7_answer_1': 75, 'q8_answer_1': 0})
            elif self.player.treatment == 'Harm':
                yield (pages.ControlQuestions, {'q1_answer_1': 0, 'q2_answer_1': 0, 'q3_answer_1': 120, 'q4_answer_1': 75,
                                                'q5_answer_1': 40, 'q6_answer_1': 129, 'q7_answer_1': 75, 'q8_answer_1': 0})
            elif self.player.treatment == 'Responsibility':
                yield (pages.ControlQuestions, {'q1_answer_1': 0, 'q2_answer_1': 240, 'q3_answer_1': 120, 'q4_answer_1': 75,
                                                'q5_answer_1': 80, 'q6_answer_1': 129, 'q7_answer_1': 75, 'q8_answer_1': 0})

        if self.subsession.round_number == (Constants.num_rounds_BDM + 1):
            yield (pages.ControlQuestionsCorrected)
        elif self.subsession.round_number == (Constants.num_rounds_BDM + Constants.num_rounds_part1 + 1):
            yield (pages.ControlQuestionsCorrected)

        if self.subsession.round_number > Constants.num_rounds_BDM:
            if self.player.role() == "Person A":
                if self.player.treatment == "Individual":
                    choice_set = [True, False]
                else:
                    choice_set = [True, True, False]
                buy = random.choice(choice_set)
                yield (pages.BuyingDecision, {'buy_decision': buy})

            if self.player.role() == "Person A2":
                choice_set = [True, True, False]
                buy = random.choice(choice_set)
                yield (pages.BuyingDecisionBuyer2, {'buy_decision_buyer2': buy})

            if self.player.role() == "Person B":
                yield (pages.BuyingBelief, {'buy_belief': True})

            if self.player.role() == "Person B2":
                yield (pages.BuyingBeliefHarmed2, {'buy_belief_harmed2': True})

        if self.subsession.round_number > Constants.num_rounds_BDM_part_1:
            if self.player.role() == "Person A" and self.group.buy_decision:
                max_compensation = math.ceil(Constants.maxsliders/Constants.SlidersPerPoint)
                choice_set_comp = list(range(0, max_compensation))
                compensation = random.choice(choice_set_comp)
                yield (pages.CompensationDecision, {'compensation_decision': compensation})

            if self.player.role() == "Person A2" and self.group.buy_decision_buyer2:
                max_compensation = math.ceil(Constants.maxsliders/Constants.SlidersPerPoint)
                choice_set_comp = list(range(0, max_compensation))
                compensation = random.choice(choice_set_comp)
                yield (pages.CompensationDecisionBuyer2, {'compensation_decision_buyer2': compensation})

            if self.player.role() == "Person B":
                yield (pages.CompensationBelief, {'compensation_belief': 0})

            if self.player.role() == "Person B2":
                yield (pages.CompensationBeliefHarmed2, {'compensation_belief_harmed2': 0})

        if self.subsession.round_number > Constants.num_rounds_BDM:
            yield (pages.Results)

        if self.subsession.round_number == Constants.num_rounds:
            yield (pages.Questionnaire, {'gender': 1, 'age': 19, 'economics_student': True, 'risk_preference': 10,
                                         'altruism': 1, 'responsible_consumption': 1, 'responsible_purchase': 113,
                                         'offsetting_behavior': 4, 'donation_behavior': 26, 'political_orientation': 5})

            yield (pages.MarketFairness, {'market_fairness_1': 1, 'market_fairness_2': 1, 'market_fairness_3': 3,
                                          'market_fairness_4': 10, 'market_fairness_5': 1, 'market_fairness_6': 1})

            yield (pages.BeforePaymentWait, {'password': 7903})

            yield (pages.PaymentInfo)

            if self.player.participant.vars['final_sliders'] > 0:
                yield (pages.Sliders)



