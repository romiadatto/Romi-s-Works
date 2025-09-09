# קבועים
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


def create_schedule(number_of_days, number_of_hours):
    """
    יוצרת מערכת שעות דו מימדית עם "Free" בכל משבצת
    """
    schedule = []
    for day in range(number_of_days):
        row = []
        for hour in range(number_of_hours):
            row.append("Free")
        schedule.append(row)
    return schedule


def show_schedule(schedule):
    """
    מדפיסה את מערכת השעות בצורה ברורה
    """
    print("\nSchedule:")
    for day_index in range(len(schedule)):
        print(DAYS_NAMES[day_index], ":", schedule[day_index])


def split_lesson(lesson_text):
    """
    מפרקת מחרוזת של שיעור לפורמט name_duration_day_start
    מחזירה ברשימה
    """
    if(lesson_text!=None):
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


def check_place(schedule, lesson, number_of_hours):
    """
    בודקת אם אפשר להכניס את השיעור בלי בעיות
    """
    lesson_name = lesson[0]
    lesson_duration = lesson[1]
    lesson_day = lesson[2]
    lesson_start = lesson[3]

    if lesson_day not in DAYS_INDEX:
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


def put_lesson(schedule, lesson):
    """
    מכניסה שיעור למערכת
    """
    lesson_name = lesson[0]
    lesson_duration = lesson[1]
    lesson_day = lesson[2]
    lesson_start = lesson[3]

    day_index = DAYS_INDEX[lesson_day] - 1
    start_index = lesson_start - FIRST_HOUR

    for i in range(start_index, start_index + lesson_duration):
        schedule[day_index][i] = lesson_name


def try_again(schedule, lesson, number_of_hours, number_of_days):
    """
    ניסיון לשבץ מחדש שיעור שלא נכנס – קודם ביום המקורי, אחר כך בימים אחרים
    """
    lesson_name = lesson[0]
    lesson_duration = lesson[1]
    lesson_day = lesson[2]
    lesson_start = lesson[3]

    if lesson_day not in DAYS_INDEX:
        return False

    # ניסיון ביום המקורי
    for hour in range(FIRST_HOUR, LAST_HOUR - lesson_duration + 1):
        trial_lesson = [lesson_name, lesson_duration, lesson_day, hour]
        if check_place(schedule, trial_lesson, number_of_hours):
            put_lesson(schedule, trial_lesson)
            print("Lesson", lesson_name, "was re-inserted at", lesson_day, hour)
            return True

    # ניסיון בימים אחרים
    for new_day_index in range(number_of_days):
        for hour in range(FIRST_HOUR, LAST_HOUR - lesson_duration + 1):
            trial_lesson = [lesson_name, lesson_duration, DAYS_NAMES[new_day_index], hour]
            if check_place(schedule, trial_lesson, number_of_hours):
                put_lesson(schedule, trial_lesson)
                print("Lesson", lesson_name, "was re-inserted at", DAYS_NAMES[new_day_index], hour)
                return True

    return False


def insert_requested_lessons(schedule, lessons, number_of_hours):
    """
    שלב 3 – מנסה לשבץ את השיעורים כפי שהמשתמש ביקש
    מחזירה רשימת שיעורים שנכשלו
    """
    failed_lessons = []
    for lesson in lessons:
        if check_place(schedule, lesson, number_of_hours):
            put_lesson(schedule, lesson)
        else:
            failed_lessons.append(lesson)

    print("\nSchedule after first insertion:")
    show_schedule(schedule)
    return failed_lessons


def reinsert_failed_lessons(schedule, failed_lessons, number_of_hours, number_of_days):
    """
    שלב 4 – מנסה לשבץ מחדש שיעורים שנכשלו
    מחזירה רשימת שיעורים שעדיין לא נכנסו
    """
    still_failed = []
    for lesson in failed_lessons:
        success = try_again(schedule, lesson, number_of_hours, number_of_days)
        if not success:
            still_failed.append(lesson)

    return still_failed


def main():
    # שלב ראשון: קליטת נתוני מערכת
    number_of_days = int(input("Enter number of study days (max 6): "))
    number_of_hours = int(input("Enter number of study hours per day: "))

    schedule = create_schedule(number_of_days, number_of_hours)

    # שלב שני: קליטת שיעורים
    lessons = []
    while True:
        lesson_text = input("Enter lesson (name_duration_day_start) or 'done' to finish: ")
        list=split_lesson(lesson_text)
        if lesson_text.lower() != "done":
            while(list[2] not in DAYS_INDEX or list[3]<FIRST_HOUR):
                print("invalid input")
                lesson_text = input("Enter lesson (name_duration_day_start) or 'done' to finish: ")
                list = split_lesson(lesson_text)
        else:
            break

        lesson = split_lesson(lesson_text)
        if lesson is None:
            print("Invalid input, try again...")

        lessons.append(lesson)

    # שלב שלישי: ניסיון לשבץ לפי בקשת המשתמש
    failed_lessons = insert_requested_lessons(schedule, lessons, number_of_hours)

    # שלב רביעי: ניסיון לשבץ מחדש
    still_failed = reinsert_failed_lessons(schedule, failed_lessons, number_of_hours, number_of_days)

    if len(still_failed) == 0:
        print("\nAll lessons inserted successfully (after reinsertion if needed).")
        show_schedule(schedule)
    else:
        print("\nThe schedule's creation failed.")
        print("These lessons could not be inserted:", still_failed)


main()
