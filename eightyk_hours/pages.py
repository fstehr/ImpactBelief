from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    pass


class Evaluation(Page):
    form_fields = ['pressingness', 'contribution', 'personal_fit', 'enthusiasm', 'individual', 'comments']


class Results(Page):
    pass


page_sequence = [Welcome, Evaluation, Results]
