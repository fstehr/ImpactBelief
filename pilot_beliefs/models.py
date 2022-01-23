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
This is a pilot snippet testing the matrix belief elicitation task. 
"""


class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('pilot_beliefs/static/Parameters2.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    num_rounds = len(paras)

    # timing parameters for display
    duration_min = 10
    sec_intro = 3
    sec_per_matrix = 7
    sec_to_answer = 20
    accuracy_bonus = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                paras = Constants.paras.copy()
                random.shuffle(paras)

                p.vars['parameters'] = paras  # store shuffled list of parameters in participant vars, then access each element by round number
                print(p.vars['parameters'])  # prints participant vars to double check randomization


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # background vars
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    finishing_time = models.LongStringField(doc="Time at which last page is reached")
    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")

    attention_check = models.StringField(doc="Filter question for attention.",
                                          label="To make sure you have read the instructions, we ask you to answer 'apple' in the field below.")

    # Characteristics of Project A
    num_x_true_A = models.IntegerField()
    num_x_belief_A = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_min_A = models.IntegerField(blank=True, min=0, max=400, doc="records min belief on number of Xs in matrix")
    num_x_belief_max_A = models.IntegerField(blank=True, min=0, max=400, doc="records max belief on number of Xs in matrix")
    confidence_belief_A = models.IntegerField(initial=20, min=0, max=20, doc="cognitive uncertainty measure adapted from Enke, Graeber (2021)")
    donation_A = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[
                                         [True, 'Yes'],
                                         [False, 'No'],
                                     ]
                                     )

    # Characteristics of Project B
    num_x_true_B = models.IntegerField()
    num_x_belief_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_min_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_max_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    confidence_belief_B = models.IntegerField(initial=20, min=0, max=20, doc="cognitive uncertainty measure adapted from Enke, Graeber (2021)")
    donation_B = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[
                                         [True, 'Yes'],
                                         [False, 'No'],
                                     ]
                                     )

    # Other behavior during elicitation
    page_loaded = models.IntegerField()
    time_out = models.BooleanField()

    # Feedback
    fun = models.IntegerField(min=0, max=10, label="How much did you enjoy the estimation task?",
                              widget=widgets.RadioSelectHorizontal, choices = range(0, 11))
    difficult = models.IntegerField(min=0, max=10, label="How difficult did you find the estimation task?",
                              widget=widgets.RadioSelectHorizontal, choices = range(0, 11))
    speed = models.IntegerField(min=0, max=10, label="How appropriate did you find the time to fill in your estimates?",
                                    widget=widgets.RadioSelectHorizontal, choices=range(0, 11))
    comments = models.LongStringField(blank=True, label="Do you have any additional feedback for us?")


# TO DO
# - fix javascript protocol on decision screen
# - update matrices and load them through a data set
# - look at estimation data with correct matrix again
# - randomize order of project A & B (i.e. from csv file to html)
# - include pictures in instructions -> donation impact
# - emphasize that there is no (immediate) feedback on belief accuracy!
# - code belief etc. data s.t. the data is called proj low and proj hi ?
# --> randomization of order of display is done on html level
# - include warm glow survey item from Carpenter (2021) JEBO "Think about the last time you gave to charity before today. What was most important to you (i) the total amount given by everyone, (ii) the amount that you personally gave or (iii) some other aspect of giving?”

# The form field page_loaded has errors, but its error message is not being displayed, possibly because you did not include the field in the page. There are 2 ways to fix this:
#
# Include the field with the formfield tag, e.g. {% formfield player.page_loaded %}
# If you are not using formfield but are instead writing the raw HTML for the form input, remember to include {{ form.page_loaded.errors }} somewhere in your page's HTML.