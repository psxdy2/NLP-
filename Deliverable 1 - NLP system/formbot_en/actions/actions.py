'''
Time @： 25/11/2021
Author @: by Dongchen Yao- psxdy2
'''

from typing import Dict, Text, Any, List, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import re
from rasa_sdk.events import SlotSet, AllSlotsReset,Restarted
from rasa_sdk import Action
import random
import requests
from actions.utils.coins import CoinDataManager
from actions.utils.request import get

class ClearflightFormSlot(Action):
    """Clear all word slot slots from the previous round of scheduled tickets"""

    def name(self) -> Text:
        return "action_clear_flight_form_slots"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        clear_slots = domain.get("forms", {})["flight_form"].keys()
        slots_data = domain.get("slots")
        return [SlotSet(slot_name, slots_data.get(slot_name)['initial_value']) for slot_name in clear_slots]

class ValidateflightForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_flight_form"

    @staticmethod
    def departure_db() -> List[Text]:
        """Database of supported departures."""

        return ['london', 'taipei', 'new york', 'singapore', 'sydney', 'beijing', 'dubai', 'paris', 'tokyo', 'los angeles', 'mumbai', 'toronto', 'shanghai', 'amsterdam', 'milan', 'frankfurt', 'mexico city', 'sao paulo', 'chicago', 'kuala lumpur', 'madrid', 'moscow', 'brussels', 'warsaw', 'seoul', 'johannesburg', 'zurich', 'melbourne', 'istanbul', 'bangkok', 'stockholm', 'vienna', 'guangzhou', 'hongkong', 'buenos aires', 'san francisco', 'montreal', 'munich', 'delhi', 'san diego', 'boston', 'manila', 'shenzhen', 'riyadh', 'lisbon', 'bangalore', 'dallas', 'bogota', 'miami', 'rome', 'hamburger', 'houston', 'berlin', 'chengdu', 'tel aviv', 'barcelona', 'doha', 'lima', 'vancouver', 'brisbane', 'chongqing', 'cairo', 'auckland', 'ho chi minh city', 'osaka', 'cambridge']

    @staticmethod
    def return_db() -> List[Text]:
        """Database of supported returns."""

        return [
    "one-way",
    "round-trip",
    "multi-city",
    "single"

        ]

    # Departure word slot verification
    def validate_departure(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate departure value."""
        print('departure：',value)
        # Determine if the departure lowercase is in the self.departure_db list

        if value.lower() in self.departure_db():
            return {"departure": value}
        # If not, give a prompt and let the user enter the departure point again
        else:
            dispatcher.utter_message(template="utter_wrong_departure")
            return {"departure": None}

    # Destination word slot validation
    def validate_destination(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate departure value."""
        print('destination：',value)

        # Determine if the destination lowercase is in the self.departure_db list
        if value.lower() in self.departure_db():
            return {"destination": value}
        # If not, give a prompt and let the user enter the destination again
        else:
            dispatcher.utter_message(template="utter_wrong_destination")
            return {"destination": None}

    # Return method word slot verification
    def validate_return(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate return value."""
        print('one-way：',value)

        # Determine if the return method is in self.return_db
        if value in self.return_db():
            return {"return": value}
        # If not, give a prompt and let the user enter the return method again
        else:
            dispatcher.utter_message(template="utter_wrong_return")
            # validation failed, set slot to None
            return {"return": None}

    # Time word slot validation
    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        print('time：',value)
        try:
            if isinstance(value,list): # If it is a list, take the first value of the list
                return {"time": value[0]}
            else:
                return {"time":value}# If it is a string, it takes itself
        except Exception as e:# If an exception is found, remind the user to enter the time again
            dispatcher.utter_message(template="utter_wrong_time")
            # validation failed, set slot to None
            return {"time": None}

########################################################################
# The function of self-introduction，Store the user's name

class ActionUserIntroduce(Action):

    def name(self) -> Text:
        return "action_user_introduce"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_in = tracker.latest_message.get("text")
        # Take the last word of the user's answer
        user_introduce_name = user_in.split(' ')[-1]
        print('name：',user_introduce_name)
        dispatcher.utter_message('Hello, '+user_introduce_name+', you can ask me any questions.')

########################################################################
#search_weather
#change QUERY_KEY
QUERY_KEY = "b1f2c02aa85b4077bdbdf84f5ab60b2d"

CITY_LOOKUP_URL = "https://geoapi.qweather.com/v2/city/lookup"
WEATHER_URL = "https://devapi.qweather.com/v7/weather/now"


class ActionQueryWeather(Action):

    def name(self) -> Text:
        return "action_query_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # User input information
        user_in = tracker.latest_message.get("text")
        # Get City
        try:
            city = tracker.latest_message.get("entities")[0]["value"]
        except Exception as e:
            city = None

        # If no city is acquired, the city is not in the corpus
        if city == None:
            dispatcher.utter_message("City type is not in the database, please try again~")
        # If there is a city, the interface gets the city id and gets the city weather
        else:
            text = self.get_weather(self.get_location_id(city))
            print(text)
            dispatcher.utter_message(text=text)
        # Clean up city word slots
        return [SlotSet("departure",None)]
        return []

    # Get city id
    @staticmethod
    def get_location_id(city):
        # params = {"location": city, "key": QUERY_KEY}
        params = {"location": city, "key": QUERY_KEY, "lang": 'en'}
        return requests.get(CITY_LOOKUP_URL, params=params).json()["location"][0]["id"]

    # Get weather by city id
    @staticmethod
    def get_weather(location_id):
        # params = {"location": location_id, "key": QUERY_KEY}
        params = {"location": location_id, "key": QUERY_KEY, "lang": 'en'}
        res = requests.get(WEATHER_URL, params=params).json()["now"]
        print('status:',requests.get(WEATHER_URL, params=params).json())
        return f"{res['text']}\nwindDir: {res['windDir']}\ntemp: {res['temp']}\nfeelsLike：{res['feelsLike']}"

########################################################################################
# search_coin
class CoinSearchAction(Action):
    def name(self) -> Text:
        return "action_search_coin_history"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        img_msg = await CoinDataManager().get_img()
        dispatcher.utter_message(image=img_msg)
        return []
##############################################################################
#game playing
import random
import os
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
# Load pretrained model for sentence embeddings
model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')
# Fetch the middle-answer in database

# Get riddles and answers from the corpus
query = [line.strip('\n') for line in open(os.getcwd()+'/actions/data/game_data/query.txt')]
respond = [line.strip('\n') for line in open(os.getcwd()+'/actions/data/game_data/response.txt')]
assert len(query)==len(respond), 'match error'

# save the middle-answer in a dictionary
q_r_dict = {}
for i in range(len(query)):
    q_r_dict[query[i]] = respond[i]

# randomly choose a middle question for user
def random_question():
    return random.choice(query)

# Randomly selected riddles for users to guess
class AskRiddleAction(Action):
    def name(self) -> Text:
        return "action_ask_riddle"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # One randomly selected riddle
        middle_question = random_question()
        # Give the riddle
        dispatcher.utter_message(middle_question)
        # Insert the riddles into the problem slots to prepare the answers for the next round
        return [SlotSet("problem",middle_question)]

# Determine if the user is answering correctly
class RiddleResultAction(Action):
    def name(self) -> Text:
        return "action_riddle_result"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the riddle for problem word slot
        middle_question = tracker.get_slot('problem')
        print('last_problem：',middle_question)
        # Answers to user riddles
        user_answer = tracker.latest_message.get("text")
        # The correct answer
        right_answer = q_r_dict[middle_question]
        print('right_answer:',right_answer)
        print('user_answer:',user_answer)
        # Calculate the similarity between the user's answer and the correct answer
        cos_sim = 1 - cosine(model.encode(right_answer), model.encode(user_answer))
        print('cos_sim：',cos_sim)

        # If the similarity is greater than 0.6, the answer is correct
        if cos_sim >= 0.6:
        #if right_answer == user_answer:
            dispatcher.utter_message('Correct!')   # if the user's answer is similar to the standard answer, then he answers correctly
        # Otherwise the answer fails
        else:
            dispatcher.utter_message("No, the correct answer is {}".format(right_answer))
        # Clean up word slots
        return [SlotSet("problem",None)]

# Conversation restart
class ActionRestart(Action):
    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]  
