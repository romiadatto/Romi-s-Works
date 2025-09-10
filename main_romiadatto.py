from colorama import init, Fore, Back
init(autoreset=True)

# constant variables
FIRST_HOUR = 8
LAST_HOUR = 16

DAYS_NAMES = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]

DAYS_INDEX = {
    "sunday": 1,
    "monday": 2,
    "tuesday": 3,
    "wednesday": 4,
    "thursday": 5,
    "friday": 6
}


def create_schedule(number_of_days, number_of_hours):  # creating schedule
    schedule = []
    for day in range(number_of_days):
        row = []
        for hour in range(number_of_hours):
            row.append("Free")
        schedule.append(row)
    return schedule


def print_schedule(schedule):  # printing schedual as well
    print(Back.MAGENTA + Fore.BLACK + "Schedule:")
    for i in range(len(schedule)):
        print(DAYS_NAMES[i], ":", ' '.join(map(str, schedule[i])))


def split_lesson(
        lesson_text):  # splits the received string and returns a list with separate values
    if (lesson_text != None):
        parts = lesson_text.split("_")
        if len(parts) != 4:
            return None

        lesson_name = parts[0]
        lesson_duration = int(parts[1])
        lesson_day = parts[2].lower()
        lesson_start = int(parts[3])

        return [lesson_name, lesson_duration, lesson_day, lesson_start]

    else:
        return None


# 3
def check_place(schedule, lesson,
                number_of_hours):  # Checks if the lesson can be entered without a problem and returns a boolean value.
    lesson_name = lesson[0]
    lesson_duration = lesson[1]
    lesson_day = lesson[2]
    lesson_start = lesson[3]

    if lesson_day not in DAYS_NAMES:
        return False

    day_index = DAYS_INDEX[lesson_day] - 1
    start_index = lesson_start - FIRST_HOUR

    if lesson_start < FIRST_HOUR or lesson_start + lesson_duration > LAST_HOUR:
        return False

    if start_index < 0 or start_index + lesson_duration > number_of_hours:
        return False

    for i in range(start_index, start_index + lesson_duration):
        if schedule[day_index][i] != "Free":
            return False

    return True


# 3
def put_lesson(schedule, lesson):  # Physically slotting the lesson
    lesson_name = lesson[0]
    lesson_duration = lesson[1]
    lesson_day = lesson[2]
    lesson_start = lesson[3]

    day_index = DAYS_INDEX[lesson_day] - 1
    start_index = lesson_start - FIRST_HOUR

    for i in range(start_index, start_index + lesson_duration):
        schedule[day_index][i] = lesson_name


# 3
def insert_requested_lessons(schedule, lessons,
                             number_of_hours):  # Schedules lessons according to user input and possible conditions, and returns those that do not meet these requirements to the failed list.
    failed_lessons = []
    for lesson in lessons:
        if check_place(schedule, lesson, number_of_hours):
            put_lesson(schedule, lesson)
        else:
            failed_lessons.append(lesson)

    print("Schedule after first insertion:")
    print_schedule(schedule)
    return failed_lessons


# 4
def try_again(schedule, lesson, number_of_hours,
              number_of_days):  # Attempt to reschedule the lesson first on the original day and then on other days
    lesson_name = lesson[0]
    lesson_duration = lesson[1]
    lesson_day = lesson[2]
    lesson_start = lesson[3]

    if lesson_day not in DAYS_NAMES:
        return False

    for i in range(number_of_days):
        for hour in range(FIRST_HOUR, LAST_HOUR - lesson_duration + 1):
            trial_lesson = [lesson_name, lesson_duration, DAYS_NAMES[i], hour]
            if check_place(schedule, trial_lesson, number_of_hours):
                put_lesson(schedule, trial_lesson)
                return True

    return False


# 4
def reinsert_failed_lessons(schedule, failed_lessons, number_of_hours,
                            number_of_days):  # Trying to reassign failed classes Returns a list of classes that have not yet been entered
    still_failed = []
    for lesson in failed_lessons:
        flag = try_again(schedule, lesson, number_of_hours, number_of_days)
        if flag == False:
            still_failed.append(lesson)

    return still_failed


def main():
    # first step
    number_of_days = int(input("Enter number of study days: "))
    while (number_of_days < 0 or number_of_days > 6):
        print("invalid input")
        number_of_days = int(input("Enter number of study days (max 6): "))

    number_of_hours = int(input("Enter number of study hours per day: "))
    while (number_of_hours > LAST_HOUR - FIRST_HOUR):
        print("invalid input")
        number_of_hours = int(
            input("Enter number of study hours per day (max 8): "))

    schedule = create_schedule(number_of_days, number_of_hours)

    # second step
    lessons = []
    while True:
        lesson_text = input(
            "Enter lesson [name_duration_day_start] or 'done' to finish: ")
        splits = split_lesson(lesson_text)
        if lesson_text.lower() != "done":
            while (splits[2] not in DAYS_INDEX or splits[3] < FIRST_HOUR or
                   splits[3] > LAST_HOUR or splits[1] > number_of_hours):
                print("invalid input or Bad time entry")
                lesson_text = input(
                    "Enter lesson [name_duration_day_start] or 'done' to finish: ")
                splits = split_lesson(lesson_text)
        else:
            break

        lesson = split_lesson(lesson_text)
        if lesson is None:
            print("Invalid input, try again...")

        lessons.append(lesson)

    # third step
    failed_lessons = insert_requested_lessons(schedule, lessons,
                                              number_of_hours)

    # fourth step
    still_failed = reinsert_failed_lessons(schedule, failed_lessons,
                                           number_of_hours, number_of_days)

    if len(still_failed) == 0:
        print(
            Fore.GREEN + "All lessons inserted successfully after reinsertion if needed.")
        print_schedule(schedule)
    else:
        print(Fore.RED + "The schedule's creation failed.")


main()
