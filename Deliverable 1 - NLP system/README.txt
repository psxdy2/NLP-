###########################################################################
##rasa instruction document##

I. Model startup commands

Open terminal to switch virtual environment：conda activate myrasa
////////////////////////
Rasa starts the command:
cd Dongchen Yao-psxdy2-HAI-CW/Deliverable 1 - NLP system/formbot_en

rasa run --cors "*" --enable-api -vv --log-file formbot.log -p 5005&

rasa run actions -p 5055&
////////////////////////////
Front-end startup commands:

cd Dongchen Yao-psxdy2-HAI-CW/Deliverable 1 - NLP system/rasa_bot_front

nvm use  16.13.0

Go to the specified front-end directory and run the command：npm run start 

########################################### #################### 
Some orders from rasa
1. rasa modifications to add corpus and answers.
Add corpus: add corpus in data/nlu.yml file.
(2), modify the corresponding answer: find the purpose of the answer that needs to be modified from nlu.yml, go to the corresponding in domain.yml, modify the answer

2, rasa to increase the intent (single round, more complex multi-round, refer to the official website)
        a. In data/nlu.yml add new intentions and corresponding materials
        b.add new intent and corresponding pipeline in data/rules.yml (single round)
        c. Newly add the name of the answer in domain.yml and the corresponding answer to the answer

3. rasa training commands.
1、First backup the tarball in models
2, to the domain to establish a directory, the implementation of rasa train
If no error is reported, the model will be modified to generate the latest tarball after the training.
If the model is wrong, modify the model according to the log

###############################################################
Intelligent robot design process
1、greet
Q：Hi
A：Hello, how may I help?

2、thankyou
Q：thank you
A：You are welcome :)

3、bot_challenge
Q：are you a bot?
A：I am a bot, powered by Rasa.

4、user_introduce
Q：Hello, i am a bot, powered by Rasa. Can you tell me your name~
A：My name is Aaron
Q：Hello, Aaron, you can ask me any questions.

5、request_flight
Q1：
A：I want to book a flight
Q：Can tell me the place of departure?"
A：London
Q：Can tell me the place of destination?" 
A：Paris
Q：Would that be a one-way trip or a round-trip flight?
A：one-way
Q：When were you thinking of going?
A：January 1
Q：All done!
A：I am going to run a flight search using the following parameters:\n
             - departure: London\n
             - destination: Paris\n
             - one-way/round-trip: one-way\n
             - time: January 1

Q2：
A：I would like to book a flight from London to Paris
Q：Would that be a one-way trip or a round-trip flight?
A：one-way
Q：When were you thinking of going?
A：January 1
Q：All done!
A：I am going to run a flight search using the following parameters:\n
             - departure: London\n
             - destination: Paris\n
             - one-way/round-trip: one-way\n
             - time: January 1

Note: If the question contains the word [departure,destination,one-way,time] as the intent of the form, then the question will not be asked.

6, whether to continue the game (when in the booking process, the user wants to exit, the following dialogue will be generated)
A: stop (stop intention, the user wants to exit the booking process)
Q：Do you want to continue?
A：yes (affirm intent, continue the booking process)
Q：Do you want to continue?
A：no（deny intent, exit the booking process)

7、weather_search（tuned and wind weather interface, need to register to get the key to replace the key in actions/actions.py)
Q：How is the weather in London
A：...
Q：What about London
A：...

8、search_btc（tuned interface)
Q：BTC price
A：Give the price trend chart

9、game_play
A：game playing
Q：Now I am going to ask you a riddle, try to figure out the answer!
A：(Randomly give the riddle prepared in data/game_data/query.txt)
Q：a mushroom
A：correct . (determine whether the answer answered by the user is more than 0.6 similar to the correct answer, and give the corresponding answer)

###################################################################
IV. Description of documents
- formbot_en:rasa model
    - actions
		- data: questions and answers for the quiz
		- game_data/query.txt
		- game_data/response.txt
		- utils: BTC price interface tool code
		- coins.py
		- request.py
		- search.py
		- actions.py: rasa main build answer script
    - data
        - nlu.yml:rasa training corpus
        - rules.yml: single-round dialogue pipeline
        - stories.yml:multi-round dialogue story
    - models: trained models
    - config.yml: set up rasa algorithms such as intention classification
    - domain.yml: all the answers to the questions
    - endpoints.yml: port database configuration
    - formbot.log: logs
- rasa_bot_front:front-end code, you can compile the source code, execute the command can see the README in the directory
- ChatbotWidget: front-end code, can not be compiled, direct browser open

####################################################################

REFERENCE : 
rasa CODE：https://github.com/RasaHQ/rasa
rasa MODLE：https://github.com/Dustyposa/rasa_ch_faq

Two interfaces are used
CITY_LOOKUP_URL = "https://geoapi.qweather.com/v2/city/lookup"
WEATHER_URL = "https://devapi.qweather.com/v7/weather/now"