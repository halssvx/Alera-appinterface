# Alera.ai.appinterface

Alera – Diabetes Companion

Alera is a simple and friendly diabetes companion created using Python and Streamlit.
It allows users to record, view, and understand their daily blood glucose readings, medication, meals, and activity.
Everything is presented in an easy to read dashboard with gentle guidance and supportive explanations.

This project is a test run while I explore and learn how to build complete applications, structure code, and publish projects on GitHub. It is not a finished product and it is not intended for clinical use. It is simply part of my journey as I learn and experiment.

Key features

Dashboard
The dashboard shows the latest blood glucose reading, a trend chart, a summary of todays entries, and an overview of readings that are within or outside the target range.

Blood glucose logging
Users can record their blood glucose levels, select the context such as before a meal or after exercise, and add notes. Recent entries are displayed clearly.

Medication tracking
Users can record medication names, doses, and whether the dose was taken or missed. Entries include the date and time.

Meals and carbohydrate logging
Users can describe a meal or snack and record optional carbohydrate information. Meal history is easy to view.

Activity tracking
Users can log physical activity including the type of activity, duration, and intensity.

Insights
The app provides gentle and supportive observations such as repeated low readings or periods of consistent control. These are not clinical instructions. They are simple patterns to think about.

Education and coping support
There is a small collection of calm explanations about highs, lows, stress, and daily management. The language is simple and non judgemental.

Settings
Users can set their preferred target range and alert thresholds with guidance that these should ideally be set with a healthcare professional.

Purpose of this project

This project is a learning exercise.
I created it to practise building more complete Python applications and to understand Streamlit in more depth.
It also helps me explore ideas in health technology and design, and to learn how to push full projects to GitHub confidently.
It is not a medical tool. It is only for education and experimentation.

Possible future ideas

Alera might later include optional features such as prediction models, export options, or more advanced graphs. None of these are required at this stage. They are simply ideas to explore as I continue learning.

How to run the app

Clone the repository

git clone https github com YOUR USERNAME alera app git
cd alera app


Create a virtual environment

python -m venv venv


Activate it on Windows

venv\Scripts\activate


Install the required libraries

pip install streamlit pandas


Run the application

streamlit run app py

A note from the creator

Alera is a personal learning project.
It allows me to try new ideas, test approaches, and improve my coding and design skills.
It is not perfect and it does not need to be.
It is a safe space for growth and experimentation.