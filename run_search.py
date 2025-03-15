import pandas as pd

from utils import (
    check_conflict,
    check_solution_is_valid,
    print_solution,
    refine_time_parsing,
)

csv_path = "data/test.csv"
dummy_module_names = ["Module A", "Module B", "Module C", "Module D"]
df = pd.read_csv(csv_path)

num_combi = 7
num_units = len(dummy_module_names)

unit_map = {}
for i, (k, _) in enumerate(df["Module"].value_counts().items()):
    unit_map[k] = dummy_module_names[i]

print(unit_map)

# Reapply refined parsing to lecture and tutorial times
df_cleaned = refine_time_parsing(df, "Lecture")
df_cleaned = refine_time_parsing(df, "Tutorial")
df_cleaned["lecture_day"] = df["Lecture"].apply(lambda x: x.split(" ")[0])
df_cleaned["tutorial_day"] = df["Tutorial"].apply(lambda x: x.split(" ")[0])
print(df_cleaned.head())
df_cleaned["module_mapped"] = df_cleaned["Module"].apply(lambda x: unit_map[x])

export_cols = ["Module", "Class", "Lecture", "Tutorial"]


def main():
    solution = []

    while not check_solution_is_valid(solution, num_combi, num_units):
        print("finding solution...")
        A_df = df_cleaned[df_cleaned["module_mapped"] == "Module A"].sample(
            frac=1
        )
        B_df = df_cleaned[df_cleaned["module_mapped"] == "Module B"].sample(
            frac=1
        )
        C_df = df_cleaned[df_cleaned["module_mapped"] == "Module C"].sample(
            frac=1
        )
        D_df = df_cleaned[df_cleaned["module_mapped"] == "Module D"].sample(
            frac=1
        )
        solution = []
        while len(solution) < num_combi:
            current_schedule = []
            selected_days = []
            for i_a, row_a in A_df.iterrows():
                if check_conflict(current_schedule, row_a):
                    # there is conflict
                    continue
                else:
                    # append to current_schedule and remove from selection
                    current_schedule.append(row_a)
                    A_df.drop(i_a, inplace=True)
                    selected_days.append(row_a["lecture_day"])
                    selected_days.append(row_a["tutorial_day"])

                    selected_days = list(set(selected_days))
                    break

            B_filtered_df = B_df[
                (~B_df["lecture_day"].isin(selected_days))
                | (~B_df["tutorial_day"].isin(selected_days))
            ]
            B_continue = False
            for i_b, row_b in B_filtered_df.iterrows():
                if check_conflict(current_schedule, row_b):
                    # there is conflict
                    continue
                else:
                    # append to current_schedule and remove from selection
                    current_schedule.append(row_b)
                    B_df.drop(i_b, inplace=True)
                    B_continue = True
                    selected_days.append(row_b["lecture_day"])
                    selected_days.append(row_b["tutorial_day"])

                    selected_days = list(set(selected_days))

                    break
            if not B_continue:
                for i_b, row_b in B_df.iterrows():
                    if check_conflict(current_schedule, row_b):
                        # there is conflict
                        continue
                    else:
                        # append to current_schedule and remove from selection
                        current_schedule.append(row_b)
                        B_df.drop(i_b, inplace=True)
                        selected_days.append(row_b["lecture_day"])
                        selected_days.append(row_b["tutorial_day"])

                        selected_days = list(set(selected_days))
                        break

            C_filtered_df = C_df[
                (~C_df["lecture_day"].isin(selected_days))
                | (~C_df["tutorial_day"].isin(selected_days))
            ]
            C_continue = False
            for i_c, row_c in C_filtered_df.iterrows():
                if check_conflict(current_schedule, row_c):
                    # there is conflict
                    continue
                else:
                    # append to current_schedule and remove from selection
                    current_schedule.append(row_c)
                    C_df.drop(i_c, inplace=True)
                    C_continue = True
                    selected_days.append(row_c["lecture_day"])
                    selected_days.append(row_c["tutorial_day"])

                    selected_days = list(set(selected_days))
                    break
            if not C_continue:
                for i_c, row_c in C_df.iterrows():
                    if check_conflict(current_schedule, row_c):
                        # there is conflict
                        continue
                    else:
                        # append to current_schedule and remove from selection
                        current_schedule.append(row_c)
                        C_df.drop(i_c, inplace=True)
                        selected_days.append(row_c["lecture_day"])
                        selected_days.append(row_c["tutorial_day"])

                        selected_days = list(set(selected_days))
                        #                     print('selected days: ', selected_days)
                        break

            for i_d, row_d in D_df.iterrows():
                if check_conflict(current_schedule, row_d):
                    # there is conflict
                    continue
                else:
                    # append to current_schedule and remove from selection
                    current_schedule.append(row_d)
                    D_df.drop(i_d, inplace=True)
                    break

            solution.append(current_schedule)

    print("solution found!")
    return solution


if __name__ == "__main__":
    solution = main()
    result_df = pd.DataFrame()
    for i, s in enumerate(solution):
        _temp_df = pd.DataFrame(s)[export_cols]
        _temp_df["Combi"] = i
        _temp_df = _temp_df[
            ["Combi", "Module", "Class", "Lecture", "Tutorial"]
        ]
        result_df = pd.concat([result_df, _temp_df])

    result_df.reset_index(inplace=True, drop=True)
