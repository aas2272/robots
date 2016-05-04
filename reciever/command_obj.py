import csv
import nltk
import sys
import time
import math
import spacy
from spacy.en import English

class command_obj():

      def __init__(self, sentence):
            self.sentence = sentence.lower()
            self.action = None
            self.object = None
            self.location = None
            self.actions = {}
            self.amods = []
            self.preps = []




##### Make it a json


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
                              # print
                              amods = unicode(line[3])
                              prep = unicode(line[4])
                              temp_list.append([act, loc, obj, amods, prep])#, amods])

                        else:
                              sys.exit('this file is corrupted')

                  try:
                        self.actions[temp_act] = temp_list
                  except:
                        pass

            print self.actions.keys()
            self.passed = self.parse(self.sentence)
            self.set_action(self.passed)
            try:
                  self.set_object(self.passed['direct_object'], self.passed['amods'])
            except:
                  print 'no object'

            try:
                  self.set_location(self.passed['loc'])
            except:
                  print 'no adv'

            try:
                  self.set_preps(self.passed['prep'])
            except:
                  print 'no preps'


            output = self.run()
            print output

            print self.action
            print self.object
            print self.location
            print self.amods
            print self.preps

      def set_action(self, passed):

            action = passed['action']

            if action in self.actions.keys():
                  self.action = action
                  print "action set"

            else:
                  ans = raw_input("I dont know that command because unidentified action " +action+ ", do you want to teach me how to \'"+ self.sentence +"\'? (yes/no)\n")
                  if ans == 'yes' or ans == 'y':
                        created = self.teach_action(passed)
                        if created:
                              self.action = action
                              for x in self.concat_coms:
                                    print x
                              print "saving"
                              self.save(self.coms_vals)

                        else:
                              print "no action created"
                  else:
                        print "No action set"
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
                  ans = raw_input('Add an action? (y/n/cancel):\n')
                  if ans == 'cancel' or ans == 'c':
                        return False
                  elif ans == 'yes' or ans == 'y':
                        print self.actions.keys()
                        task = raw_input('Please write our the next step using the intermediate command:\n')
                        print task

                        cmd = command_obj(task)
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
                  ##### CHECK THIS ABOVE LINE
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
                        print word.orth_ + 'root'
                        root =  word
                        return root



                  # else:
                        # print word.orth_ + word.dep_ + word.head.orth_
            # return root

      def get_prep(self, prep_list, child):


            # child.dep_ == 'prep':
            prep = child
            print prep.orth_ + 'prep'
            l = []
            l.append(prep.orth_)

            for ch in prep.children:

                  if ch.dep_ == 'pobj':
                        pobj = ch
                        print pobj.orth_ + 'pobj'
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

            print sentence


            # for word in sentence:

                  # if word.dep_ == 'ROOT':
                  #       root = word.orth_
                  #       print root + 'root'

                  # elif word.dep_ == 'dobj':
                  #       direct_object = word.orth_
                  #       print direct_object + 'dobj'

                  # elif word.dep_ == 'amod':
                  #       amods.append(word.orth_)
                  #       print word.orth_ + 'amod'

                  # elif word.dep_ == 'prt':
                  #       prt = word.orth_
                  #       print prt + 'prt'

                  # else:
                  #       print 'None ' + word.dep_



                  # print word.head
                  # print str(word) +'/'
                  # print word.pos_
                  # print word.tag_
                  # # print nlp.vocab.strings[word.pos]
                  # print nlp.vocab.strings[word.dep]
                  # print word.head

            root = self.find_root(sentence)
            prep_list = []
            amods = []
            # root is going to be the main verb
            for child in root.children:

                  if child.dep_ == 'dobj':
                        # this is the object of the verb
                        direct_object = child
                        print direct_object.orth_ + 'dobj'

                        for ch in direct_object.children:
                              #gets the adjectives of the direct object
                              if ch.dep_ == 'amod':
                                    amods.append(ch.orth_)
                                    print ch.orth_ + 'amod'

                              elif ch.dep_ == 'prep':
                                    print ch
                                    prep_list = self.get_prep(prep_list, ch)
                                    #### check preps for child objects

                  elif child.dep_ == 'prt' or child.dep_ == 'ccomp':
                        # this is a modifier of the verb, look into this
                        prt = child
                        print prt.orth_ + 'prt'

                  elif child.dep_ == 'prep':
                        # print child.orth_ + '!!!!!'
                        # gets the preposition in order to get prepositional phrases recursively
                        prep_list = self.get_prep(prep_list, child)
                        # this is a list of lists, where each list is in this format [prepostion, object, [adj of objects]]
                        print prep_list

                  elif child.dep_ == 'advmod':

                        advmod = child
                        print advmod






                  # else:
                  #       print 'None ' + word.dep_
            # print word.head
            # print str(word) +'/'
            # print word.pos_
            # print word.tag_
            # # print nlp.vocab.strings[word.pos]
            # print nlp.vocab.strings[word.dep]
            # print word.head

            # print word.orth_ + ' word'
            # print word.dep_ + ' dep'
            # print 'children'
            # for x in word.children:
            #       print x,
            # print ''
            # print word.head.orth_ + ' head'



            passed = {}
            try:
                  passed['action'] = root.orth_ + '_' + prt.orth_
            except:
                  passed['action'] = root.orth_

            try:
                  passed['direct_object'] = direct_object.orth_
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

            #trouble with up/direction

            return passed



      def __str__(self):
            return self.sentence

      def save(self, vals):

            with open('data/actions.csv', 'a+') as f:
                  writer = csv.writer(f, delimiter = ',')
                  print vals
                  print self.action
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
                  print line
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
                              print ind
                              print self.preps
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


