from backend import bot, database, ui

if __name__ == '__main__':
    print(ui.STARTUP_MESSAGE)
    while True:
        choice = input(ui.COMMANDS_MESSAGE)
        if choice == '1':
            database.create_db()
        elif choice == '2':
            database.populate_db()
        elif choice == '3':
            database.delete_db()
        elif choice == 'R':
            print(ui.LAUNCHING_BOT)
            bot.run_bot()
        elif choice == '0':
            exit()
        else:
            print(ui.WRONG_COMMAND)
