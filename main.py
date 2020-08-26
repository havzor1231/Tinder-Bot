from tinder_api_sms import *;
from features import *;
import pprint
import datetime
import string
import dialogflow
import os   
from google.api_core.exceptions import InvalidArgument
from twilio.rest import Client
import sched, time


s = sched.scheduler(time.time, time.sleep)

account_sid = '#'
auth_token = '#'
client = Client(account_sid, auth_token)

dialogflowProjectId = '#'
dialogflowLanguageCode = 'en-US'
googleAppCred = 'C:\\Users\\andykim\\Documents\\TinderAPI\\Tinder\\#.json'

	
credential_path = "C:\\Users\\andykim\\Documents\\TinderAPI\\Tinder\\#.json"
os.environ['googleAppCred'] = credential_path



def dialogText(id, message):
	text_to_analyze = message;

	session_client = dialogflow.SessionsClient()
	session = session_client.session_path(dialogflowProjectId, id)

	textInput = dialogflow.types.TextInput(text=text_to_analyze, language_code=dialogflowLanguageCode)
	query_input = dialogflow.types.QueryInput(text=textInput)
	try:
	    response = session_client.detect_intent(session=session, query_input=query_input)
	except InvalidArgument:
	    raise
	print("Query text:", response.query_result.query_text)
	print("Detected intent:", response.query_result.intent.display_name)
	print("Detected confidence:", response.query_result.intent_detection_confidence)
	print("Fulfillment text:", response.query_result.fulfillment_text)
	print("\n");

	return response.query_result.fulfillment_text;

def twilioMsg(name, pic, message, id):
	message = client.messages \
                .create(
                     body = "After talking with \'you\' for a bit, " + name + " " + message + "\n \n if you want to hangout, check your tinder! \n \n if not, please reply to this with the ID. \n \n ID: " + id,
                     from_='+14082157063',
                     media_url = pic,
                     to = '+14088911891'
                 )


	print(message.sid)


printer = pprint.PrettyPrinter(indent=4)
self_dict = get_self();
selfId = self_dict['_id'];

def automated_replies():
	#recs = get_recommendations()["results"];
	count = "90";
	match_dict = all_matches(count);

	matches = match_dict["data"]["matches"];

	#find last message that we didnt send for each user
	for user in matches:

		userId = user['_id'];
		if user['messages']:
			lastMessage = user['messages'][-1];
			if lastMessage['from'] != selfId:
				message = lastMessage['message'];
				reply = dialogText(userId,message);
				reply = reply.lower();
				print(reply)
				if "hangout with you" in reply:
					name = user['person']['name'];
					pic = user['person']['photos'][0]['processedFiles'][0]['url'];
					twilioMsg(name, pic, reply, userId);

				elif reply:
					send_msg(userId, reply);	
	#s.enter(150, 1, automated_replies);

def replymessages_ex():
	count = "80";
	match_dict = all_matches(count);

	date = str(datetime.datetime.now()).replace(" ", "");
	#print(date);

	self_dict = get_self();
	selfId = self_dict['_id'];

	matches = match_dict["data"]["matches"];

	#find last message that we didnt send for each user
	for user in matches:
		userId = user['_id'];
		
		if user['messages']:
			
			lastMessage = user['messages'][-1];
			if lastMessage['from'] != selfId:
				message = lastMessage['message'];
				reply = dialogText(userId, message).lower();

				print(reply)
				if reply:
					send_msg(userId, reply);

def automatedliking_ex():
	recs = get_recommendations()["results"];

	#print(recs);
	i = 1;
	for user in recs:
		if i < 30:
			userId = user['_id'];
			print(like(userId));
		i+=1;



#s.enter(150, 1, fn);
#s.run()
