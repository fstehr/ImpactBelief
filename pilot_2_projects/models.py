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

doc = """
This is an experiment on impact beliefs of donations, with 2 projects per screen. 
All currency variables are in US Dollars.
Design is 2x2 (player.accuracy_bonus (within subj) x player.treatment (btw subj.))
"""


class Constants(BaseConstants):
    name_in_url = 'study2'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('pilot_2_projects/static/Parameters.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    # structure of experiment
    num_parts = 3
    num_wtp_items = 3
    num_rounds = len(paras) * (num_parts - 1) + num_wtp_items

    # timing parameters for display
    duration_min = 25
    sec_intro = 3
    sec_per_matrix = 7
    sec_to_answer = 20

    # incentives
    endowment = 40
    accuracy_bonus_low = 2
    accuracy_bonus_high = 20


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize parameter order on subject level
        if self.round_number == 1:
            for p in self.session.get_participants():
                paras = Constants.paras.copy()

                # store shuffled list of img number & parameters in participant vars,
                # access each element by round number in pages.py
                p.vars['parameters'] = []
                img = [*range(1, len(paras) + 1)]
                p.vars['img_a'] = []   # initialize participant vars
                p.vars['img_b'] = []

                for i in range(1, Constants.num_parts + 1):
                    a = random.sample(img, len(img))   # randomize which matrix is displayed for each project (matrix_80_i)
                    b = random.sample(img, len(img))
                    c = random.sample(paras, len(paras))
                    p.vars['img_a'] += a
                    p.vars['img_b'] += b
                    p.vars['parameters'] += c
                # print('img_a is', p.vars['img_a'])
                # print('img_b is', p.vars['img_b'])
                # print(p.vars['parameters'])  # prints participant vars to double check randomization

                # randomize on participant level whether project A is displayed on the left or right for all rounds
                is_left = [0, 1]
                rounds = range(1, Constants.num_rounds + 1)
                p.vars['cheap_project_first'] = [random.choice(is_left) for i in rounds]
                # print("cheap_project_first is", p.vars['cheap_project_first'])

                # assign one payment round
                p.vars['payment_round'] = random.choice(rounds)
                # print("Payment round is", p.vars['payment_round'])

                # randomly assign incentive order to participants between subjects
                orders = ["NeutralMotivated", "MotivatedNeutral"]
                p.vars['order'] = random.choice(orders)

                # Assign between subject treatment with pr(ExAnte) = 1/3, pr(ExPost) = 2/3
                treatments = ["ExAnte", "ExPost", "ExPost"]
                p.vars['treatment'] = random.choice(treatments)

                # initialize some participant vars:
                p.vars['too_many_wrong'] = False
                p.vars['attention_check_failed'] = False


        # store some of the participant vars in the data set
        for p in self.get_players():
            # Define "part" variable in the beginning of the experiment
            if self.round_number <= len(Constants.paras):
                p.part = 1
            elif self.round_number <= len(Constants.paras) * 2:
                p.part = 2
            elif self.round_number <= Constants.num_rounds:
                p.part = 3
                if self.round_number == Constants.num_rounds - 2:
                    p.left_side_num_doses = 8
                elif self.round_number == Constants.num_rounds - 1:
                    p.left_side_num_doses = 20
                elif self.round_number == Constants.num_rounds:
                    p.left_side_num_doses = 32

            # store treatment assignment in data set
            p.payment_round = p.participant.vars['payment_round']
            p.treatment = p.participant.vars['treatment']

            # Assign incentive strength to players in all rounds using treatment order assigned in first round
            if p.participant.vars['order'] == "NeutralMotivated":
                p.order = "NeutralMotivated"
                if p.part == 1:
                    p.accuracy_bonus = Constants.accuracy_bonus_high
                else:
                    p.accuracy_bonus = Constants.accuracy_bonus_low
            elif p.participant.vars['order'] == "MotivatedNeutral":
                p.order = "MotivatedNeutral"
                if p.part == 1:
                    p.accuracy_bonus = Constants.accuracy_bonus_low
                else:
                    p.accuracy_bonus = Constants.accuracy_bonus_high


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # background vars
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    finishing_time = models.LongStringField(doc="Time at which last page is reached")
    payment_round = models.IntegerField(doc="round that is selected for final payment")
    is_mobile = models.BooleanField(doc="Automatic check through .js whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")

    forced_timeout = models.BooleanField(doc="True if subject was excluded during experiment because of attention check fail or"
                                             "too many wrong answers in control questions (>2). ")
    wrong_answer_count = models.IntegerField(initial=0,
                                             doc="variable which counts the number of attempts for a control questions.")

    cq_1 = models.BooleanField(label="If you are randomly selected for a bonus payment, your bonus payment depends "
                                     "on your answers in the experiment",
                               choices=[[True, 'True'], [False, 'False']])

    def cq_1_error_message(self, value):
        # print('value 1 is', value)
        if not value:
            self.wrong_answer_count += 1
            return "Wrong answer."

    cq_2 = models.IntegerField(label="At most how many times are you allowed to answer wrongly to be admitted "
                                     "to the experiment?",
                               min=0, max=100)

    def cq_2_error_message(self, value):
        # print('value 2 is', value)
        if value != 2:
            self.wrong_answer_count += 1
            return "Wrong answer."

    cq_3 = models.IntegerField(label="How many vitamin A doses your donation finances depends on...",
                               widget=widgets.RadioSelect,
                               choices=[[1, 'your estimate of the number of pills in an image.'],
                                        [2, 'the true number of pills in an image.'],
                                        [3, 'whether your estimate is correct.']])

    def cq_3_error_message(self, value):
        # print('value 3 is', value)
        if value != 2:
            self.wrong_answer_count += 1
            return "Wrong answer."

    cq_4 = models.IntegerField(label="In what way does your donation decision have real consequences (if it is selected "
                                     "as a decision-that-counts)?",
                               widget=widgets.RadioSelect,
                               choices=[[1, 'The money you donate will go to a charity of your choice.'],
                                        [2, 'Your choice has no real-world consequences.'],
                                        [3, 'The money you donate will go to another participant in this study.'],
                                        [4, 'If you donate, you fund real vitamin A doses to be administered by Helen Keller International.']])

    def cq_4_error_message(self, value):
        # print('value 3 is', value)
        if value != 4:
            self.wrong_answer_count += 1
            return "Wrong answer."

    cq_5 = models.IntegerField(label="How many pills are there in a given image?",
                               widget=widgets.RadioSelect,
                               choices=[
                                   [1, "at least 10 pills"],
                                   [2, "Between 0 and 400 pills"],  # Correct Answer
                                   [3, "at most 200 pills"],
                                   [4, "This cannot be known"]])

    def cq_5_error_message(self, value):
        if value != 2:
            self.wrong_answer_count += 1
            return "Wrong answer."

    cq_6 = models.IntegerField(label="Suppose your estimate is 6 pills away from the true number of pills. What will be your "
                                     "bonus payment (in $) if this estimate is selected as decision-that-counts?")

    def cq_6_error_message(self, value):
        if value != self.accuracy_bonus:
            if self.round_number == 1:
                self.wrong_answer_count += 1
            return "Wrong answer."

    attention_check = models.StringField(blank=True, doc="Filter question for attention",
                                         label="To make sure you have read the instructions, we ask you to answer "
                                                "'apple' in the field below.")

    trial_belief_A = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of pills in matrix")
    trial_confidence_A = models.IntegerField(initial=-99, min=0, max=20)
    trial_donation_A = models.BooleanField(widget=widgets.RadioSelectHorizontal, choices=[[True, 'Yes'], [False, 'No']])
    trial_belief_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of pills in matrix")
    trial_confidence_B = models.IntegerField(initial=-99, min=0, max=20)
    trial_donation_B = models.BooleanField(widget=widgets.RadioSelectHorizontal, choices=[[True, 'Yes'], [False, 'No']])

    # treatment variables
    order = models.StringField()
    part = models.IntegerField()
    accuracy_bonus = models.IntegerField()  # options are lo and hi, as defined in Constants
    treatment = models.StringField()   # options as ExAnte and ExPost

    comparison_id = models.IntegerField()
    comparison_type = models.StringField()

    # Characteristics of Project A
    num_x_A = models.IntegerField()
    price_A = models.IntegerField()
    efficiency_A = models.FloatField()
    img_A = models.IntegerField()

    # Subject input of project A
    num_x_belief_A = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    confidence_belief_A = models.IntegerField(initial=-99, min=0, max=20,
                                              doc="cognitive uncertainty measure adapted from Enke, Graeber (2021)")
    donation_A = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[[True, 'Yes'], [False, 'No']])

    # Characteristics of Project B
    num_x_B = models.IntegerField()
    price_B = models.IntegerField()
    efficiency_B = models.FloatField()
    img_B = models.IntegerField()

    # Subject input of project B
    num_x_belief_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    confidence_belief_B = models.IntegerField(initial=-99, min=0, max=20, doc="cognitive uncertainty measure adapted from Enke, Graeber (2021)")
    donation_B = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[[True, 'Yes'], [False, 'No']]
                                     )

    # Payoff variables
    current_donation_payoff = models.IntegerField()
    current_belief_A_payoff = models.IntegerField()
    current_belief_B_payoff = models.IntegerField()
    payoff_decision = models.StringField()

    # Other behavior during elicitation
    page_loaded = models.IntegerField()   # counts how many times Donation.html was refreshed
    time_out = models.BooleanField()    # field which gets value 1 if subject did not enter belief on time.
    honeypot = models.IntegerField(blank=True,
                                   doc="hidden field which will only be filled by bots")

    # WTP for various vitamin A doses
    left_side_num_doses = models.IntegerField()
    switching_point = models.IntegerField()
    mpl_row = models.IntegerField(doc="stores the randomly selected row of an mpl")
    current_mpl_payoff = models.IntegerField()
    donation_mpl = models.BooleanField()   # true if switching point in mpl is above randomly drawn scenario

    # additional variables
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
            [0, 'Less than $10,000'],
            [1, '$10,000 - $19,999'],
            [2, '$20,000 - $29,999'],
            [3, '$30,000 - $39,999'],
            [4, '$40,000 - $49,999'],
            [5, '$50,000 - $59,999'],
            [6, '$60,000 - $69,999'],
            [7, '$70,000 - $79,999'],
            [8, '$80,000 - $89,999'],
            [9, '$90,000 - $99,999'],
            [10, '$100,000 - $149,999'],
            [11, '$150,000 or more'],
        ],
    )

    altruism = models.IntegerField(
        choices=range(0, 11),
        widget=widgets.RadioSelectHorizontal,
        label='How do you assess your willingness to share with others without expecting anything in '
              'return when it comes to charity? Please click on the slider to indicate where you fall on the scale.')

    giving_type = models.IntegerField(
        label="Think about the last time you gave to charity before today. "
              "What was most important to you when you decided to donate?",
        doc="warm glow survey item from Carpenter (2021) JEBO",
        widget=widgets.RadioSelect,
        choices=[
            [1, 'the total amount given by everyone'],
            [2, 'the amount that you personally gave'],
            [3, 'some other aspect of giving']
        ]
        )



# TO DO

# still have to donate 6 doses from pilot!!!

# - systematically test belief & donation payoffs
# - test randomization of pictures!!! using console log with the picture names!

# - calculate and update optimal payment rule (e.g. 1 in 20?)

# think about how to deal with with time-out variable --> is this still there?


# The experiment is programmed such that subjects:
# -	who more than two mistakes when answering the control questions testing their understanding of the instructions
# --> implement with app_after_this_page = payment info
# are excluded from the experiment.



