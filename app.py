import streamlit as st
import matplotlib.pyplot as plt

# ------------------------------
# CONFIGURATION
# ------------------------------
NUM_SUBJECTS = 5
QUIZ_MARK = 1
ASSIGNMENT_MARK = 12
ENDTERM_MARK = 70

# ------------------------------
# GRADE FUNCTION
# ------------------------------
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+", 10
    elif percentage >= 80:
        return "A", 9
    elif percentage >= 70:
        return "B", 8
    elif percentage >= 60:
        return "C", 7
    elif percentage >= 50:
        return "D", 6
    elif percentage >= 40:
        return "E", 5
    else:
        return "F", 0

# ------------------------------
# WELCOME SECTION
# ------------------------------
st.title("🎓 Student Academic Progress Tracker")

st.markdown("""
### 📘 About This Project
This application tracks a student's academic progress across **5 subjects**  
based on **quizzes, assignments, and optional end-term examination**.

It provides:
- Subject-wise analysis
- Progress visualization
- Final grading & feedback

Designed for **students and teachers** with no technical background.
""")

st.divider()

# ------------------------------
# STUDENT DETAILS
# ------------------------------
st.header("👤 Student Details")

student_name = st.text_input("Student Name")
roll_no = st.text_input("Roll Number")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

st.divider()

# ------------------------------
# SUBJECT DATA INPUT
# ------------------------------
subjects = {}

st.header("📚 Subject-wise Assessment Entry")

for i in range(NUM_SUBJECTS):
    st.subheader(f"Subject {i+1}")
    subject_name = st.text_input(f"Subject {i+1} Name", key=f"sub{i}")

    col1, col2, col3 = st.columns(3)

    quizzes = []
    with col1:
        st.markdown("**Quizzes**")
        for q in range(4):
            quizzes.append(
                st.selectbox(
                    f"Quiz {q+1} (0/1)",
                    [0, 1],
                    key=f"s{i}q{q}"
                )
            )

        quiz5 = st.selectbox("Quiz 5 (Optional)", ["Not Conducted", 0, 1], key=f"s{i}q5")
        quiz6 = st.selectbox("Quiz 6 (Optional)", ["Not Conducted", 0, 1], key=f"s{i}q6")

    with col2:
        st.markdown("**Assignments**")
        assignment1 = st.slider("Assignment 1 (0–12)", 0, 12, key=f"s{i}a1")
        assignment2 = st.slider("Assignment 2 (Optional)", 0, 12, key=f"s{i}a2")

    with col3:
        st.markdown("**Endterm**")
        endterm = st.slider("Endterm (Optional)", 0, 70, key=f"s{i}end")

    subjects[subject_name] = {
        "quizzes": quizzes,
        "quiz5": quiz5,
        "quiz6": quiz6,
        "assignment1": assignment1,
        "assignment2": assignment2,
        "endterm": endterm
    }

st.divider()

# ------------------------------
# PROCESS & ANALYZE
# ------------------------------
if st.button("📊 Generate Report"):

    st.header("📈 Subject-wise Analysis")

    semester_total = 0
    semester_max = 0

    for subject, data in subjects.items():
        quiz_total = sum(data["quizzes"])

        quiz_max = 4
        if data["quiz5"] != "Not Conducted":
            quiz_total += data["quiz5"]
            quiz_max += 1
        if data["quiz6"] != "Not Conducted":
            quiz_total += data["quiz6"]
            quiz_max += 1

        assignment_total = data["assignment1"]
        assignment_max = 12

        if data["assignment2"] > 0:
            assignment_total += data["assignment2"]
            assignment_max += 12

        total = quiz_total + assignment_total
        max_total = quiz_max + assignment_max

        if data["endterm"] > 0:
            total += data["endterm"]
            max_total += 70

        percentage = (total / max_total) * 100

        semester_total += total
        semester_max += max_total

        grade, points = calculate_grade(percentage)

        st.markdown(f"""
        **{subject}**
        - Total: {total}/{max_total}
        - Percentage: {percentage:.2f}%
        - Grade: **{grade}**
        """)

        # Progress graph
        plt.figure()
        plt.bar(["Quizzes", "Assignments", "Endterm"],
                [quiz_total, assignment_total, data["endterm"]])
        plt.title(subject)
        st.pyplot(plt)
        plt.clf()

    st.divider()

    # ------------------------------
    # FINAL RESULT
    # ------------------------------
    final_percentage = (semester_total / semester_max) * 100
    final_grade, final_points = calculate_grade(final_percentage)

    st.header("🏁 Final Result")

    st.markdown(f"""
    **Student:** {student_name}  
    **Roll No:** {roll_no}  
    **Email:** {email}  

    **Semester Percentage:** {final_percentage:.2f}%  
    **Final Grade:** **{final_grade}**  
    **Grade Points:** {final_points}
    """)

    # Feedback message
    if final_points >= 8:
        st.success("🌟 Excellent work! Keep maintaining this consistency.")
    elif final_points >= 6:
        st.info("👍 Good performance. A little more effort can take you higher!")
    else:
        st.warning("📘 Don't be discouraged. Focus on fundamentals and practice regularly.")
