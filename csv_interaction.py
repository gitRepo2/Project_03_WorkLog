import csv
import re
import pep8
import datetime

from task import Task

csv.register_dialect('taskDialect', delimiter=',', quotechar='|')


class CSV_interaction:
    @classmethod
    def write_task_in_file(cls, task_ob):
        '''This method takes cls and a task object as argument and
        write the task in one line into the a text file.'''
        with open('tasklist.csv', 'a', newline='') as csvfile:
            taskwriter = csv.writer(csvfile, dialect='taskDialect')
            taskwriter.writerow(Task.get_task_info_in_list(task_ob))

    @classmethod
    def delete_task_in_file(cls, task_to_del):
        '''This method takes cls and a task object and deletes the line
        in the tasklist.csv text file that corresponds to the given task.'''
        # Create a file if there isn't one
        try:
            file = open('tasklist.csv', 'r')
        except IOError:
            file = open('tasklist.csv', 'w')
        # Read lines from the file
        list_of_tasks = cls.read_task_from_file()
        with open('tasklist.csv', 'w', newline='') as csvfile:
            for task in list_of_tasks:
                if str(task.date_of_entry) != str(task_to_del.date_of_entry):
                    tasks_writer = csv.writer(csvfile, dialect='taskDialect')
                    tasks_writer.writerow(Task.get_task_info_in_list(task))

    @classmethod
    def read_task_from_file(cls):
        '''This method takes cls as argument and parses the content
        of the file tasklist.csv into a list of tasks. This list is
        returned.'''
        # Create a file if there isn't one
        try:
            file = open('tasklist.csv', 'r')
        except IOError:
            file = open('tasklist.csv', 'w')
        # Read lines from the file
        list_of_tasks = []
        with open('tasklist.csv',
                  'r',
                  newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=",",
                                quotechar='|')
            try:
                for row in reader:
                    list_of_tasks.append(Task.parse_line_into_a_task(row))
            except:
                print('Oops. Something went wrong while reading the csv file.')
        return list_of_tasks

'''
# Testing
eu_pa =  pytz.timezone('Europe/Paris')
local_date = eu_pa.localize(datetime.datetime.now())
date = local_date.astimezone(pytz.utc)
task1 = Task('myTitleProgram', date, date, 'someNotes')
print('task1.date: ', task1.date)
CSV_interaction().write_task_in_file(task1)
CSV_interaction().delete_task_in_file(task1)
# list_of_tasks = CSV_interaction().read_task_from_file()
'''
checker = pep8.Checker('csv_interaction.py')
checker.check_all()
