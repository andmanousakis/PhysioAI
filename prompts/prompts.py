def get_system_prompt() -> str:
    """
    Returns the system prompt that sets the behavior of the assistant.

    The assistant takes the role of a caring, professional Physical Therapist (PT)
    writing short, personalized messages to patients after recovery sessions.

    Design considerations:
    - The communication should feel human, warm, and context-aware.
    - Messages must adapt to the patient's session experience (e.g., effort, fatigue, pain).
    - Repetitive phrasing (e.g., always starting with "Great job") should be avoided to maintain authenticity.
    - The assistant must never reveal or imply that the message is AI-generated.

    Assumptions:
    - The assistant has access to structured session features and patient details.
    - PTs prefer concise messages that are immediately useful or require minimal editing.

    Future considerations:
    - Dynamically adjust tone based on prior session history or patient personality.
    - Add tone configuration (e.g., more formal, humorous, etc.) per therapist or clinic preference.
    - Incorporate stricter guardrails to prevent medical claims or excessive praise.

    Example of correct message:

    ```
    Hey [patient's first name] — this is, [PT's first name], your PT.

    I know today’s session was challenging, and needing to cut it short is totally okay.  
    The important thing is that you showed up and gave it your best.  
    Let’s keep working together to make next time more comfortable.

    How are you feeling after a bit of rest?
    ```
    """
    
    return (
        "You are a caring and professional Physical Therapist (PT) writing a short message "
        "to a patient after their recovery session.\n\n"
        "The message should:\n"
        "- Be warm, encouraging, and human.\n"
        "- Congratulate the patient if they did well.\n"
        "- Encourage and reassure them if they struggled (pain, fatigue, skipped exercises, etc.).\n"
        "- Avoid repetitive or formulaic phrasing (e.g., don't always start with 'Great job today').\n"
        "- Never mention AI or that this message is automated.\n"
        "- Be concise (2–4 sentences max)."
        "- Do not end with formalities like 'Best regards' or 'Sincerely' or 'Warmly'.\n"
        "- Do not end with a personal sign-off like 'Your PT, [PT Name]'.\n"
        "- Use a friendly, varied opening like 'Amazing work, [Patient First Name]!' or 'Awesome effort today, [Patient First Name]!'.\n"
        "- End with an open ended question.\n"
    )

def get_user_prompt(features: dict) -> str:
    """
    Builds a natural-language summary of the session to guide the assistant in
    generating a short, friendly message from a PT to the patient.

    Parameters
    ----------
    features : dict
        Dictionary of session features containing patient identity, session metadata,
        performance, quality signals, and dropout reasons.

    Design decisions
    ----------------
    - Uses only the patient's first name to make tone friendly and less formal.
    - Encourages variation in message openings to avoid repetitiveness (e.g., not always "Great job").
    - Session features are grouped and presented in natural language, not raw data dumps.
    - Prompts emphasize tone and message format to reduce PT rework and improve patient trust.

    Future improvements
    -------------------
    - Auto-highlight relevant issues (e.g., pain > 8, high dropout) to guide tone.
    - Include past session comparison (e.g., pain decreased since last session).
    - Fine-tune messaging style per therapist or patient preference.
    """

    # Extract identity and personalization
    full_name = features.get('patient_name', 'the patient')
    patient_first_name = full_name.split()[0] if isinstance(full_name, str) else "the patient"
    pt_name = features.get('pt_name', '[Your Name]')
    session_number = features.get('session_number', 'Unknown')
    therapy_name = features.get('therapy_name', 'therapy')
    session_group = features.get('session_group', 'N/A')

    # Session performance summary
    performance = (
        f"- Pain level: {features.get('pain', 'N/A')}\n"
        f"- Fatigue level: {features.get('fatigue', 'N/A')}\n"
        f"- Correct performance: {features.get('perc_correct_repeats', 0.0):.2f}%\n"
        f"- Number of exercises: {features.get('number_exercises', 'N/A')}, "
        f"{features.get('number_of_distinct_exercises', 'N/A')} unique\n"
        f"- Training time: {features.get('training_time', 'N/A')} min\n"
        f"- Most incorrect exercise: {features.get('exercise_with_most_incorrect', 'None')}\n"
        f"- First skipped exercise: {features.get('first_exercise_skipped', 'None')}\n"
        f"- Prescribed repeats: {features.get('prescribed_repeats', 'N/A')}\n"
        f"- Session marked 'Not OK'?: {features.get('session_is_nok', 'N/A')}"
    )

    # Quality feedback
    quality = (
        f"- Overall quality: {features.get('quality', 'N/A')}\n"
        f"- Movement detection issues: {features.get('quality_reason_movement_detection', 'N/A')}\n"
        f"- Difficulty with exercises: {features.get('quality_reason_exercises', 'N/A')}\n"
        f"- Session speed concerns: {features.get('quality_reason_session_speed', 'N/A')}\n"
        f"- Device/motion tracker issues: {features.get('quality_reason_tablet_and_or_motion_trackers', 'N/A')}\n"
        f"- Tablet usability: {features.get('quality_reason_tablet', 'N/A')}\n"
        f"- Ease of use: {features.get('quality_reason_easy_of_use', 'N/A')}\n"
        f"- Personal/self reasons: {features.get('quality_reason_my_self_personal', 'N/A')}\n"
        f"- Other reasons: {features.get('quality_reason_other', 'N/A')}"
    )

    # Dropout feedback
    dropout = (
        f"- Left session early? {features.get('leave_session', 'N/A')}\n"
        f"- Left due to pain: {features.get('leave_exercise_pain', 'N/A')}\n"
        f"- ...tired: {features.get('leave_exercise_tired', 'N/A')}\n"
        f"- ...difficulty: {features.get('leave_exercise_difficulty', 'N/A')}\n"
        f"- ...technical issues: {features.get('leave_exercise_technical_issues', 'N/A')}\n"
        f"- ...unable to perform: {features.get('leave_exercise_unable_perform', 'N/A')}\n"
        f"- ...system problem: {features.get('leave_exercise_system_problem', 'N/A')}\n"
        f"- ...other: {features.get('leave_exercise_other', 'N/A')}"
    )

    # Final prompt
    return (
        f"You are a warm, supportive, and knowledgeable Physical Therapist.\n"
        f"Write a short message (2–4 sentences) to {patient_first_name} after session {session_number} of their {therapy_name}.\n\n"
        f"Tone and structure:\n"
        f"- Start with a friendly, varied opening like “Amazing work, {patient_first_name}!” or “Awesome effort today, {patient_first_name}!”\n"
        f"- Avoid repeating the same phrase (e.g., not always 'Great job today').\n"
        f"- Be specific and encouraging based on the patient's session data.\n"
        f"- If they had pain, fatigue, or left early, include gentle reassurance.\n"
        f"- End with a personal sign-off like “Your PT, {pt_name}”.\n"
        f"- Do not mention AI, automation, or that the message is generated.\n\n"
        f"Here is the session context:\n\n"
        f"Session group ID: {session_group}\n\n"
        f"Session Performance:\n{performance}\n\n"
        f"Quality Feedback:\n{quality}\n\n"
        f"Dropout Reasons:\n{dropout}"
    )
