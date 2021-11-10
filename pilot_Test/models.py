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


doc = """
This is a pilot snippet testing the matrix belief elicitation task. 
"""


class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = None
    num_rounds = 2

    duration_min = 10
    sec_intro = 3
    sec_per_matrix = 3
    sec_to_answer = 20
    accuracy_bonus = 1


class Subsession(BaseSubsession):
    pass


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
    project_id_A = models.IntegerField()
    num_x_true_A = models.IntegerField()
    num_x_belief_A = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_min_A = models.IntegerField(blank=True, min=0, max=400, doc="records min belief on number of Xs in matrix")
    num_x_belief_max_A = models.IntegerField(blank=True, min=0, max=400, doc="records max belief on number of Xs in matrix")

    # Characteristics of Project B
    project_id_B = models.IntegerField()
    num_x_true_B = models.IntegerField()
    num_x_belief_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_min_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_max_B = models.IntegerField(blank=True, min=0, max=400, doc="records belief on number of Xs in matrix")

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
# - update matrices and load them through a data set
