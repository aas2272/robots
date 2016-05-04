import nltk
import sys
import time
import math
import spacy
from spacy.en import English
from command_obj import command_obj
from speechcom import speechcom
from nlp_talker import talker

class session():
	def __init__(self):

		option = raw_input('Choose an option(1 for speech, 2 for text): ')
		if option == '1':
			print "Say a command!\n\n\n"
			speech = speechcom()
			self.data = speech.get_text()

		else:
			self.data = raw_input('Write a command:\n\n\n')

		cmd = command_obj(self.data, option)


		output = cmd.get_output()

		for command in output:
			print command
			string_com = ' '.join(command[:3])
			adj = ' '.join(command[3])
			string_com += ' ' + adj
			print 'publishing'
			talker(string_com)
			time.sleep(10)
			print 'awake'


if __name__ == "__main__":
	sentence = ' '.join(sys.argv[1:])
	ses = session()



