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
import itertools    # allows to balance treatments
from otree.db.models import ForeignKey

doc = """
This is a pilot snippet testing whether it makes a difference (for beliefs & donations) 
whether two projects are on one screen or not.
This is the code with <b>2 projects per screen</b>. All currency variables are in US Dollars.
Design is 2x2 (player.accuracy_bonus (within subj) x player.treatment (btw subj.))
"""


class Constants(BaseConstants):
    name_in_url = 'study2'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('pilot_2_projects/static/Parameters.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    # structure of experiment
    num_parts = 2
    num_rounds = len(paras) * num_parts

    # timing parameters for display
    duration_min = 15
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
                print('img_a is', p.vars['img_a'])
                print('img_b is', p.vars['img_b'])
                print(p.vars['parameters'])  # prints participant vars to double check randomization

                # randomize on participant level whether project A is displayed on the left or right for all rounds
                is_left = [0, 1]
                rounds = range(1, Constants.num_rounds + 1)
                p.vars['cheap_project_first'] = [random.choice(is_left) for i in rounds]
                print("cheap_project_first is", p.vars['cheap_project_first'])

                # assign one payment round
                p.vars['payment_round'] = random.choice(rounds)
                # print("Payment round is", p.vars['payment_round'])

                # randomly assign treatment order to participants
                orders = ["NeutralMotivated", "MotivatedNeutral"]
                p.vars['order'] = random.choice(orders)

            # store some of the participant vars in the data set
            for p in self.get_players():
                # Define "part" variable in the beginning of the experiment
                if self.round_number <= len(Constants.paras):
                    p.part = 1
                elif self.round_number <= Constants.num_rounds:
                    p.part = 2

                # Assign between subject treatment with pr(ExAnte) = 1/3, pr(ExPost) = 2/3
                treatments = ["ExAnte", "ExPost", "ExPost"]
                p.treatment = random.choice(treatments)

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
    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")

    cq_1 = models.BooleanField(label="If you are randomly selected for a bonus payment, your bonus payment depends "
                                     "on your answers in the experiment",
                                    choices=[[True, 'True'], [False, 'False']])
    cq_2 = models.IntegerField(label="How many vitamin A doses your donation finances depends on...",
                               widget=widgets.RadioSelect,
                               choices=[[1, 'your estimate of the number of pills in an image.'],
                                        [2, 'the true number of pills in an image.'],
                                        [3, 'whether your estimate is correct.']]
                               )
    cq_3 = models.IntegerField(label="How many pills are there in a given image?",
                               widget=widgets.RadioSelect,
                               choices=[
                                   [1, "at least 50 pills"],
                                   [2, "Between 0 and 400 pills"],  # Correct Answer
                                   [3, "at most 260 pills"],
                                   [4, "This cannot be known"]])
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
    belief_bonus = models.IntegerField(initial=2)
    current_donation_payoff = models.IntegerField()
    current_belief_A_payoff = models.IntegerField()
    current_belief_B_payoff = models.IntegerField()
    payoff_decision = models.StringField()

    # Other behavior during elicitation
    page_loaded = models.IntegerField()
    time_out = models.BooleanField()

    # Feedback
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
# obs current belief payoff does not seem to work!!!
# - test randomization of pictures!!! using console log with the picture names!

# - emphasize that there is no (immediate) feedback on belief accuracy!
# - maybe not call it estimation but best guess or belief or so in the instructions!
# - as elicited by their donation in a dictator game with other participants at the end of the experiment

# think about how to deal with with time-out variable

# include honey pot properly on donation page!
# update trial page buttons in the same way as donation

###### For experiment
# - randomize treatments with high & low incentives
# - implement ex ante and ex post treatment

# The experiment is programmed such that subjects:
# -	who do not enter their belief estimate on time two times (within 20 seconds),
# -	who do not manage to answer an attention check correctly,
# -	who fail to answer the control questions testing their understanding of the instructions correctly within two attempts
# are excluded from the experiment.


# think about how to assign treatment most elegantly/practically
# https://github.com/chkgk/otree_adaptive_treatment_assignment/blob/master/adaptive_assignment_demo/models.py




