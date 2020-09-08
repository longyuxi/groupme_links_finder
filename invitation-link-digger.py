TARGET_GROUP_NAME = "DUKE 2024" 

# import groupme token
tokenfile = open("token", "r")
TOKEN = tokenfile.readline().replace("\n", "")
tokenfile.close()


from groupy.client import Client
client = Client.from_token(TOKEN)
import re
import csv
output_file = open("links.tsv", "wt", encoding="utf-8")
tsv_writer = csv.writer(output_file, delimiter = "\t")
tsv_writer.writerow(["group title (if [N/A] refer to original message)", "link", "sender name", "sent time", "original message"])

target_group_chat = ""


def write_all_msgs_texts_to_file():
	"""Writes all messages within the target group chat to Messages.txt
	"""
	messages = target_group_chat.messages.list()
	oldest_message_in_page = messages[0]

	total_number_of_messages = 0

	while True:
		messages = target_group_chat.messages.list(oldest_message_in_page.id)
		msgs = ""
		for m in messages:
			try:
				msgs = msgs + m.text + "\n"
			except:
				msgs = msgs + "[NONE]" + "\n"
		f = open("Messages.txt", "a", encoding='utf-8')
		f.write(msgs)
		f.close()
		oldest_message_in_page = messages[-1]

		total_number_of_messages = total_number_of_messages + 20
		print("Number of messages:" + str(total_number_of_messages))



def handle_msg_for_group_link(message):
	"""
	This function compares the content of the incoming message against a Regex argument
	if the content contains a GroupMe invitation, this function can recognize it 
	and will try to infer the title of the group. 

	This function will write data about the message to the file links.tsv
	There are two types of groupme messages: 
		1. perfectly formatted ones: e.g. "You're invited to join my group "Blue Crew" on GroupMe. 
		https://groupme.com/join_group/12345678/1AB2C3D4"
		2. randomly formatted ones: e.g. "Hey a friend and I thought to make a TN groupme, 
		so if you're from Tennessee, you should join. https://groupme.com/join_group/12345678/1AB2C3D4" 
	If type 1: the function will write (group name, sender name, time sent, whole message)
	If type 2: the function will write ("[N/A]", sender name, time sent, whole message)


	Args:
		message (message): the message object to be handled
	"""

	gm_link_matcher = re.compile(r'(https:\/\/(?:app.)?groupme.com\/join_group\/\d{8}\/\w{8})')
	gm_invitation_matcher_1 = re.compile(r'(You\'re invited to my new group)')
	gm_invitation_matcher_2 = re.compile(r'(on GroupMe)')
	if message.text is None:
		txt = ' '
	else:
		txt = message.text.replace("\n", " ")

	if gm_link_matcher.search(txt) is not None:
		# There is a GroupMe invitation link in there
		print(message.text)
		if gm_invitation_matcher_1.search(txt) is not None:
			# There is copy-pasted groupme invitation in there
			link_beginning_index = gm_invitation_matcher_1.search(txt).end() + 2
			link_ending_index = gm_invitation_matcher_2.search(txt).start() - 2

			group_title = txt[link_beginning_index:link_ending_index]
			link = gm_link_matcher.search(txt).group(0)

		else:
			# There is just an invitation link in there
			group_title = "[N/A]"
			link = gm_link_matcher.search(txt).group(0)

		sender_name = message.name
		sent_time = message.created_at
		original_message = txt


		tsv_writer.writerow([group_title, link, sender_name, sent_time, original_message])

		print("title:", group_title)
		print("link:", link)
		print("sender name:", sender_name)
		print("sent time:", sent_time)

def read_all_msgs():
	"""Reads all messages in the channel target_group_chat 
	and handle each message with handle_msg_for_groupme_link()
	"""
	messages = target_group_chat.messages.list()
	oldest_message_in_page = messages[0]

	total_number_of_messages = 0

	while True:
		messages = target_group_chat.messages.list(oldest_message_in_page.id)
		for m in messages:
			handle_msg_for_group_link(m)
		oldest_message_in_page = messages[-1]

		total_number_of_messages = total_number_of_messages + 20
		print("Number of messages:" + str(total_number_of_messages))

def find_all_invitation_links(group_name):
	"""Finds all the invitation links in the first group with its title containing group_name

	Args:
		group_name (str): string contained in the target group's title
	"""
	# fetch group object
	for group in client.groups.list():
		if TARGET_GROUP_NAME in group.name:
			global target_group_chat 
			target_group_chat = group
	try:
		read_all_msgs()
	except IndexError:
		print("Process finished.")
	

if __name__ == "__main__":
	find_all_invitation_links(TARGET_GROUP_NAME)
