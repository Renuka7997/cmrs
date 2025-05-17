
					Construction Material Recommendation System

An intelligent, AI-powered web application designed to recommend optimal construction materials based on user inputs like building type, climate, budget, and more.

Features:

1. user authentication: Role based access for admin and core users

2. AI powered recommendations suggests materials based on the input parameters

3. smart form inputs:
 1. Building type: residential, commercial, industrial 
 2. property type: (e.g., house, penthouse, villa, school building)
 3. Material category (e.g., roofing, flooring, interior, structural)
 4. climate type: hot, humid, cold, temperate
 5. soil type: (e.g, clay, humid, sandy, rocky)
 6. Budget: high, low, medium
 7. location: (e.g., Rural residential , suburban commercial)

4. Admin dashboard: manages the users 


Technologies used:

os: windows only (It can only run in the win)
Frontend: Html, css, javascript 
Backend: Python, Flask
Database: MySQL, SQLAlchemy 
ML: Scikit-learn, Joblib, imbalanced-learn
Libraries: Flask-WTF, Flask-Login, Pandas, NumPy 

Hardware requirements:

processor: i3 or more
Ram: 4gb or more
storage: 1gb 


Software requirements:

os: windows 10 or 11(64 bit)
python version : 3.10
Framework: flask (for backend)
libraries :numpy, pandas, scikit-learn, joblib, flask, flask-wtf, flask-sqlalchemy
IDE/ Editor: VS Code/Pycharm/ Jupyter Notebook
Browser: Google Chrome / Firefox / Edge (for accessing the web app)
Database: MySQL or SQLite (SQLAlchemy used as ORM)
Enivronment: Anaconda Navigator


Requirements
Flask==2.3.3
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
mysqlclient==2.2.4  # Or use PyMySQL if preferred
scikit-learn==1.4.1
pandas==2.2.1
numpy==1.26.4
joblib==1.4.2
Werkzeug==2.3.8
Flask-WTF==1.2.1
WTForms==3.1.2
imbalanced-learn==0.12.0

# cmrs
The construction Material Recommendation System is an intelligent web-based application designed to assist users in selecting the most suitable construction materials based on project-specific parameters. It leverages a trained machine learning model to analyze user inputs and provide accurate recommendation for material types.
