from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, Job
import requests
import json
import requests
import logging


my_chat_id='0'
updater = Updater(token='CHAT_TOKEN')
jobqueue = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Okay! I am collecting the info of your repositories and number of stars. Please wait")
	job_minute = Job(callback_minute, 60.0)
	jobqueueput(job_minute, next_t=0.0)

def echo(bot, update):
	global my_chat_id
	bot.send_message(chat_id='CHAT_ID', text=update.message.text)
	my_chat_id=update.message.chat_id
	
	print update.message.chat_id

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

'''
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
'''
def callback_minute(bot, job):
	bot.send_message(chat_id='CHAT_ID', text=get_data())




updater.start_polling()


def get_data():

	access_token='YOUR_API_TOKEN'
	username="YOUR_USERNAME"
	r = requests.get('https://api.github.com/users/'+username+'/repos?access_token='+access_token)
	project_name=""
	json_data = json.loads(r.text)
	last_data="CONTRIBUTED REPOSITORIES \n"
	for repo in json_data:
		r  = requests.get('https://api.github.com/repos/'+username+'/'+repo["name"]+'?access_token='+access_token)
		data = json.loads(r.text)
		if 'parent' in data:
			project_name = data["parent"]["full_name"]
			k  = requests.get('https://api.github.com/repos/'+project_name+'/commits'+'?access_token='+access_token)

		else:
			project_name = data["full_name"]
			k  = requests.get('https://api.github.com/repos/'+project_name+'/commits'+'?access_token='+access_token)
		#print project_name
		commit_data = json.loads(k.text)
		is_user_in=False
		for i in commit_data:
			try:
				if i["author"]["login"] == username:
					is_user_in=True
			except:
					pass
			try:
				if i["author"]["name"] == username:
					is_user_in=True

			except:
					pass
			try:
				if i["commit"]["author"]["name"] == username:
					is_user_in=True

			except:
					pass
		
		s  = requests.get('https://api.github.com/repos/'+project_name+'?access_token='+access_token)
		commit_data = json.loads(s.text)
		stargazers_count=commit_data["stargazers_count"]
		if is_user_in:
			if stargazers_count !=0 :
				last_data=last_data+project_name+"  "+str(stargazers_count)+"  \n\n"
	print last_data
	return last_data

