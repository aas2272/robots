import nltk
import sys
import time
import math
import spacy
from spacy.en import English
from command_obj import command_obj
# from spacy.parts_of_speech import *

class session():
      def __init__(self):

            self.data = raw_input("Welcome, please enter a command:\n")

            cmd = command_obj(self.data)

      def process(self, data):
            # nlp = English()
            # doc = nlp(unicode(indata))
            # token = doc[0]
            # sentence = next(doc.sents)

            cmd = command_obj()
            # action = 'plick_up'
            action = data
            # action = 'plick_up'
            act = cmd.set_action(action)

            # for word in sentence:
            #       print str(word) +'/',
            #       print word.pos_
            #       print word.tag_
            #       # print nlp.vocab.strings[word.pos]
            #       print nlp.vocab.strings[word.dep]
            #       print word.head


            if act:
                  print "action set"
            else:
                  ans = raw_input("I dont know that command, do you want to teach me how to "+ action+"? (yes/no) ")
                  if ans == 'yes' or ans == 'y':
                        created = self.teach_action(action)
                        print created
                  else:
                        print "No action set"
                        # return False




      def teach_action(self, action):

            concat_coms = []
            while(True):
                  ans = raw_input('Add an action? (y/n/cancel) ')
                  if ans == 'cancel' or ans == 'c':
                        return False
                  elif ans == 'yes' or ans == 'y':
                        cmd = command_obj()
                        print cmd.actions
                        task = raw_input('Please write our the next step using the intermediate command:\n')
                        print task


                        self.process(task)

                        concat_coms.append(task)
                  else:
                        break


if __name__ == "__main__":
   #sentence = "I "
   sentence = ''
   for x in sys.argv[1:]:
      sentence += str(x) + " "

      # output = main(sentence)
      # print output



   ses = session()

   # # sentence[:-1]
   # ses.process(ses.data)
#

