from os import environ


SESSION_CONFIGS = [
    dict(
        name='compensation_beliefs',
        display_name='Compensation DiffResp Beliefs - Experiment',
        num_demo_participants=9,
        app_sequence=['compensation_beliefs'],
        mode="follow-up",
        treatments_played="134",
        num_groups=1,
        doc="""
            Edit the 'treatments_played' parameter to change which treatments are played.
            Possible values are 1234 (Ind, Harm, Resp, Risk), 123, 124, ... and all other combinations of 
            3 treatments
            """
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=0, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = 'ow62l+tjbu=p=v%q-i5mvpd4g^a@j1pan&ny6rd-cnsj8im%-r'

INSTALLED_APPS = ['otree', 'slider_task']
