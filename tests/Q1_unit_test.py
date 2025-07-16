import pandas as pd
import pandas.testing as pdt
from pathlib import Path

def test_features_match():
    columns_to_check = [
        "session_group",
        "patient_id",
        "patient_name",
        "patient_age",
        "pain",
        "fatigue",
        "therapy_name",
        "session_number",
        "leave_session",
        "quality",
        "quality_reason_movement_detection",
        "quality_reason_my_self_personal",
        "quality_reason_other",
        "quality_reason_exercises",
        "quality_reason_tablet",
        "quality_reason_tablet_and_or_motion_trackers",
        "quality_reason_easy_of_use",
        "quality_reason_session_speed",
        "session_is_nok",
        "leave_exercise_system_problem",
        "leave_exercise_other",
        "leave_exercise_unable_perform",
        "leave_exercise_pain",
        "leave_exercise_tired",
        "leave_exercise_technical_issues",
        "leave_exercise_difficulty",
        "prescribed_repeats", 
        "training_time",
        "perc_correct_repeats",
        "number_exercises",
        "number_of_distinct_exercises",
        "exercise_with_most_incorrect",
        "first_exercise_skipped",
    ]

    path_expected = Path("data/features_expected.parquet")
    path_actual = Path("data/features.parquet")

    df_expected = pd.read_parquet(path_expected)
    df_actual = pd.read_parquet(path_actual)

    df_expected = df_expected.sort_values("session_group").reset_index(drop=True)
    df_actual = df_actual.sort_values("session_group").reset_index(drop=True)

    # Compare all columns except 'exercise_with_most_incorrect'. According to README.md, this column could have many possible values.
    base_cols = [col for col in columns_to_check if col != "exercise_with_most_incorrect"]
    pdt.assert_frame_equal(
        df_actual[base_cols],
        df_expected[base_cols],
        check_like=True,
        check_dtype=True
    )

    # Custom comparison for 'exercise_with_most_incorrect'.
    df_exercise = pd.read_parquet("data/exercise_results.parquet")

    # Compute total wrong_repeats per session_group and exercise.
    agg = (
        df_exercise
        .groupby(["session_group", "exercise_name"])["wrong_repeats"]
        .sum()
        .reset_index()
    )

    # Identify sessions where all exercises had 0 wrong repeats.
    total_wrong = agg.groupby("session_group")["wrong_repeats"].sum().reset_index()
    zero_wrong_sessions = set(total_wrong[total_wrong["wrong_repeats"] == 0]["session_group"])

    # Get max wrong_repeats per session_group.
    max_wrong = agg.groupby("session_group")["wrong_repeats"].max().reset_index()
    candidates = pd.merge(agg, max_wrong, on=["session_group", "wrong_repeats"])

    # Convert to mapping: session_group → set of valid exercise names.
    session_to_valid = (
        candidates
        .groupby("session_group")["exercise_name"]
        .apply(set)
        .to_dict()
    )

    mismatches = []
    for i, row in df_actual.iterrows():
        session = row["session_group"]
        actual = row["exercise_with_most_incorrect"]

        if session in zero_wrong_sessions:
            if pd.isna(actual):
                continue  # Correct: no incorrects → NULL expected
            else:
                mismatches.append((session, actual, "NULL (all 0s expected)"))
        else:
            valid_set = session_to_valid.get(session, set())
            if actual not in valid_set:
                mismatches.append((session, actual, valid_set))

    if mismatches:
        print("Mismatches in 'exercise_with_most_incorrect':")
        for session, actual, expected in mismatches[:10]:
            print(f"  session_group: {session}, got: {actual}, expected: {expected}")
        raise AssertionError(f"{len(mismatches)} mismatched `exercise_with_most_incorrect` values.")
