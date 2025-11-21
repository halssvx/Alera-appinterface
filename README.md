Alera – Diabetes Companion

Alera is a calm and friendly diabetes companion created using Python and Streamlit.
It helps users record and view their blood glucose readings, medication, meals, and activity, all within a clear and supportive interface.
The aim is to provide an organised space for daily diabetes management while keeping the experience simple and approachable.

This project is a test run while I explore how to build complete applications, how to design user friendly features, and how to publish and maintain projects on GitHub.
It is an experiment rather than a finished product and it is not intended for medical use.

What Alera offers
Dashboard

A quick view of the latest reading, a graph showing progress over time, a summary of todays entries, and helpful statistics that show patterns at a glance.

Blood glucose logging

A clean form for entering readings with context and optional notes.
Recent readings appear instantly for easy review.

Medication tracking

The user can record medication names, doses, and whether the dose was taken or missed.
Entries include date and time so the full history is always available.

Meals and carbohydrate logging

Meals and snacks can be described clearly and optional carbohydrate information can be added.
This makes it easier to notice links between food and readings.

Activity tracking

The user can record exercise type, duration, and intensity.
This provides useful insight into how activity affects blood glucose patterns.

Insights

Alera gently highlights patterns such as repeated low readings or long stretches of stable results.
These comments are supportive observations and never clinical instructions.

Education and coping support

A space with clear explanations about highs, lows, stress, and daily life with diabetes.
The tone is calm, kind, and free from judgement.

Settings

Users can set their own target ranges and alert thresholds with a reminder that these choices are best made with a healthcare professional.

Purpose of this project

This project exists to support learning.
I created it to practise building structured Python applications, to understand Streamlit in greater depth, and to explore ideas in health technology and design.
It also helps me improve at using Git and GitHub through my account halssvx.

Alera is not a clinical tool.
It is simply a learning project created for exploration, curiosity, and growth.

Ideas for future development

Alera may later include optional features such as prediction models, export features, or more detailed visual summaries.
These ideas are possibilities for future exploration rather than immediate goals.

Running the application

Clone the repository

git clone https://github.com/halssvx/Alera-appinterface
cd alera app


Create a virtual environment

python -m venv venv


Activate it on Windows

venv\Scripts\activate


Install the required libraries

pip install streamlit pandas


Launch the application

streamlit run app py