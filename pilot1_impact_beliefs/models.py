from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
import csv
from otree.db.models import ForeignKey
from slider_task.models import BaseSlider, SliderPlayer

author = 'Frauke Stehr'

doc = """
Experiment on motivated beliefs of impact of other-regarding behavior"""


class Constants(BaseConstants):
    name_in_url = 'experiment'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('impact_beliefs/static/Parameters.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    num_work_rounds = 1
    num_decision_rounds = len(paras) * 4
    num_rounds = num_decision_rounds + num_work_rounds
    endowment = 300
    beliefs_fixed_payment = 150
    beliefs_max_accuracy_bonus = beliefs_fixed_payment
    beliefs_max_payment = beliefs_fixed_payment + beliefs_max_accuracy_bonus

    # slider_columns = 3  # uncomment this if you want sliders in the slider task to be displayed in multiple columns
    num_sliders = 60

    sec_intro = 10
    sec_per_matrix = 10
    sec_to_answer = 15

    real_world_kg_co2_per_x = 0.5
    car_kg_co2_per_mile = 0.275  # source: carbonindependent.org with avg mpg=52

    min_price = 12.75
    max_price = 157.25


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                paras = Constants.paras.copy()
                p.vars['trial_timeout_counter'] = 0  # initialize trial timeout counter
                p.vars['timeout_counter'] = 0  # initialize timeout counter
                p.vars['timeout_in_payment_round'] = 0  # initialize timeout counter
                p.vars['forced_timeout'] = 0
                p.vars['attention_check_failed'] = 0

                # generate participant varlist for beliefs by part, to store beliefs using project_id
                p.vars['beliefs_part1'] = [0] * len(paras)
                p.vars['beliefs_part3'] = [0] * len(paras)

                # randomize the order of projects on participant level, but within part and store as participant varlist
                random.shuffle(paras)
                new_paras = Constants.paras.copy()  # defines a helplist of parameters, which is shuffled then appended to original paras list
                for i in [0, 1, 2]:  # repeat three times to get four parts (original + 3 times shuffled)
                    random.shuffle(new_paras)  # shuffles helplist
                    paras = paras + new_paras  # appends shuffled helplist to list of parameters
                p.vars['parameters'] = paras  # store shuffled list of parameters in participant vars, then access each element by round number
                # print(p.vars['parameters'])  # prints participant vars to double check randomization

                # randomly assign treatment order to participants
                orders = ["NeutralMotivated", "MotivatedInfo"]
                p.vars['order'] = random.choice(orders)

                # randomly assign payment round
                rounds = range(1, Constants.num_rounds + 1)
                p.vars['payment_round'] = random.choice(rounds)
                print("Payment round is", p.vars['payment_round'])

            for p in self.get_players():
                p.prepare_sliders(num=Constants.num_sliders, min=0, max=100)

        for p in self.get_players():
            # Define "part" variable in the beginning of the experiment
            if self.round_number == 1:
                p.part = 0
                p.round_type = "effort"
            elif self.round_number <= len(Constants.paras) + 1:
                p.part = 1  # belief rounds 1
                p.round_type = "belief"
            elif self.round_number <= len(Constants.paras) * 2 + 1:
                p.part = 2  # donation rounds 1
                p.round_type = "donation"
            elif self.round_number <= len(Constants.paras) * 3 + 1:
                p.part = 3  # belief rounds 2
                p.round_type = "belief"
            else:
                p.part = 4  # donation rounds 2
                p.round_type = "donation"

            # Assign treatment to players in all rounds using treatment order assigned in first round
            if p.participant.vars['order'] == "NeutralMotivated":
                p.order = "NeutralMotivated"
                if p.part == 0:
                    p.treatment = ""
                elif p.part == 1 or p.part == 2:
                    p.treatment = "Neutral"
                else:
                    p.treatment = "Motivated"
            elif p.participant.vars['order'] == "MotivatedInfo":
                p.order = "MotivatedInfo"
                if p.part == 0:
                    p.treatment = ""
                elif p.part == 1 or p.part == 2:
                    p.treatment = "Motivated"
                else:
                    p.treatment = "Info"

    def vars_for_admin_report(self):
        participants = [p for p in self.session.get_participants()]
        for p in self.session.get_participants():
            final_payoff = p.payoff
            final_payoff_plus_part_fee = p.payoff_plus_participation_fee()
        return {
            'participants': participants,
            'final_payoff': final_payoff,
            'final_payoff_plus_part_fee': final_payoff_plus_part_fee,
        }


class Group(BaseGroup):
    pass


class Player(SliderPlayer):
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")

    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")

    part = models.IntegerField()
    round_type = models.StringField()
    order = models.StringField()
    treatment = models.StringField()


    gif_clicked = models.BooleanField(blank=True, doc="automatically filled if people click on gif")
    gif_watched = models.BooleanField(blank=True, doc="check box field where people confirm they clicked on the gif")
    clicked_early = models.BooleanField(blank=True, doc="True if person tried to continue from instructions < 60 sec")
    equation_clicked = models.BooleanField(blank=True,
                                           doc="automatically filled if people click on equation for quadratic scoring rule")

    trial_belief_1 = models.IntegerField(blank=True, min=0, max=400)
    trial_belief_2 = models.IntegerField(blank=True, min=0, max=400)
    # https://www-jstor-org.ezproxy.ub.unimaas.nl/stable/24363518?seq=1#metadata_info_tab_contents
    attention_check = models.IntegerField(blank=True, min=0, max=400, doc="Asks to fill in 54 as random number as attention check.")
    attention_check_failed = models.BooleanField(blank=True, doc="True if subject failed to put in 23 as random answer")

    trial_timeout = models.IntegerField(initial=0, blank=True,
                                        doc="Counts how many time-outs occured on trial belief page")

    num_x_belief = models.IntegerField(min=0, max=400, doc="records belief on number of Xs in matrix")
    timeout = models.BooleanField(blank=True, doc="True if a time-out occured on a belief-elicitation page")
    forced_timeout = models.BooleanField(blank=True,
                                         doc="True if subject was forced to quit because of too many time-outs")
    donation = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                   choices=[
                                       [True, 'Yes'],
                                       [False, 'No'],
                                   ]
                                   )
    project_id = models.IntegerField()
    num_x_true = models.IntegerField()
    price = models.FloatField()

    current_payoff = models.FloatField()

    co2_belief_car = models.FloatField(label="Consider a household that drives on average 8,000 miles a year. How much emissions could be saved in a year if this household were to live car-free? Assume in your answer that they would walk or take the bike instead.",)
    co2_belief_plane = models.FloatField(label="Consider a transatlantic round-trip flight from London to New York. How much emissions could be saved by avoiding this flight?",)
    co2_belief_renewables = models.FloatField(label="Consider a household which uses 4,800 kWh of energy a year. How much emissions could be saved in a year if this household would switch to renewable energy?",)
    co2_belief_vegan = models.FloatField(label="Consider a household that consumes around 1.2 kg of meat and 2.2 kg of dairy a week. How much emissions could be saved in a year if they were to adopt a plant-based diet?",)
    co2_belief_laundry = models.FloatField(label="Consider a household which washes around 165 loads per year. How much emissions would be saved in a year if they were to change washer temperature settings from “hot wash, warm rinse” to “warm wash, cold rinse” for all laundry?",)
    co2_belief_dryer = models.FloatField(label="Consider a household which washes around 165 loads per year. How much emissions would be saved in a year if they were to air-dry all laundry instead of using an electric dryer?",)

    cost_belief_car = models.FloatField(label="Live car-free",)
    cost_belief_plane = models.FloatField(label="Avoid one transatlantic round-trip flight",)
    cost_belief_renewables = models.FloatField(label="Use renewable energy at home",)
    cost_belief_vegan = models.FloatField(label="Adopt a plant-based diet",)
    cost_belief_laundry = models.FloatField(label="Wash clothes in cold water",)
    cost_belief_dryer = models.FloatField(label="Air-dry clothes",)

    # Comprehension Question Fields
    wrong_answer1 = models.IntegerField(doc="Counts the number of wrong guesses for cq1.", initial=0)
    wrong_answer2 = models.IntegerField(doc="Counts the number of wrong guesses for cq2.", initial=0)
    wrong_answer3 = models.IntegerField(doc="Counts the number of wrong guesses for cq3.", initial=0)
    wrong_answer4 = models.IntegerField(doc="Counts the number of wrong guesses for cq4.", initial=0)

    cq1 = models.BooleanField(doc="Comprehension Question 1", choices=[
        [True, 'True'],
        [False, 'False'],
    ])

    def cq1_error_message(self, value):
        if self.round_number < len(Constants.paras) + 2 and not value:
            self.wrong_answer1 += 1
            return "Wrong answer."
        elif self.round_number == len(Constants.paras) + 2 and value:
            self.wrong_answer1 += 1
            return "Wrong answer."

    cq2 = models.IntegerField(doc="Comprehension Question 2", min=0, max=400)

    def cq2_error_message(self, value):
        if self.round_number == 1 and value != 50:
            self.wrong_answer2 += 1
            return "Wrong answer."
        elif self.round_number == 2 and value != Constants.beliefs_fixed_payment:
            self.wrong_answer2 += 1
            return "Wrong answer."
        elif self.round_number == len(Constants.paras) + 2 and value != Constants.endowment:
            self.wrong_answer2 += 1
            return "Wrong answer."

    cq3 = models.BooleanField(doc="Comprehension Question 3", choices=[
        [True, 'True'],
        [False, 'False'],
    ])

    def cq3_error_message(self, value):
        if value != True:
            self.wrong_answer3 += 1
            return "Wrong answer."

    cq4 = models.IntegerField(doc="Comprehension Question 4", widget=widgets.RadioSelect)

    def cq4_choices(player):
        if player.round_number == 1:  # Your final earnings are determined as follows
            choices = [
                [1, "The sum of the participation fee and the earnings in all five tasks"],
                [2, "Either the participation fee or the earnings in all five tasks"],
                [3, "The sum of the participation fee and the earnings in one decision of the five tasks"],
                # Correct Answer
                [4, "Either the participation fee or the earnings in one decision of the five tasks"],
            ]
        elif player.round_number == 2:  # How many Xs can there be in a given matrix?
            choices = [
                [1, "at least 50 Xs"],
                [2, "Between 0 and 400 Xs"],  # Correct Answer
                [3, "at most 260 Xs"],
                [4, "This cannot be known"],
            ]
        elif player.round_number == len(
                Constants.paras) + 2:  # Which of the following statements about the consequences of your decision is correct?
            choices = [
                [1, "When I decide not to donate, 50 Points are subtracted from my earnings and donated."],
                [2,
                 "When I decide to donate, 50 Points are subtracted from my earnings and donated to climatecare.org."],
                [3, "When I decide not to donate, I earn nothing in this task."],
                [4,
                 "When I decide to donate, the price of the project is subtracted from my earnings and donated to climatecare.org."],
                # Correct Answer
            ]
        else:
            choices = []
        return choices

    def cq4_error_message(self, value):
        if self.round_number == 1 and value != 3:
            self.wrong_answer4 += 1
            return "Wrong answer."
        elif self.round_number == 2 and value != 2:
            self.wrong_answer4 += 1
            return "Wrong answer."
        elif self.round_number == len(Constants.paras) + 2 and value != 4:
            self.wrong_answer4 += 1
            return "Wrong answer."

    age = models.IntegerField(label="What is your age?",
                              choices=[
                                  [1, "17 or younger"],
                                  [2, "18 - 19"],
                                  [3, "20 - 29"],
                                  [4, "30 - 39"],
                                  [5, "40 - 49"],
                                  [6, "50 - 59"],
                                  [7, "60 or older"],

                              ])

    gender = models.IntegerField(
        label="What is your gender?",
        choices=[
            [1, "Female"],
            [2, "Male"],
            [3, "Non-binary"],
            [4, "Prefer Not to Specify"],
        ],
        widget=widgets.RadioSelectHorizontal,
    )

    levelOfEducation = models.IntegerField(
        label="What is the highest degree or level of education you have completed?",
        choices=[
            [0, 'Less than High School diploma'],
            [1, 'High School or equivalent'],
            [2, 'Bachelor degree (e.g. BA, BSc)'],
            [3, 'Master degree (e.g. MA, MSc, MEd)'],
            [4, 'Doctorate (e.g. PhD, EdD, DBA)'],
            [5, 'other'],
        ],
    )

    income = models.IntegerField(
        label="What is your household income per year? In your answer, please consider only people with whom you share finances as part of your household. "
              "This would, for example, most likely exclude other members from your student dorm.",
        choices=[
            [0, 'Less than £10,000'],
            [1, '£10,000 - £19,999'],
            [2, '£20,000 - £29,999'],
            [3, '£30,000 - £39,999'],
            [4, '£40,000 - £49,999'],
            [5, '£50,000 - £59,999'],
            [6, '£60,000 - £69,999'],
            [7, '£70,000 - £79,999'],
            [8, '£80,000 - £89,999'],
            [9, '£90,000 - £99,999'],
            [10, '£100,000 - £149,999'],
            [11, '£150,000 or more'],
        ],
    )

    # https://medium.com/pew-research-center-decoded/small-changes-in-survey-scales-can-matter-when-measuring-political-ideology-in-europe-4a10d9a015c5
    politics_right = models.IntegerField(
        label= "In political matters people talk of 'the left' and 'the right'. Please pick the category that you identify most with.",
        choices=[[1, "left"],
                 [2, "leaning left"],
                 [3, "centre"],
                 [4, "leaning right"],
                 [5, "right"]
                 ],
        widget=widgets.RadioSelectHorizontal,
    )

    altruism = models.IntegerField(
        choices=range(0, 11),
        widget=widgets.RadioSelectHorizontal,
        label='How do you assess your willingness to share with others without expecting anything in '
              'return when it comes to charity? Please use a scale from 0 to 10, where 0 means you '
              'are “completely unwilling to share” and a 10 means you are “very willing to share”. '
              'You can also use the values in between to indicate where you fall on the scale.')

    env_attitude = models.IntegerField(
        label="Here are two statements people sometimes make when discussing the environment"
              " and economic growth. Please use the slider to indicate which of them comes closer to your own point of view?",
        doc=" environmental attitudes Q111 from 2017 wave of world value survey. " \
            "0= Economic growth and creating jobs should be the top priority, even if the"
            "environment suffers to some extent. 10= Protecting the environment should"
            "be given priority, even if it causes slower economic growth and some"
            "loss of jobs.")

    honeypot = models.IntegerField(blank=True,
                                   doc="hidden field which will only be filled by bots")


class Slider(BaseSlider):  # Class that is needed for the slider task
    player = ForeignKey(Player,
                        on_delete=models.CASCADE,
                        )
