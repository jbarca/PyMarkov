"""
Author: Jacob Barca
Since: 26/5/20
Last Modified: 28/5/20
"""

import PySimpleGUI as sg
import markov


class Application:
	def __init__(self, title, theme=None):
		self.layout = []
		self.window = None
		self.title = title
		if theme:
			self.set_theme(theme)

	def set_theme(self, theme):
		sg.theme(theme)

	def add_layout_items(self, layout_items):
		for item in layout_items:
			self.layout.append(item)

	def create_window(self):
		self.window = sg.Window(self.title, self.layout)

	def generate_text(self, text, n):
		model = markov.build_model(text, n)
		new_text = markov.generate(model, n)
		return new_text

	def run(self):
		while True:
			event, values = self.window.read()
			#print(event, values)
			if event in (None, 'Exit'):
				break
			if event == 'Go':
				text = self.generate_text(values['-IN-'], 2)
				print(text, end='')
			if event == 'Clear':
				self.window['-OUTPUT-'].update('')

		self.window.close()


if __name__ == "__main__":
	app = Application('Markov Chain')
	app.add_layout_items([[sg.Text('What you will print will display below:')],
						  [sg.Multiline('', key='-IN-', size=(50, 10))],
						  [sg.Output(size=(50,10), key='-OUTPUT-')],
						  [sg.Button('Go'), sg.Button('Clear'), sg.Button('Exit')]])
	app.create_window()

	app.run()



