"""
Author: Jacob Barca
Since: 26/5/20
Last Modified: 7/6/20
"""

import PySimpleGUI as sg
import markov


class Application:
	"""
	Class that encapsulates a PySimpleGUI GUI "Application" and its features
	-- should be a singleton class for this particular project.
	"""
	def __init__(self, title, theme=None):
		self.layout = []
		self.window = None
		self.title = title
		self.text_changed = False
		self.current_model = None
		self.current_text = ""
		if theme:
			self.set_theme(theme)

	def set_theme(self, theme):
		sg.theme(theme)

	def add_layout_items(self, layout_items):
		for item in layout_items:
			self.layout.append(item)

	def create_window(self):
		self.window = sg.Window(self.title, self.layout)

	def generate_text(self, text, n, seed=None, max_iterations=100):
		model = self.current_model
		if self.text_changed or not self.current_model:
			model = markov.build_model(text, n)
			self.current_model = model
			self.text_changed = False
		new_text = markov.generate(model, n, seed, max_iterations)
		return new_text

	def run(self):
		while True:
			event, values = self.window.read()
			#print(event, values)
			if event in (None, 'Exit'):
				break
			if event == '-B1-':
				# Generates text based on the markov chain module created in markov.py
				# the user can choose an order and the maximum iterations. Each generation
				# is printed on it's own separate line.
				if len(values['-IN-']) > 1:
					order = 2
					max_iterations = 100
					if len(values['-D1-']) > 0 and len(values['-IN2-']) > 0:
						order = int(values['-D1-'])
						max_iterations = int(values['-IN2-'])
					text = self.generate_text(values['-IN-'], order, None, max_iterations)
					self.window['-OUTPUT-'].print(text, end='')
			if event == '-FILE-':
				# Opens a file to read into the input box
				if values['-FILE-']:
					with open(values['-FILE-'], 'r') as f:
						text = f.read()
						self.window['-IN-'].update(text)
			if event == '-IN-':
				self.text_changed = True
				# Autocomplete like feature that allows dynamic text generation based on
				# the last few characters of the text. Changes dynamically as the user types.
				if values['-DG-']:
					order = 2
					max_iterations = 100
					if len(values['-D1-']) > 0 and len(values['-IN2-']) > 0:
						order = int(values['-D1-'])
						max_iterations = int(values['-IN2-'])
					order = min(order, len(values['-IN-'][:-1]))
					# TODO: Add dynamic model updating when user types in new text
					model = markov.build_model(values['-IN-'][:-1], order, self.current_model)
					new_text = markov.generate(model, order, values['-IN-'][-order-1:-1], max_iterations)
					self.window['-OUTPUT-'].update('')
					self.window['-OUTPUT-'].print(values['-IN-'][:-1], end='')
					self.window['-OUTPUT-'].print(new_text[order:], text_color='white', background_color='red', end='')
					self.current_text = values['-IN-'][:-1]

			if event == 'Clear':
				# Clear the output box
				self.window['-OUTPUT-'].update('')

		self.window.close()


if __name__ == "__main__":
	app = Application('Markov Chain', 'Default1')
	app.add_layout_items([[sg.Text('Enter text below to be used in the text generation, or read in a text file:')],
						  [sg.Text('File to open: '), sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
						  [sg.Multiline('', key='-IN-', size=(100, 10), enable_events=True)],
						  [sg.MLine(size=(100,10), key='-OUTPUT-', disabled=True)],
						  [sg.Text('Order: '), sg.Drop(values=('2', '3', '4', '5', '6'), auto_size_text=True, key='-D1-')],
						  [sg.Text('Max iterations: '), sg.Input(key='-IN2-', size=(10, 10))],
						  [sg.Checkbox('Dynamic generation', default=False, key='-DG-', enable_events=True)],
						  [sg.Button('Go', key='-B1-'), sg.Button('Clear'), sg.Button('Exit')]])
	app.create_window()

	app.run()



