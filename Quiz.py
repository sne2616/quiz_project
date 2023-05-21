import altair as alt
import requests
import re
import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import csv




m = st.markdown("""
<style>
div.stButton > button:first-child{
    background-color: ##ff99ff;
    color:#ffffff;
    padding: 10px 20px; border-radius: 5px;
}
div.stButton > button:hover {
    background-color:#0000CD;
    color:#000000;
    padding: 20px 30px 20px; border-radius: 5px;
}
</style>""",unsafe_allow_html=True)


quiz = {
    "**Question 1: What is a correct syntax to output 'Hello World' in Python?**": ["Print('Hello World')", "echo 'Hello World'", "p('Hello World')", "echo Hello World"],
    "**Question 2: How do you insert COMMENTTS in Python code?**": ["/*This is a comment*/", "#This is a comment", "//This is a comment"],
    "**Question 3: Which one is NOT a legal variable name?**": ["Myvar", "_myvar", "my-var", "my_var"],
    "**Question 4: How do you create a variable with the numeric value 5?**": ["Both the other answers are correct", "x=5", "x=int(5)"],
    "**Question 5: What is the correct file extension for python files?**": [".py", ".pt", ".pyt", ".pyth"],
    "**Question 6: How do you create a variable with the floating number 2.8?**": ["x=2.8","Both the other answers are correct","x=float(2.8)"],
    "**Question 7: What is the correct syntax to output the type of a variable or object in Python?**":["print(type of (x))","print(type of x)","print(type(x))","print type of x"],
    "**Question 8: What is the correct way to create a function in Python?**": ["function my function():","create my Function():","def my Function():"],
    "**Question 9: In Python 'Hello' is the same as double quotes Hello?**": ["TRUE","FALSE"],
    "**Question 10: What is a correct syntax to return the first charcater in a string?**": ["x='Hello'.sub(0,1)","x=sub('Hello',0,1)","x='Hello[0]"],
    "**Question 11: Which method can be used to remove any whitespace from both the beginning and the end of string?**": ["strip()","trim()","len()","ptrim()"],
    "**Question 12: Which method can be used to return a string in upper case letters?**": ["upper()","toUpperCase()","upperCase()","uppercase()"],
    "**Question 13: Which method can be used to replace parts of a string?**": ["replace()","replace string()","repl()","switch()"],
    "**Question 14: Which operator is used to multiply numbers?**": ["#","*","%","x"],
    "**Question 15: Which operator can be used to compare two values?**": ["><","=","<>","=="],
    "**Question 16: Which of these collections defines a LIST?**": ["('apple','banana','cherry')",{'apple','banana','cherry'},['apple','banana','cherry'],"{'name':'apple','color':'green'}"],
    "**Question 17: Which of these collections defines a TUPLE?**": ["('apple','banana','cherry')",{'apple','banana','cherry'},['apple','banana','cherry'],"{'name':'apple','color':'green'}"],
    "**Question 18: Which of these collections defines a SET?**": ["('apple','banana','cherry')",{'apple','banana','cherry'},['apple','banana','cherry'],"{'name':'apple','color':'green'}"],
    "**Question 19: Which of these collections defines a DICTIONARY?**": ["('apple','banana','cherry')",{'apple','banana','cherry'},['apple','banana','cherry'],"{'name':'apple','color':'green'}"],
    "**Question 20: Which collection is ordered, changeable,and allows duplicate members?**": ["SET","DICTIONARY","TUPLE","LIST"],
    "**Question 21: Which collection does not allow duplicate members?**": ["TUPLE","LIST","SET"],
    "**Question 22: How do you start writing an if statement in Python?**": ["if x>y:","if x>y then","if(x>y)"],
    "**Question 23: How do you start writing a while loop in Python?**": ["while x>y","while x>y{","x>y while{","while(x>y)"],
    "**Question 24: How do you start writing a for loop in Python?**": ["for x>y","for x in y:","for each x in y"],
    "**Question 25: Which statement is used to stop a loop?**": ["stop","exit","return","break"]
}



