# Work-Log project
# Lukas Straumann, 02-Apr-2018, V1.0
import pep8
import os
import datetime
import pytz
import re
import collections as col
from collections import OrderedDict

from csv_interaction import CSV_interaction
from task import Task


class UserInteraction(Task):
    def __init__(self):
        d = OrderedDict()
        d['a'] = ['a: Add a new task.', self.add_new_task]
        d['b'] = ['b: Search for a task.', self.do_nothing]
        d['c'] = ['c: Quit the program.', self.quit_program]
        self.MENU_OPTIONS = d

        d = OrderedDict()
        d['a'] = ['a: by a date', self.search_by_date]
        d['b'] = ['b: by a range of dates', self.search_by_range_of_dates]
        d['c'] = ['c: by an exact pattern', self.search_by_exact_pattern]
        d['d'] = ['d: by a regular expression pattern', self.search_by_regex]
        d['e'] = ['e: by the time spent of the task', self.search_by_timespent]
        d['f'] = ['f: Return to main menu', self.do_nothing]
        self.SEARCH_OPTIONS = d

        d = OrderedDict()
        d['n'] = ['[N]ext', self.do_nothing]
        d['e'] = ['[E]dit', self.edit_task]
        d['d'] = ['[D]elete', self.delete_task]
        d['r'] = ['[R]eturn', self.do_nothing]
        self.S_RESULT_OPTIONS = d

    def do_nothing(self):
        pass

    def welcome_message(self):
        '''This method prints a start text in the console for the user.'''
        self.clear_screen()
        print('Welcome to Work-Log.\n')

    def show_main_menu(self):
        '''This method shows the main menu to the user and returns the
        user input choice e.g. 'b'. '''
        while True:
            print('\nWhat would you like to do:\n')
            for menu_item in self.MENU_OPTIONS:
                    print(self.MENU_OPTIONS[menu_item][0])
            user_input = input().lower()
            if user_input in self.MENU_OPTIONS:
                return user_input
            else:
                print("Your input: '{}' is not available in the menu. ".format(
                    user_input))
                print("Please try again.\n")

    def show_search_menu(self):
        '''This method shows the search sub menu and ask the user to choose
        an option. It returns a choise e.g. 'a'. '''
        while True:
            print('\nWould you like to search: ')
            for menu_item in self.SEARCH_OPTIONS:
                    print(self.SEARCH_OPTIONS[menu_item][0])
            user_input = input().lower()
            if user_input in self.SEARCH_OPTIONS:
                return user_input
            else:
                print("Your input: '{}' is not available in ".format(
                    user_input))
                print("the search menu. Please try again.\n")

    def add_new_task(self):
        '''This method take self as argument and ask the user to input
        all necessary information to add a task. The new task is added to
        the CSV file.'''
        while True:
            # Ask for the name of the task
            name_input = input("Please key in the name of the task. ")
            print("\nWhen is this task due? ")
            # Ask for the date of the task
            while True:
                date_input = input("Please use MM/DD/YYYY format. ")
                try:
                    parsed_input_date = datetime.datetime.strptime(
                        date_input, '%m/%d/%Y')
                except ValueError:
                    print("'{}' doesn't seem to be a valid date.".format(
                        date_input))
                else:
                    if date_input == '01/01/0001':
                        print('This date is not allowed to be used.')
                    else:
                        local_date = pytz.timezone('Europe/Paris').localize(
                            parsed_input_date)
                        utc_date = local_date.astimezone(pytz.utc)
                        break
            # Ask for time spent on the task
            print("\nHow much time did you spend on task '{}'? ".format(
                name_input))
            while True:
                time_input = input("Please use a HH:MM format. ")
                try:
                    local_date = datetime.datetime.strptime(time_input,
                                                            '%H:%M')
                except ValueError:
                    print("{} doesn't seem to be a valid time.".format(
                        time_input))
                else:
                    # Convert spent time user input to minutes
                    m = re.match(r'^(?P<hours>\d\d):(?P<minutes>\d\d)',
                                 time_input)
                    hours = int(m.group('hours'))
                    minutes = int(m.group('minutes'))
                    time_input = hours * 60 + minutes
                    break
            # Ask for notes to the task
            notes_input = input("Please key any notes to this task. ")
            break
        # Add (write) the new task into a file
        CSV_interaction.write_task_in_file(Task(name_input,
                                                utc_date,
                                                time_input,
                                                notes_input))

    def search_by_range_of_dates(self):
        '''This method takes self as argument. It get the tasks as a
        list from the text file and guides the user to search tasks within
        a specific range of dates. It returns a list with eventually found
        tasks.'''
        # Extract tasks for file
        list_of_tasks = CSV_interaction.read_task_from_file()
        # End the method if no task is available
        if len(list_of_tasks) == 0:
            return []
        # Ask for a search date
        print("\nIn which period of time has the task been assinged for? ")
        while True:
                date_input = input("Please use MM/DD/YYYY-MM/DD/YYYY format. ")
                try:
                    date_start, date_end = date_input[:10], date_input[-10:]
                    parsed_date_start = datetime.datetime.strptime(
                        date_start, '%m/%d/%Y')
                    parsed_date_end = datetime.datetime.strptime(
                        date_end, '%m/%d/%Y')
                except ValueError:
                    print("{} doesn't seem to be valid dates.".format(
                        date_input))
                else:
                    loc_timezone = pytz.timezone('Europe/Paris')
                    local_date_start = loc_timezone.localize(parsed_date_start)
                    local_date_end = loc_timezone.localize(parsed_date_end)
                    utc_date_start = local_date_start.astimezone(pytz.utc)
                    utc_date_end = local_date_end.astimezone(pytz.utc)
                    break
        found_tasks = []
        for task in list_of_tasks:
            if utc_date_start < task.date and utc_date_end > task.date:
                found_tasks.append(task)
        return found_tasks

    def search_by_date(self):
        '''This method takes self as argument. It get the tasks dates as a
        list from the text file and guides the user to chose tasks with
        a specific date from the given list. It returns a list with eventually
        found tasks.'''
        # Extract tasks for file
        list_of_tasks = CSV_interaction.read_task_from_file()
        # End the method if no task is available
        if len(list_of_tasks) == 0:
            return []
        # Convert date from UTC to local
        loc_tz = pytz.timezone('Europe/Paris')
        # Get normalize dates in a list
        norm_date_list = []
        for task in list_of_tasks:
            norm_date_list.append(loc_tz.normalize(task.date.astimezone(
                loc_tz)))
        # Remove duplicates and sort the list
        norm_date_list = sorted(list(set(norm_date_list)))
        dates = []
        for norm_date in norm_date_list:
            dates.append(norm_date.strftime("%m/%d/%Y"))
        # Print explanation to user
        print("Here is a list of date to choose tasks from:")
        # Print dates to console
        index = 0
        for date in dates:
            index += 1
            print(str(index) + ': ' + date)
        while True:
            user_input = input("Please choose a date by chosing a number: ")
            choice = 0
            try:
                choice = int(user_input)
                print('choice', choice)
                if 0 < choice and choice <= index:
                    break
                else:
                    text1 = "This number was not given as choice. "
                    text2 = "Please try again."
                    print(text1+text2)
            except ValueError:
                print("That was not a number input.")
        chosen_date = dates[choice-1]
        try:
            parsed_input_date = datetime.datetime.strptime(chosen_date,
                                                           '%m/%d/%Y')
        except ValueError:
            print("{} doesn't seem to be a valid date.".format(
                date_input))
        else:
            local_date = pytz.timezone('Europe/Paris').localize(
                parsed_input_date)
            utc_date = local_date.astimezone(pytz.utc)
        found_tasks = []
        for task in list_of_tasks:
            if utc_date == task.date:
                found_tasks.append(task)
        return found_tasks

    def search_by_exact_pattern(self):
        '''This method takes self as argument and allows the user to
        key in a search string. It then loops over all the tasks to
        find the exact string. A list of a tasks with matches string is
        returned.'''
        # Extract tasks for file
        list_of_tasks = CSV_interaction.read_task_from_file()
        # End the method if no task is available
        if len(list_of_tasks) == 0:
            return []
        # Ask for the name of the task
        text = "Please key in the exact search term of the task. "
        search_input = input(text)
        matches = 0
        found_tasks = []
        for task in list_of_tasks:
            task_as_list = Task.get_task_info_in_list(task)
            if search_input in "".join(str(i) for i in task_as_list):
                found_tasks.append(task)
        return found_tasks

    def search_by_regex(self):
        '''This method take self as argument and allows the user to enter
        an regular expression. It then loops over all the tasks to
        find this pattern. A list of a tasks with matches string is
        returned.'''
        # Extract tasks for file
        list_of_tasks = CSV_interaction.read_task_from_file()
        # End the method if no task is available
        if len(list_of_tasks) == 0:
            return []
        # Ask for the regular expression format to search within the tasks
        print("Please key in the regular expression for your search.")
        regex_input = input("e.g. \d\d ")
        if regex_input == '':
            print('\nNo regular expression was given.')
            return []
        found_tasks = []
        for task in list_of_tasks:
            task_as_list = Task.get_task_info_in_list(task)
            task_string = "".join(str(i) for i in task_as_list)
            try:
                if re.search(r'{}'.format(regex_input),
                             task_string, re.X) is not None:
                    found_tasks.append(task)
            except:
                print('Oops!! Something went wrong while searching.')
                break
        return found_tasks

    def search_by_timespent(self):
        '''This method takes self as argument and allows the user to
        search tasks by the time spent on the task. It then loops over all
        the tasks to find the exact amount of time spent in minutes.
        A list of a tasks with matches string is returned.'''
        # Extract tasks for file
        list_of_tasks = CSV_interaction.read_task_from_file()
        # End the method if no task is available
        if len(list_of_tasks) == 0:
            return []
        # Ask for the name of the task
        text = "Please key in the time spent on the task in minutes. "
        search_input = input(text)
        matches = 0
        found_tasks = []
        for task in list_of_tasks:
            if search_input in str(task.time_spent):
                found_tasks.append(task)
        return found_tasks

    def quit_program(self):
        '''This method prints a good bye message to the user.'''
        print('\nYou decided to quit. Have a good day.')

    def show_search_result(self, found_tasks):
        '''This method task self and found_tasks list a argument and provides
        the user with a displayed task where he can chose options for the
        found tasks.'''
        if len(found_tasks) == 0:
            print('\nNo task was found.')
        else:
            current = 0
            while True:
                if len(found_tasks) > 0:
                    print('\nResult: {} out of {} found tasks shown:'.format(
                        current+1,
                        len(found_tasks)))
                    Task.print_a_task(found_tasks[current])
                else:
                    print('No more tasks to show.')
                text1 = 'Choose [N]ext, [E]dit, [D]elete, '
                text2 = '[R]eturn as a next action.'
                user_input = input(text1+text2).lower()
                # Evaluate user input
                if user_input == 'n':
                    current += 1
                elif user_input == 'e':
                    if len(found_tasks) > 0:
                        self.edit_task(found_tasks[current])
                    else:
                        print('No more tasks to edit.')
                elif user_input == 'd':
                    if len(found_tasks) > 0:
                        self.delete_task(found_tasks[current])
                        found_tasks.pop(current)
                    else:
                        print('No more tasks to delete.')
                elif user_input == 'r':
                    break
                else:
                    print('\nThis is not a valid input. Please try again.')
                if current == len(found_tasks):
                    current = 0

    def edit_task(self, task):
        '''This method takes self and a task as argument. The user is guided
        step by step to edit the task. Once done, the task is update in the
        text file.'''
        while True:
            # Ask for the name of the task
            print("Your task to edit: '{}'. ".format(task.title))
            name_input = input("Please key in the edited name of the task. ")
            print("\nWhat is the task's new due date? ")
            # Ask for the date of the task
            while True:
                date_input = input("Please use MM/DD/YYYY format. ")
                try:
                    parsed_input_date = datetime.datetime.strptime(
                        date_input, '%m/%d/%Y')
                except ValueError:
                    print("{} doesn't seem to be a valid date.".format(
                        date_input))
                else:
                    local_date = pytz.timezone('Europe/Paris').localize(
                        parsed_input_date)
                    utc_date = local_date.astimezone(pytz.utc)
                    break
            # Ask for time spent on the task
            text = "\nHow much time does it take to finish the task "
            print(text + "'{}'? ".format(name_input))
            time_input = input("Please use a HH:MM format. ")
            try:
                time = datetime.datetime.strptime(time_input, '%H:%M')
            except ValueError:
                print("{} doesn't seem to be a valid time.".format(time_input))
            else:
                # Convert user input to minutes
                m = re.match(r'^(?P<hours>\d\d):(?P<minutes>\d\d)', time_input)
                hours = int(m.group('hours'))
                minutes = int(m.group('minutes'))
                time_input = hours * 60 + minutes
            # Ask for notes to the task
            notes_input = input("Please key the new notes to this task. ")
            break
        # Add (write) the new task into a file
        CSV_interaction.delete_task_in_file(task)
        # Add (write) the new task into a file
        CSV_interaction.write_task_in_file(Task(name_input,
                                                utc_date,
                                                time_input,
                                                notes_input))

    def delete_task(self, task_to_delete):
        '''This method takes self and a task object as arguments. It deletes
        the task from the text file.'''
        CSV_interaction.delete_task_in_file(task_to_delete)

    def clear_screen(self):
        '''This method clears the console screen.'''
        if os.name == "nt":
            os.system("cls")
            print('\n' * 50)
        else:
            os.system("clear")


def running():
    '''This function runs the top level user interaction.'''
    ui = UserInteraction()
    ui.welcome_message()
    while True:
        next_menu = ui.show_main_menu()
        # Call next_menu method based on user input
        ui.MENU_OPTIONS[next_menu][1]()
        if next_menu == 'c':
            break
        if next_menu == 'b':
            # Enter the sub menu 'search options'
            while True:
                next_menu = ui.show_search_menu()
                found_tasks = ui.SEARCH_OPTIONS[next_menu][1]()
                if next_menu == 'f':
                    break
                ui.show_search_result(found_tasks)


if __name__ == "__main__":
    running()

checker = pep8.Checker('main.py')
checker.check_all()
