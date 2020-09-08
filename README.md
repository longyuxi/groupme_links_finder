# Overview

Ever have a GroupMe chat where invitations to other groupme chats are posted, and you have to scroll so far up to find the invitations that you need? This Python script comes to the rescue by reading all the GroupMe messages in a specific chat and stores all the invitation links to a table file called *links.tsv*.

Besides the invitation link and the inferred group title, the table also includes the sender name, send time and original message, so you can tag the original poster and ask him or her to send you a new invitation in case the original link expired. The file is stored in a .tsv file, which you can open with Excel or any other workspace software, just choose the option to open a tab delimited file and Unicode-8 for the smiley emojis in all your Group titles.

# Installation

1. Clone this repository. 
2. Install Groupy through `pip install GroupyAPI`.
3. Follow the [tutorial on Groupy's website](https://groupy.readthedocs.io/en/latest/pages/installation.html) to obtain your Access Token. Once you have it, open a new file within the folder of your repository called `token` and paste the token in there. And you are ready to go!

# Use
1. Edit the *TARGET_GROUP_NAME* first line of *invitation-link-digger.py* to match the name of the group the chat history of which  you want to search through. *TARGET_GROUP_NAME* only has to be a substring unique to the title of your target group, so you don't have to copy the emojis verbatim. 
2. To run, simply navigate to the directory where you want to save *links.tsv* and run the python script with `python /path/to/invitation-link-digger.py`. Be sure to run it with Python 3.5+ 