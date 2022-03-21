from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Terminated(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def is_displayed(self):
        return self.participant.vars['too_many_wrong'] == True \
                or self.participant.vars['timeout_counter'] == 2 \
               or self.participant.vars['attention_check_failed'] == True

    def vars_for_template(self):
        participant = self.participant
        if participant.vars['too_many_wrong'] == True:
            too_many_wrong = True
            attention_fail = False
            timeout = False
        elif participant.vars['attention_check_failed'] == True:
            too_many_wrong = False
            attention_fail = True
            timeout = False
        elif participant.vars['timeout_counter'] == 2:
            too_many_wrong = False
            attention_fail = False
            timeout = True
        return {'too_many_wrong': too_many_wrong, 'timeout': timeout, 'attention_check_failed': attention_fail}
        # dict(redemption_code=participant.label or participant.code)


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def vars_for_template(self):
        participant = self.participant
        timeout_in_payment_decision = participant.vars['timeout_in_payment_decision']

        final_payoff = participant.payoff
        final_payoff_plus_part_fee = participant.payoff_plus_participation_fee()
        link = 'https://app.prolific.co/submissions/complete?cc=F4F99D60'

        return {'timeout_in_payment_decision': timeout_in_payment_decision,
                'final_payoff_display': final_payoff,
                'final_payoff_plus_part_fee_display': final_payoff_plus_part_fee,
                'link': link}
        # dict(redemption_code=participant.label or participant.code)


page_sequence = [Terminated, PaymentInfo]