filename = 'quiz.csv'

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(quiz)

print(f'CSV file "{filename}" has been created.')


# Define the answers to the quiz questions
answers = ["Print('Hello World')", "#This is a comment", "my-var", "Both the other answers are correct", ".py","Both the other answers are correct","print(type of x)","def my Function():","True","x=sub('Hello',0,1)","strip()","upper()","switch()","*","==","['apple','banana','cherry']","('apple','banana','cherry')","{'apple','banana','cherry'}","{'name':'apple','color':'green'}","LIST","SET","if x>y:","while x>y","for x in y:","break"]

# Define a function to calculate the user's score
def calculate_score(user_answers):
    score = 0
    for i in range(len(user_answers)):
        if user_answers[i] == answers[i]:
            score += 1
    return score

# Define the app pages
app_pages = ["Home", "Quiz", "Result"]

# Define the functions to render each page
def render_home_page():
    st.title("Welcome to the Python Quiz!")
    st.markdown("This is a simple quiz to test your knowledge of Python.")
    st.markdown("The test contains **25** questions and there is no time limit.")
    image = Image.open('python.png')
    st.image(image, caption='PYTHON')
    st.subheader('Click [here](https://www.tutorialspoint.com/python/index.htm) to visit the website.')
    st.subheader(" NOTE: If you want to know anything about PYTHON then click on the link above.")
    st.header("Click on the Quiz button to start the quiz.")

    if st.button("Start Quiz"):
        st.session_state["page"] = "quiz"


def render_quiz_page():
    st.title("The Python Quiz")
    st.write("**The quiz contains 25 question. Select one of the options and click on the Submit button to check your answer.**")
    
    user_answers = []
    st.markdown("**Answer the following questions:**")
    for i, (question, options) in enumerate(quiz.items()):
        user_answer = st.selectbox(f"{i+1}. {question}", options)
        user_answers.append(user_answer)
    score = calculate_score(user_answers)
    st.write(f"You scored {score} out of {len(quiz)}")
    st.session_state["score"] = score
    
    if st.button("Submit Answers"):
    
        st.success("Your answers have been submitted!")
        st.session_state["page"] = "result"

def render_result_page():
    st.title("Quiz Results")
    st.subheader(f"**Your final score is: {st.session_state['score']} out of {len(quiz)}**")
     # Calculate incorrect answers
    incorrect_answers = len(quiz) - st.session_state["score"]

    # Create data for the chart
    labels = ["Correct Answers", "Incorrect Answers"]
    values = [st.session_state["score"], incorrect_answers]
    colors = ["green", "red"]

    # Plot the chart
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)

    # Customize the chart
    ax.set_ylabel("Number of Answers")
    ax.set_title("Quiz Results")

    # Display the chart
    st.pyplot(fig)

    # Show the correct answers
    st.subheader("**Check your answers**")
    for i, (question, options) in enumerate(quiz.items()):
        st.write(f"{i+1}. {question}")
        correct_answer = answers[i]
        st.write(f"Correct answer: {correct_answer}")
        st.write("---")
    st.subheader("**Check your answers**")
    for i, (question, options) in enumerate(quiz.items()):
        st.write(f"{i+1}. {question}")
        correct_answer = answers[i]
        st.write(f"Correct answer: {correct_answer}")
        st.write("---")
    
    if st.button("Try Again"):
        st.info("**Thank You for Participating!!!!**")
        st.session_state["page"] = "home"
        
        

        
# Define the app layout
def app():
    st.sidebar.title("PYTHON")
    selected_page = st.sidebar.selectbox("Select to", app_pages)

    # Render the selected page
    if selected_page == "Home":
        render_home_page()
    elif selected_page == "Quiz":
        render_quiz_page()
    elif selected_page == "Result":
        render_result_page()








# Run the app
app()
