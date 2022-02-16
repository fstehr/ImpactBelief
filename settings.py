from os import environ


SESSION_CONFIGS = [
    dict(
        name='pilot_donation',
        display_name='Pilot Donation',
        num_demo_participants=2,
        app_sequence=['pilot_donations'],
    ),
    dict(
        name='pilot_1_project',
        display_name='Pilot: 1 project per screen',
        num_demo_participants=2,
        app_sequence=['pilot_1_project'],
    ),
    dict(
        name='pilot_2_projects',
        display_name='Pilot: 2 projects per screen',
        num_demo_participants=2,
        app_sequence=['pilot_2_projects'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=2.40, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
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
