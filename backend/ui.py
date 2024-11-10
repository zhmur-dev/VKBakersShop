STARTUP_MESSAGE = '''\nWelcome to VKBakersShop!\n
Don't forget to set variables in your '.env' file and run postgresql on your server before proceeding!\n'''
COMMANDS_MESSAGE = '''Enter command:
1. Create new database.
2. Populate database with sample data.
3. Delete existing database.
R. RUN VK BOT.
0. Exit\n
> '''
WRONG_COMMAND = 'Sorry, you might have entered a wrong command. Please try again.\n'

CREATING_DB = 'Creating database...'
DB_CREATED = 'Database created successfully\n'
POPULATING_DB = 'Populating database...'
DB_POPULATED = 'Database populated successfully\n'
DELETING_DB = 'Deleting database...'
DB_DELETED = 'Database deleted successfully\n'
LAUNCHING_BOT = 'VK Bot will now be launched.'

MAX_INLINE_BUTTONS = 2

GREETINGS_MESSAGE = 'Добро пожаловать в пекарню VK Bakers Shop!'
GET_CATEGORIES_MESSAGE = 'Мы предлагаем продукты в следующих категориях:'
GET_PRODUCTS_MESSAGE = 'Вот какие продукты есть у нас в категории {category_name}:'
ERROR_MESSAGE = '''
Извините, кажется произошла ошибка - направляем Вас в начало разговора!\n\n
''' + GET_CATEGORIES_MESSAGE

BACK_TO_CATEGORIES = '< Назад к категориям'
BACK_TO_PRODUCTS = '< Назад к категории {category_name}'
