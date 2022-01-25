import os

__DEFAULT_URL = 'postgres://aebcrhjenauqmh:dea835d585ba77abdec9005b421d0843f62b6b55c200b25f656021012b8873b5@ec2-34' \
                '-242-89-204.eu-west-1.compute.amazonaws.com:5432/dbc834tv39kdsn'
DB_DSN = os.environ.get('DATABASE_URL', __DEFAULT_URL)

BOT_TOKEN = '5222656934:AAEwBp638yg_TCPfxPtKdCG_rv7cz1g6Vy4'

APP_URL = 'https://stegholdbot.herokuapp.com/'
