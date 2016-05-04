import csv
import nltk
import sys
import time
import math
import spacy
from spacy.en import English
from speechcom import speechcom

class command_obj():

      def __init__(self, sentence, option):
            self.sentence = sentence.lower()
            self.action = None
            self.object = None
            self.location = None
            self.actions = {}
            self.amods = []
            self.preps = []
	    self.option = option

            with open('data/actions.csv', 'r+') as f:
                  reader = csv.reader(f, delimiter = ',')
                  for line in reader:
                        if len(line) == 1:
                              try:
                                    self.actions[temp_act] = temp_list
                              except:
                                    pass

                              temp_act = unicode(line[0])
                              temp_list = []

                        elif len(line) == 5:
                              act = unicode(line[0])
                              loc = unicode(line[1])
                              obj = unicode(line[2])
                              amods = unicode(line[3])
                              prep = unicode(line[4])
                              temp_list.append([act, loc, obj, amods, prep])

                        else:
                              sys.exit('this file is corrupted')

                  try:
                        self.actions[temp_act] = temp_list
                  except:
                        pass

            #print self.actions.keys()
            self.passed = self.parse(self.sentence)
            self.set_action(self.passed)
	    
            try:
                  self.set_object(self.passed['direct_object'], self.passed['amods'])
		  if self.object == None:
			self.object = ''
            except:
		  self.set_object('', [])
                  print 'no object'

            try:
                  self.set_location(self.passed['loc'])
            except:
                  #print 'no adv'
		  pass
            try:
                  self.set_preps(self.passed['prep'])
            except:
                  #print 'no preps'
		  pass

            self.output = self.run()
            #print output

            #print self.action
            #print self.object
            #print self.location
            #print self.amods
            #print self.preps

      def get_output(self):
	    return self.output


      def set_action(self, passed):

            action = passed['action']

            if action in self.actions.keys():
                  self.action = action
                  #print "action set"

            else:
		  if self.option == '1':
		        print "I dont know that command because unidentified action " +action+ ", do you want to teach me how to \'"+ self.sentence +"\'?\n\n\n" 

		        speech = speechcom()

		        ans = speech.get_text()
		  else:
                  	ans = raw_input("I dont know that command because unidentified action " +action+ ", do you want to teach me how to \'"+ self.sentence +"\'? (yes/no)\n")


                  if ans.lower() == 'yes' or ans.lower() == 'y':
                        created = self.teach_action(passed)
                        if created:
                              self.action = action
                              for x in self.concat_coms:
                                    print x
                              print "saving"
                              self.save(self.coms_vals)

                        else:
			      sys.exit('Action not created')
                  else:
                        sys.exit("No action set")
                        # return False

      def set_object(self, obj, amods):
            self.object = obj
            self.amods = amods
            ### check if object is in environment


      def set_location(self, loc):
            self.location = loc

      def set_preps(self,prep_list):
            self.preps = prep_list


      def teach_action(self, passed):

            action = passed['action']

            print "Teaching how to " + action

            self.concat_coms = []
            self.coms_vals = []
            while(True):

		  if self.option == '1':
		  	print 'Add an action?\n\n\n'
		        speech = speechcom()
		        ans = speech.get_text()
		  else:
                        ans = raw_input('Add an action? (y/n/cancel):\n')

                  if ans.lower() == 'cancel' or ans.lower() == 'c':
                        return False
                  elif ans.lower() == 'yes' or ans.lower() == 'y':
                        print self.actions.keys()
                        #print task
			if self.option == '1':
			      print 'Please say the next step using the intermediate commands:\n\n\n'
			      speech = speechcom()
			      task = speech.get_text()
			else:
			
                              task = raw_input('Please write our the next step using the intermediate command:\n')

                        cmd = command_obj(task, self.option)
                        vals = self.assign(cmd)


                        self.concat_coms.append(cmd)
                        self.coms_vals.append(vals)
                  else:
                        ## no command added
                        if len(self.concat_coms) < 1:
                              return False
                        else:
                        ## have tasks to make this command
                              break



            return True

      def assign(self, cmd):

            vals = {}
            try:
                  obj1 = cmd.passed['direct_object']
            except:
                  obj1 = None
            try:
                  obj2 = self.passed['direct_object']
            except:
                  obj2 = None

            if obj1 == obj2 and obj1 != '':
                  vals['obj'] = 'object'
                  vals['amods'] = 'cmd'#.passed['amods']
            else:
                  vals['obj'] = ''
                  vals['amods'] = ''#self.passed['amods']
            try:
                  loc1 = cmd.passed['loc']
            except:
                  loc1 = None
            try:
                  loc2 = self.passed['loc']
            except:
                  loc2 = None

            if loc1 == loc2 and loc1 != '':
                  vals['loc'] = 'location'
            else:
                  vals['loc'] = loc1

            try:
                  prep1 = cmd.passed['prep']
            except:
                  prep1 = []

            try:
                  prep2 = self.passed['prep']
            except:
                  prep2 = []

            out_preps = {}
            i = 0
            for x in prep1:
                  found = False

                  for y in range(len(prep2)):
                        if x[0] == prep2[y][0] and x[1] == prep2[y][1]:
                              out_preps[i] = y
                              found = True
                              i += 1

                  if found == False:
                        print 'prep not found'

            vals['prep'] = out_preps
            vals['action'] = cmd.passed['action']

            return vals


      def find_root(self, sentence):
            for word in sentence:
                  if word.dep_ == 'ROOT':
                        #print word.orth_ + 'root'
                        root =  word
                        return root



                  # else:
                        # print word.orth_ + word.dep_ + word.head.orth_
            # return root

      def get_prep(self, prep_list, child):


            # child.dep_ == 'prep':
            prep = child
            #print prep.orth_ + 'prep'
            l = []
            l.append(prep.orth_)

            for ch in prep.children:

                  if ch.dep_ == 'pobj':
                        pobj = ch
                        #print pobj.orth_ + 'pobj'
                        l.append(pobj.orth_)
                        amods = []
                        for c in pobj.children:
                              if c.dep_ == 'prep':
                                    next = c
                              elif c.dep_ == 'amod':
                                    amods.append(c.orth_)
                        l.append(amods)
                        prep_list.append(l)
                        try:
                              prep_list = self.get_prep(prep_list, next)
                        except:
                              pass


            return prep_list




      def parse(self, sentence):
            nlp = English()
            doc = nlp(unicode(sentence))
            sentence = next(doc.sents)

            #print sentence

            root = self.find_root(sentence)
            prep_list = []
            amods = []
	    direct_object = None
            # root is going to be the main verb
            for child in root.children:

                  if child.dep_ == 'dobj':
                        # this is the object of the verb
                        direct_object = child
                        #print direct_object.orth_ + 'dobj'

                        for ch in direct_object.children:
                              #gets the adjectives of the direct object
                              if ch.dep_ == 'amod':
                                    amods.append(ch.orth_)
                                    #print ch.orth_ + 'amod'

                              elif ch.dep_ == 'prep':
                                    #print ch
                                    prep_list = self.get_prep(prep_list, ch)
                                    #### check preps for child objects

                  elif child.dep_ == 'prt' or child.dep_ == 'ccomp':
                        # this is a modifier of the verb, look into this
                        prt = child
                        #print prt.orth_ + 'prt'

                  elif child.dep_ == 'prep':
                        #print child.orth_ + '!!!!!'
                        # gets the preposition in order to get prepositional phrases recursively
                        prep_list = self.get_prep(prep_list, child)
			if root.orth_ == 'go':
			      if len(prep_list) > 0 and direct_object == None:
			            direct_object = prep_list[0][1]
				    amods = prep_list[0][2]
			            		
                        # this is a list of lists, where each list is in this format [prepostion, object, [adj of objects]]
                        #print prep_list

                  elif child.dep_ == 'advmod':

                        advmod = child
                        #print advmod




            passed = {}
	    
            try:
                  passed['action'] = root.orth_ + '_' + prt.orth_
            except:
                  passed['action'] = root.orth_
	    

	    if passed['action'] == 'pick_up':
		  passed['action'] = unicode('pick')

	    elif root.orth_ == 'move':
		  passed['action'] = unicode('move')

            try:
                  passed['direct_object'] = direct_object.orth_
            except:
		  try:
			passed['direct_object'] = direct_object
		  except:
                        passed['direct_object'] = ''

            try:
                  passed['amods'] = amods
            except:
                  passed['amods'] = ''

            try:
                  passed['prep'] = prep_list
            except:
                  passed['prep'] = ''

            try:
                  passed['loc'] = advmod
            except:
                  passed['loc'] = ''

	    if passed['action'] == 'move':
		  passed['loc'] = sentence[-1].orth_
	    ### This is because it thinks move up and move down are single commands

            #trouble with up/direction

            return passed



      def __str__(self):
            return self.sentence

      def save(self, vals):

            with open('data/actions.csv', 'a+') as f:
                  writer = csv.writer(f, delimiter = ',')
                  #print vals
                  #print self.action
                  writer.writerow([self.action])
                  actions_array = []

                  for x in vals:
                        # amods = '; '.join(map(str, x['amods']))
                        # prep = '; '.join(map(str, x['prep']))
                        out = []
                        for y in range(len((x['prep']).keys())):
                              out.append(x['prep'][y])

                        prepositions = ';'.join(map(str, out))

                        to_save = [x['action'], x['loc'], x['obj'], x['amods'], prepositions]#, x['amods']]
                        print to_save
                        actions_array.append(to_save)
                        writer.writerow(to_save)
                  self.actions[self.action] = actions_array
                        # check out dictwriter

      def run(self):
            output = []

            for line in self.actions[self.action]:
                  #print line
                  out = [line[0]]
                  if line[1] == 'location':
                        out.append(self.location)
                  else:
                        out.append(line[1])
                  if line[2] == 'object':
                        out.append(self.object)
                  else:
                        out.append(line[2])

                  if line[3] == 'cmd':
                        out.append(self.amods)
                  else:
                        out.append([])

                  ##### look into this one to see if it makes sense
                  if line[4] != '':
                        out_prep = []
                        preps = line[4].split(';')
                        for x in preps:
                              ind = int(x)
                              #print ind
                              #print self.preps
                              try:

                                    out_prep.append(self.preps[ind])
                              except:
                                    pass

                        out.append(out_prep)
                  else:
                        out.append([])

                  output.append(out)
            if len(output) == 0:
                  output.append([self.action, self.location, self.object, self.amods, self.preps])

            return output
                  ### Deal with a mods


