import pep8
import datetime
import pytz


class Task:
    '''This class defines a single task with its attributes: title, date, time
    spent on the task and notes.'''
    def __init__(self, title, date, time_spent, notes='', date_of_entry=''):
        self.title = title
        self.date = date
        self.time_spent = time_spent
        self.notes = notes
        if date_of_entry == '':
            eu_pa = pytz.timezone('Europe/Paris')
            local_date = eu_pa.localize(datetime.datetime.now())
            self.date_of_entry = local_date.astimezone(pytz.utc)
        else:
            self.date_of_entry = date_of_entry

    @classmethod
    def get_task_info_in_list(cls, a_task):
        '''This method takes a task a argument and returns the task attributes
        in form of a list.'''
        timedate_fmt = '%Y-%m-%d %H:%M:%S.%f%z'
        a_task_in_list = []
        a_task_in_list.append(a_task.date_of_entry)
        a_task_in_list.append(a_task.title)
        a_task_in_list.append(a_task.date.strftime(timedate_fmt))
        a_task_in_list.append(a_task.time_spent)
        a_task_in_list.append(a_task.notes)
        return a_task_in_list

    @classmethod
    def parse_line_into_a_task(cls, a_list):
        '''This method takes a list as argument, parses the information to a
        task object and returns it.'''
        timedate_fmt = '%Y-%m-%d %H:%M:%S.%f%z'
        # datetime.timedelta(hours=-5)
        task_object = Task(date_of_entry=a_list[0],
                           title=a_list[1],
                           date=datetime.datetime.strptime(
                               a_list[2], timedate_fmt),
                           time_spent=int(a_list[3]),
                           notes=a_list[4])
        return task_object

    @classmethod
    def print_a_task(cls, a_task):
        '''This method takes cls and a task as argument and prints it in a
        ordered way to the console.'''
        # Convert date from UTC to local
        loc_tz = pytz.timezone('Europe/Paris')
        # task.date
        norm_date = loc_tz.normalize(a_task.date.astimezone(loc_tz))
        date_to_print = norm_date.strftime("%m/%d/%Y")
        # task.time_spent
        hours, minutes = a_task.time_spent // 60, a_task.time_spent % 60
        if hours < 10:
            hours = '0' + str(hours)
        if minutes < 10:
            minutes = '0' + str(minutes)
        time_spent_to_print = str(hours) + ':' + str(minutes)
        # Print the task item nicely
        print('------------------------------------------------')
        print('Title:                  {}'.format(a_task.title))
        print('Date:                   {}'.format(date_to_print))
        print('Time spent on task:     {}'.format(time_spent_to_print))
        print('Notes to the task:      {}'.format(a_task.notes))
        print('------------------------------------------------')

'''
# Testing
task = Task('test task title', datetime.datetime.strptime(
    '2010-03-02 23:00:00+0000',
    '%Y-%m-%d %H:%M:%S%z'),
            'this is a note')
#print(Task.get_task_info_in_list(task)[0])
a_line = "tasktitle, 2019-04-02 23:00:00+0000,987,this is a note"
# print(Task.parse_line_into_a_task(a_line, delimiter=",").title)
# print(task.UID)
# print(Task.get_task_info_in_list(task)[0])
# Task.print_a_task(task)
'''
checker = pep8.Checker('task.py')
checker.check_all()
