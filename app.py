"""
Author: Jacob Barca
Since: 26/5/20
Last Modified: 26/5/20
"""

import PySimpleGUI as sg
from markov import TextGenerator as tg


class Application:
	def __init__(self, pattern, theme):
		self.layout = []
		self.window = None
		self.pattern = pattern
		self.set_theme(theme)

	def set_theme(self, theme):
		sg.theme(theme)

	def add_layout_items(self, layout_items):
		for item in layout_items:
			self.layout.append(item)

	def create_window(self):
		self.window = sg.Window(self.pattern, self.layout)

	def run(self):
		while True:
			event, values = self.window.read()
			print(event, values)
			if event in (None, 'Exit'):
				break
			if event == 'Show':
				self.window['-OUTPUT-'].update(values['-IN-'])

		self.window.close()


if __name__ == "__main__":
	app = Application('Pattern 2B', 'BluePurple')
	app.add_layout_items([[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
						 [sg.Input(key='-IN-')],
						 [sg.Button('Show'), sg.Button('Exit')]])
	app.create_window()

	app.run()



