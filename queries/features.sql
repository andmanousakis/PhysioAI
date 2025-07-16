WITH exercise_wrongs AS (
    SELECT
        session_group,
        exercise_name,
        SUM(wrong_repeats) AS total_wrong_repeats
    FROM exercise
    GROUP BY session_group, exercise_name
),
most_incorrect_exercise AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY session_group
            ORDER BY total_wrong_repeats DESC
        ) AS rk
    FROM exercise_wrongs
),
filtered_most_incorrect AS (
    SELECT
        session_group,
        exercise_name AS exercise_with_most_incorrect
    FROM most_incorrect_exercise
    WHERE rk = 1 AND total_wrong_repeats > 0
),
skipped_exercises AS (
    SELECT
        session_group,
        exercise_name,
        exercise_order,
        ROW_NUMBER() OVER (
            PARTITION BY session_group
            ORDER BY exercise_order ASC
        ) AS rk
    FROM exercise
    WHERE leave_exercise IS NOT NULL
),
first_skipped_per_session AS (
    SELECT
        session_group,
        exercise_name AS first_exercise_skipped
    FROM skipped_exercises
    WHERE rk = 1
)

SELECT
    e.session_group,
    ANY_VALUE(e.patient_id) AS patient_id,
    ANY_VALUE(e.patient_name) AS patient_name,
    ANY_VALUE(e.patient_age) AS patient_age,
    ANY_VALUE(e.pain) AS pain,
    ANY_VALUE(e.fatigue) AS fatigue,
    ANY_VALUE(e.therapy_name) AS therapy_name,
    ANY_VALUE(e.session_number) AS session_number,
    ANY_VALUE(e.leave_session) AS leave_session,
    ANY_VALUE(e.quality) AS quality,
    MAX(e.quality_reason_movement_detection) AS quality_reason_movement_detection,
    MAX(e.quality_reason_my_self_personal) AS quality_reason_my_self_personal,
    MAX(e.quality_reason_other) AS quality_reason_other,
    MAX(e.quality_reason_exercises) AS quality_reason_exercises,
    MAX(e.quality_reason_tablet) AS quality_reason_tablet,
    MAX(e.quality_reason_tablet_and_or_motion_trackers) AS quality_reason_tablet_and_or_motion_trackers,
    MAX(e.quality_reason_easy_of_use) AS quality_reason_easy_of_use,
    MAX(e.quality_reason_session_speed) AS quality_reason_session_speed,
    MAX(e.session_is_nok) AS session_is_nok,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'system_problem') AS DOUBLE) AS leave_exercise_system_problem,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'other') AS DOUBLE) AS leave_exercise_other,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'unable_perform') AS DOUBLE) AS leave_exercise_unable_perform,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'pain') AS DOUBLE) AS leave_exercise_pain,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'tired') AS DOUBLE) AS leave_exercise_tired,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'technical_issues') AS DOUBLE) AS leave_exercise_technical_issues,
    CAST(COUNT(*) FILTER (WHERE e.leave_exercise = 'difficulty') AS DOUBLE) AS leave_exercise_difficulty,
    SUM(e.prescribed_repeats) AS prescribed_repeats,
    SUM(e.training_time) AS training_time,
    SUM(e.correct_repeats) * 1.0 / NULLIF(SUM(e.correct_repeats + e.wrong_repeats), 0) AS perc_correct_repeats,
    COUNT(e.exercise_name) AS number_exercises,
    COUNT(DISTINCT e.exercise_name) AS number_of_distinct_exercises,
    f.exercise_with_most_incorrect,
    s.first_exercise_skipped

FROM exercise e
LEFT JOIN filtered_most_incorrect f
    ON e.session_group = f.session_group
LEFT JOIN first_skipped_per_session s
    ON e.session_group = s.session_group
GROUP BY e.session_group, f.exercise_with_most_incorrect, s.first_exercise_skipped;
