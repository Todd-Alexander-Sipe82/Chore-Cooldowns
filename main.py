import csv
from datetime import datetime

# Chore list format: [chore name, cooldown, last day completed, ready]
# Cooldown: how often the chore needs to be done in days.
# Last day completed: if -1, it hasn't been done yet. Otherwise, day number of the year is how this is tracked.
# Ready: 'Ready' means chore needs to be done, 'On Cooldown' means it does not need to be done.

# IMPROVEMENTS:
# What if I want to do a different chore, but not mark current as complete?
# What about priority?

# open existing chore list, print to list of lists
with open('Chores', 'r') as infile:
    read = csv.reader(infile)
    chores = list(read)

# set the current day as a number
day_of_year = datetime.now().timetuple().tm_yday


# this function updates the ready status of a chore, based on: cooldown + day_of_year
def update(ls):
    for item in ls:
        if item[2] != '-1':
            if int(item[2]) + int(item[1]) > day_of_year:
                item[3] = 'On Cooldown'
            else:
                item[3] = 'Ready'
        else:
            item[3] = 'Ready'
    return ls


chores = update(chores)


def determine_chore(ls):
    chore = ''
    cooldown = 0
    counter = 0
    for item in ls:
        counter += 1
        # check ready
        if int(item[3] == 'Ready'):
            # check -1
            if int(item[2]) == -1:
                # check if highest (or tied with highest, in which case original stays)
                if int(item[1]) > cooldown:
                    chore = item[0]
                    cooldown = int(item[1])
    return chore


# this function is run when a chore has been finished, updating the completed day
def do_chore(ls, chore):
    for item in ls:
        if item[0] == chore:
            item[2] = day_of_year
            item[3] = 'On Cooldown'
    return ls


print("Welcome to Todd's Chore Tracker.")
print("Today is day number: " + str(day_of_year))
print("Commands:")
print("  'd' when finished with the current chore.")
print("  'q' to exit program and save progress.")
# print("  'c' to cycle to the next unfinished chore.") # this could be an improvement
user_input = ''
while user_input != 'q':
    current_chore = determine_chore(chores)
    if current_chore != '':
        print('The chore that needs to be done is: ' + current_chore)
    else:
        print('Wow, all of the chores are done. Nice!')
        break
    user_input = input('Enter command:')
    if user_input == 'd':
        chores = do_chore(chores, current_chore)
        print('Great job, you did a chore.')


# exit routine
print('Okay, great job today. Come back later to log more chores.')
# write the updated list to csv
with open('Chores', 'w', newline='') as outfile:
    write = csv.writer(outfile)
    write.writerows(chores)
