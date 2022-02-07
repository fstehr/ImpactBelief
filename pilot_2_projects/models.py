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
"""


class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('pilot_2_projects/static/Parameters.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    num_rounds = len(paras)

    # timing parameters for display
    duration_min = 10
    endowment = 40


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize parameter order on subject level
        if self.round_number == 1:
            for p in self.session.get_participants():
                paras = Constants.paras.copy()
                random.shuffle(paras)

                p.vars['parameters'] = paras  # store shuffled list of parameters in participant vars, then access each element by round number
                # print(p.vars['parameters'])  # prints participant vars to double check randomization

                # assign one payment round
                rounds = range(1, Constants.num_rounds + 1)
                p.vars['payment_round'] = random.choice(rounds)
                print("Payment round is", p.vars['payment_round'])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # background vars
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    finishing_time = models.LongStringField(doc="Time at which last page is reached")
    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")
    attention_check = models.StringField(blank=True, doc="Filter question for attention.",
                                          label="To make sure you have read the instructions, we ask you to answer 'apple' in the field below.")

    # Characteristics of Project A
    num_doses_A = models.IntegerField()
    price_A = models.IntegerField()
    efficiency_A = models.FloatField()
    donation_A = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[
                                         [True, 'Yes'],
                                         [False, 'No'],
                                     ]
                                     )
    current_payoff = models.IntegerField()

    # Characteristics of Project B
    num_doses_B = models.IntegerField()
    price_B = models.IntegerField()
    efficiency_B = models.IntegerField()
    donation_B = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[
                                         [True, 'Yes'],
                                         [False, 'No'],
                                     ]
                                     )

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

# --> update donation/belief  screens
# - remove code duplicates - mainly move all images into a global folder and reference from there!


# - randomize order of project A & B (i.e. from csv file to html) --> include a dummy variable cheapleft for orders
# - emphasize that there is no (immediate) feedback on belief accuracy!
# - code belief etc. data s.t. the data is called proj low and proj hi ?
# --> randomization of order of display is done on html level



# The form field page_loaded has errors, but its error message is not being displayed, possibly because you did not include the field in the page. There are 2 ways to fix this:
#
# Include the field with the formfield tag, e.g. {% formfield player.page_loaded %}
# If you are not using formfield but are instead writing the raw HTML for the form input, remember to include {{ form.page_loaded.errors }} somewhere in your page's HTML.