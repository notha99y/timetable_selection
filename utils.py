import re
from datetime import datetime


def get_day(timeslot):
    """
    assume timeslot is Day starttime to endtime
    """

    if type(timeslot) != str:
        # assume it is na
        return None
    else:
        return timeslot.split(" ")[0]


def refine_time_parsing(df, time_column):
    """
    Improves the parsing of time ranges by handling edge cases and filling in missing values.
    """

    def time_to_24h(t):
        """Convert 12-hour time format to 24-hour time."""
        return (
            datetime.strptime(t, "%I%p").time()
            if "." not in t
            else datetime.strptime(t, "%I.%M%p").time()
        )

    starts, ends = [], []
    for entry in df[time_column]:
        match = re.search(r"(\d+\.?\d*\w+)\s*to\s*(\d+\.?\d*\w+)", str(entry))
        if match:
            starts.append(time_to_24h(match.group(1)))
            ends.append(time_to_24h(match.group(2)))
        else:
            starts.append(None)
            ends.append(None)

    df[f"{time_column}_Start"] = starts
    df[f"{time_column}_End"] = ends
    return df


def check_overlap(first_class, second_class):
    """
    class: (day, start_time, end_time)
    """
    if type(first_class[0]) != str or type(second_class[1]) != str:
        return False

    if first_class[1] is None:
        return False

    return (
        first_class[1] < second_class[2]
        and second_class[1] < first_class[2]
        and first_class[0] == second_class[0]
    )


def check_conflict(current_schedule, new_class):
    for s in current_schedule:
        # check lecture with lecture
        class_1 = (s["lecture_day"], s["Lecture_Start"], s["Lecture_End"])
        class_2 = (
            new_class["lecture_day"],
            new_class["Lecture_Start"],
            new_class["Lecture_End"],
        )
        if check_overlap(class_1, class_2):
            return True

        # check lecture with tutorial
        class_1 = (s["lecture_day"], s["Lecture_Start"], s["Lecture_End"])
        class_2 = (
            new_class["tutorial_day"],
            new_class["Tutorial_Start"],
            new_class["Tutorial_End"],
        )
        if check_overlap(class_1, class_2):
            return True

        # check tutorial with lecture
        class_1 = (s["tutorial_day"], s["Tutorial_Start"], s["Tutorial_End"])
        class_2 = (
            new_class["lecture_day"],
            new_class["Lecture_Start"],
            new_class["Lecture_End"],
        )
        if check_overlap(class_1, class_2):
            return True

        # check tutorial with tutorial
        class_1 = (s["tutorial_day"], s["Tutorial_Start"], s["Tutorial_End"])
        class_2 = (
            new_class["tutorial_day"],
            new_class["Tutorial_Start"],
            new_class["Tutorial_End"],
        )
        if check_overlap(class_1, class_2):
            return True
    return False


def check_solution_is_valid(solution, num_combi, num_units):
    if len(solution) != num_combi:
        return False
    for s in solution:
        if len(s) != num_units:
            return False

    return True


def print_solution(solution, show_selected_days=True):
    for s in solution:
        selected_days = []
        for c in s:
            print(
                f"{c['Module']} | {c['Class']} | {c['Lecture']} | {c['Tutorial']}"
            )
            selected_days.append(c["lecture_day"])
            selected_days.append(c["tutorial_day"])
        if show_selected_days:
            selected_days = list(set(selected_days))
            print("selected days: ", selected_days)

        print("-" * 88)
