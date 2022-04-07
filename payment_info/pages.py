from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Terminated(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def is_displayed(self):
        return self.participant.vars['too_many_wrong'] or self.participant.vars['attention_check_failed']

    def vars_for_template(self):
        participant = self.participant
        if participant.vars['too_many_wrong']:
            too_many_wrong = True
            attention_fail = False
        elif participant.vars['attention_check_failed']:
            too_many_wrong = False
            attention_fail = True
        return {'too_many_wrong': too_many_wrong, 'attention_check_failed': attention_fail}
        # dict(redemption_code=participant.label or participant.code)


class PaymentInfo(Page):
    pass


page_sequence = [Terminated, PaymentInfo]
