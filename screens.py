import tkinter as tk

class Welcome(tk.Frame):

	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Chess")
		self.root.geometry("375x120")
		self.info = (("",""),("",""))
		self.widgets = []

		tk.Frame.__init__(self, self.root)
		self.create_widgets()

	def create_widgets(self):
		self.root.bind('<Return>', self.hit_enter)

		welcome_label = tk.Label(self.root, text = "Please enter settings:")
		welcome_label.grid(column = 0, row = 0)
		info_label = tk.Label(self.root, text = "NAME")
		info_label.grid(column = 1, row = 1)
		sele_label = tk.Label(self.root, text = "TYPE")
		sele_label.grid(column = 2, row = 1)

		ne_lb1 = tk.Label(self.root, text = "(WHITE)")
		ne_lb1.grid(column = 0, row = 2)
		ne_lb2 = tk.Label(self.root, text = "(BLACK)")
		ne_lb2.grid(column = 0, row = 4)

		name_entry = tk.Entry(self.root, width = 10)
		name_entry.grid(column = 1, row = 2)
		name_entry.focus()

		name_entry2 = tk.Entry(self.root, width = 10)
		name_entry2.grid(column = 1, row = 4)

		p1sel = tk.StringVar()
		p2sel = tk.StringVar()

		player_sel1 = tk.Radiobutton(self.root, text = "Live", value = "L", variable = p1sel)
		player_sel1.grid(column = 2, row = 2)
		comput_sel1 = tk.Radiobutton(self.root, text = "AI", value = "A", variable = p1sel)
		comput_sel1.grid(column = 3, row = 2)

		player_sel2 = tk.Radiobutton(self.root, text = "Live", value = "L", variable = p2sel)
		player_sel2.grid(column = 2, row = 4)
		comput_sel2 = tk.Radiobutton(self.root, text = "AI", value = "A", variable = p2sel)
		comput_sel2.grid(column = 3, row = 4)

		enter = tk.Button(self.root, text = "Enter", command = self.submit)
		enter.grid(row = 6, column = 1)

		self.widgets.append(name_entry)
		self.widgets.append(name_entry2)
		self.widgets.append(p1sel)
		self.widgets.append(p2sel)

	def start(self):
		self.root.mainloop()

	def submit(self):
		self.info = []
		self.info.append((self.widgets[0].get(), self.widgets[2].get()))
		self.info.append((self.widgets[1].get(), self.widgets[3].get()))
		self.info = tuple(self.info)
		self.root.destroy()

	def get_entry_info(self):
		return self.info

	def hit_enter(self, event):
		self.submit()