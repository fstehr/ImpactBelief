from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def vars_for_template(self):
        participant = self.participant
        if participant.vars['trial_timeout_counter'] == 3 or participant.vars['timeout_counter'] == 2:
            timeout = True
            attention_fail = False
            final_payoff = 0
            final_payoff_plus_part_fee = self.session.config.participation_fee
        # elif participant.vars['attention_check_failed']== True:
        #     timeout = False
        #     attention_fail = True
        #     final_payoff = 0
        #     final_payoff_plus_part_fee = self.session.config.participation_fee
        else:
            timeout = False
            attention_fail = False
            final_payoff = participant.payoff
            final_payoff_plus_part_fee = participant.payoff_plus_participation_fee()

        return {'timeout': timeout, 'attention_check_failed': attention_fail, 'final_payoff_display': final_payoff,
                'final_payoff_plus_part_fee_display': final_payoff_plus_part_fee}
        # dict(redemption_code=participant.label or participant.code)


page_sequence = [PaymentInfo]
