"""
Author: Jacob Barca
Since: 26/5/20
Last Modified: 29/5/20
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

	def generate_text(self, text, n, max_iterations):
		model = markov.build_model(text, n)
		new_text = markov.generate(model, n, None, max_iterations)
		return new_text

	def run(self):
		while True:
			event, values = self.window.read()
			#print(event, values)
			if event in (None, 'Exit'):
				break
			if event == '-B1-':
				if len(values['-IN-']) > 1:
					order = 2
					max_iterations = 100
					if len(values['-D1-']) > 0 and len(values['-IN2-']) > 0:
						order = int(values['-D1-'])
						max_iterations = int(values['-IN2-'])
					text = self.generate_text(values['-IN-'], order, max_iterations)
					print(text, end='')
			if event == 'Clear':
				self.window['-OUTPUT-'].update('')

		self.window.close()


if __name__ == "__main__":
	app = Application('Markov Chain', 'Default1')
	app.add_layout_items([[sg.Text('Enter text below to be used in the text generation:')],
						  [sg.Text('File to open: '), sg.Input(), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
						  [sg.Multiline('', key='-IN-', size=(100, 10))],
						  [sg.Output(size=(100,10), key='-OUTPUT-')],
						  [sg.Text('Order: '), sg.Drop(values=('2', '3', '4', '5', '6'), auto_size_text=True, key='-D1-')],
						  [sg.Text('Max iterations: '), sg.Input(key='-IN2-', size=(10, 10))],
						  [sg.Button('Go', key='-B1-'), sg.Button('Clear'), sg.Button('Exit')]])
	app.create_window()

	app.run()



