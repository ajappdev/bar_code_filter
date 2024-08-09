
from datetime import datetime
import pandas as pd
import re
from django.conf import settings

# Declaring django modules
from django.core.paginator import Paginator
import platform
import numpy as np

# Declaring Global Variables

# Get the operating system name
os_name = platform.system()

if os_name == 'Windows':
    BASE_APP_URL = "http://localhost:8000"
else:
    BASE_APP_URL = "hhttps://productmanuals.online"

DATE_SHORT_LOCAL_WITH_DASH: str = '%Y-%m-%d'
SCORE_SIMILARITY = 0.85
SCORE_PASSING = 0.6
SCORE_UNLOCKING = 0.7
QUESTIONS_PER_TOPIC_CERTIFICATION = 1
QUESTIONS_PER_TOPIC_TEST = 1
QUESTIONS_PER_IMPROVEMENT = 5
QUESTIONS_PER_TOPIC = 10
QUESTIONS_PER_MODULE = 7
QUESTIONS_PER_TOPIC_CUSTOM = 3
QUESTIONS_PER_RANDOM_QUIZ = 10
MAX_RANDOM_QUIZZES = 2

PROSPECT_STATUS = [
    ("Prospect", "Prospect"),
    ("Contacted", "Contacted"),
    ("Visited", "Visited"),
    ("Registred", "Registred"),
    ("2+ logins", "2+ logins"),
    ("Premium User", "Premium User"),
    ("Missed Renewal", "Missed Renewal"),
    ("Gone inactive", "Gone inactive"),
    ("Standby", "Standby"),
    ("Registred Standby", "Registred Standby"),
    ("Visited, not interested", "Visited, not interested"),
    ("Not visited, not interested", "Not visited, not interested"),
    ("Not joignable", "Not joignable"),
    ("Terminated", "Terminated")]

PROSPECT_CHANNELS = [
    ("Reddit", "Reddit"),
    ("Linkedin", "Linkedin"),
    ("Twitter", "Twitter"),
    ("Discord", "Discord"),
    ("Facebook Group", "Facebook Group"),
    ("Online Forum", "Online Forum")]

PROSPECT_NOTES_TYPES = [
    ("Bug", "Bug"),
    ("Feedback", "Feedback"),
    ("Prospection Action", "Prospection Action")]

BASE_PREMIUM_PLAN = {
    "price": 9.99,
    "name": "Premium",
    "savings": 0,
    "period": "month",
    "description": "Monthly Subscription",
}

BASE_PREMIUM_PLAN_ANNUAL = {
    "price": 89,
    "name": "Premium_annual",
    "savings": 25,
    "period": "year",
    "description": "Annual Subscription",
}

CURRENT_PLANS = [
    BASE_PREMIUM_PLAN,
    BASE_PREMIUM_PLAN_ANNUAL]

PRODUCT_NAME = 'ProductManuals'

BBC_LIST = ['alae1ajbar@gmail.com', 'ibnouratib.pro@gmail.com']

def is_hyperlink(s):
    # Regular expression for a simple URL check
    url_pattern = re.compile(
        r'^(?:http|https):\/\/'  # http or https
        r'(?:www\.)?'  # optional www
        r'[a-zA-Z0-9\-\.]+'  # domain name
        r'\.[a-zA-Z]{2,}'  # top-level domain
        r'(?:\/[^\s]*)?$'  # optional path
    )
    return url_pattern.match(s) is not None

def calculate_pass_rate(df: pd.DataFrame):
    """
    This function, given a list of answered questions, returns a tuple like
    this (total_number_questions, nb_answered_right, nb_answered_false, pass
    rate)
    """
    total_number_questions = len(df)
    nb_answered_right = df['answered_right'].sum()
    nb_answered_false = total_number_questions - nb_answered_right
    if total_number_questions:
        pass_rate = (nb_answered_right / total_number_questions) * 100
    else:
        pass_rate = None
        
    # Create the tuple
    result_tuple = (
        total_number_questions,
        nb_answered_right,
        nb_answered_false,
        pass_rate)

    return result_tuple


def pagination(page: int, nbr_pag: int, liste_obj):
    paginator = Paginator(liste_obj, nbr_pag)
    obj = paginator.get_page(page)
    return obj


def shorten_number(number: float):
    if number >= 1000000:
        return number/1000000, "M"
    elif number >= 1000:
        return number/1000, "K"
    else:
        return number, ""
