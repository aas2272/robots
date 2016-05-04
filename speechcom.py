import speech_recognition as sr
import sys

class speechcom():

	def __init__(self):
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print "there say something"
			audio = r.listen(source)

		try:
			self.data =  r.recognize_google(audio)
			print self.data
			

		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
			sys.exit(0)
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
			sys.exit(0)


	def get_text(self):
		return self.data
















