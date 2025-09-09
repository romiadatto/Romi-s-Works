# קבועים
STARTING_HOUR = 8
ENDING_HOUR = 16

DAY_LIST = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]

DAYS_DICT = {
    "sunday": 1,
    "monday": 2,
    "tuesday": 3,
    "wednesday": 4,
    "thursday": 5,
    "friday": 6
}


def init_schedule(amount_of_days, hours_per_day):
    """
    יוצרת מערכת שעות דו מימדית עם Free בכל משבצת
    """
    schedule = []
    for i in range(amount_of_days):
        row = []
        for j in range(hours_per_day):
            row.append("Free")
        schedule.append(row)
    return schedule


def print_schedule(schedule):
    """
    מדפיסה את מערכת השעות בצורה ברורה
    """
    print("\nSchedule:")
    for i in range(len(schedule)):
        print(DAY_LIST[i], ":", schedule[i])


def parse_lesson(lesson_str):
    """
    מפרקת מחרוזת של שיעור לפורמט name_duration_day_start
    """
    try:
        parts = lesson_str.split("_")
        if len(parts) != 4:
            return None
        name = parts[0]
        duration = int(parts[1])
        day = parts[2].lower()
        start_hour = int(parts[3])
        return name, duration, day, start_hour
    except:
        return None


def can_insert(schedule, lesson, hours_per_day):
    """
    בודקת אם אפשר להכניס את השיעור בלי בעיות
    """
    name, duration, day, start_hour = lesson

    if day not in DAYS_DICT:
        return False

    day_index = DAYS_DICT[day] - 1
    start_index = start_hour - STARTING_HOUR

    if start_hour < STARTING_HOUR or start_hour + duration > ENDING_HOUR:
        return False

    if start_index < 0 or start_index + duration > hours_per_day:
        return False

    for i in range(start_index, start_index + duration):
        if schedule[day_index][i] != "Free":
            return False

    return True


def insert_lesson(schedule, lesson):
    """
    מכניסה שיעור למערכת
    """
    name, duration, day, start_hour = lesson
    day_index = DAYS_DICT[day] - 1
    start_index = start_hour - STARTING_HOUR

    for i in range(start_index, start_index + duration):
        schedule[day_index][i] = name


def try_reinsert(schedule, lesson, hours_per_day, amount_of_days):
    """
    ניסיון לשבץ מחדש שיעור שלא נכנס – קודם ביום המקורי, אחר כך בימים אחרים
    """
    name, duration, day, start_hour = lesson

    if day not in DAYS_DICT:
        return False

    # נסה ביום המקורי
    for hour in range(STARTING_HOUR, ENDING_HOUR - duration + 1):
        trial = (name, duration, day, hour)
        if can_insert(schedule, trial, hours_per_day):
            insert_lesson(schedule, trial)
            print("Lesson", name, "was re-inserted at", day, hour)
            return True

    # נסה בשאר הימים
    for new_day_index in range(amount_of_days):
        for hour in range(STARTING_HOUR, ENDING_HOUR - duration + 1):
            trial = (name, duration, DAY_LIST[new_day_index], hour)
            if can_insert(schedule, trial, hours_per_day):
                insert_lesson(schedule, trial)
                print("Lesson", name, "was re-inserted at", DAY_LIST[new_day_index], hour)
                return True

    return False


def insert_lessons_requested(schedule, lessons, hours_per_day):
    """
    שלב 3 – מנסה לשבץ את השיעורים כפי שהמשתמש ביקש
    מחזיר רשימת שיעורים שנכשלו
    """
    failed_lessons = []
    for lesson in lessons:
        if can_insert(schedule, lesson, hours_per_day):
            insert_lesson(schedule, lesson)
        else:
            failed_lessons.append(lesson)

    print("\nSchedule after first insertion:")
    print_schedule(schedule)
    return failed_lessons


def reinsert_failed_lessons(schedule, failed_lessons, hours_per_day, amount_of_days):
    """
    שלב 4 – מנסה לשבץ מחדש שיעורים שנכשלו
    מחזיר רשימת שיעורים שעדיין לא הצליחו להיכנס
    """
    still_failed = []
    for lesson in failed_lessons:
        success = try_reinsert(schedule, lesson, hours_per_day, amount_of_days)
        if not success:
            still_failed.append(lesson)

    return still_failed


def main():
    # שלב ראשון: קליטת נתוני מערכת
    amount_of_days = int(input("Enter number of study days (max 6): "))
    hours_per_day = int(input("Enter number of study hours per day: "))
    schedule = init_schedule(amount_of_days, hours_per_day)

    # שלב שני: קליטת שיעורים
    lessons = []
    while True:
        lesson_str = input("Enter lesson (name_duration_day_start) or 'done' to finish: ")
        if lesson_str.lower() == "done":
            break

        lesson = parse_lesson(lesson_str)
        if lesson is None:
            print("Invalid input format. Try again.")
            continue

        lessons.append(lesson)

    # שלב שלישי: ניסיון לשבץ לפי בקשת המשתמש
    failed_lessons = insert_lessons_requested(schedule, lessons, hours_per_day)

    # שלב רביעי: ניסיון לשבץ מחדש את מי שנכשל
    still_failed = reinsert_failed_lessons(schedule, failed_lessons, hours_per_day, amount_of_days)

    if len(still_failed) == 0:
        print("\nAll lessons inserted successfully (after reinsertion if needed).")
        print_schedule(schedule)
    else:
        print("\nThe schedule's creation failed.")
        print("These lessons could not be inserted:", still_failed)

main()
