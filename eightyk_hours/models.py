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

author = 'Your name here'

doc = """
Your app description
"""


def make_likert_field(label):  # create a Likert type field with a 10 point scale form 0 to 10, with the argument 'label'
    choices = range(0, 11)
    return models.IntegerField(
        choices=choices,
        widget=widgets.RadioSelect,
        label=label,
    )



class Constants(BaseConstants):
    name_in_url = 'eightyk_hours'
    players_per_group = None

    # Get items from csv file
    with open('eightyk_hours/static/proposals.csv', encoding='utf-8-sig') as parameters:
        items = list(csv.DictReader(parameters, dialect='excel'))
        # create sub-dictionaries for each topic-based table
        environment = []
        politics = []
        education = []
        decision = []
        society = []
        health = []

        for i in range(len(items)):
            if items[i]['header1'] == "Umwelt":
                environment.append(items[i])
            elif items[i]['header1'] == "Politische Partizipation":
                politics.append(items[i])
            elif items[i]['header1'] == "Bildung":
                education.append(items[i])
            elif items[i]['header1'] == "Qualität von Entscheidungen":
                decision.append(items[i])
            elif items[i]['header1'] == "Gesellschaftlicher Zusammenhalt":
                society.append(items[i])
            elif items[i]['header1'] == "Gesundheit":
                health.append(items[i])

    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # generate many fields for each item and question
    # for i in range(len(Constants.items)):
    #   exec("item_%s = models.IntegerField()" % i)

    pressingness = make_likert_field("How pressing do you think the problem is?")
    contribution = make_likert_field("How do you evaluate the magnitude of the contribution by this idea?")
    personal_fit = make_likert_field("How do you rate Frauke's personal fit with this idea? (skills, interests,...)")
    enthusiasm = make_likert_field("How enthusiastic are you about this idea?")
    individual = make_likert_field("To what extent do you think it is managable to start working on this project idea by oneself?")
    comments = models.LongStringField()

