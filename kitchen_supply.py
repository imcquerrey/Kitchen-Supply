from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
import json
from datetime import datetime


class AccountSelect:
	def __init__(self, master):
		# Initializing Account Select
		master.title('Login')
		self.root = master

		# Parse Account Names from accounts.csv
		self.loadaccounts()

		# Buttons & Labels
		self.accounts_cb = ttk.Combobox(master, values=self.accounts, state="readonly", width=30)
		self.accounts_cb.set(self.accounts[0])
		self.accounts_cb.grid(column=0, row=0)
		login_bt = Button(master, text='Login', command=self.nextwin, width=30)
		login_bt.grid(column=0, row=1)

		# Center
		windowWidth = master.winfo_reqwidth()
		windowHeight = master.winfo_reqheight()
		positionRight = int(master.winfo_screenwidth() / 2 - windowWidth / 1.5)
		positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
		master.geometry("+{}+{}".format(positionRight, positionDown))

		# Loop
		master.mainloop()


	def loadaccounts(self):
		# Open and loop through every account grabbing the name of the account then appending to list
		csvfile = open('customers.csv', 'r')
		reader = csv.DictReader(csvfile)
		self.accounts = []
		for r in reader:
			self.accounts.append(r['Name'])
		csvfile.close()


	def nextwin(self):
		# Get variables ready
		global user
		user = str(self.accounts_cb.get())
		global carttotal
		carttotal = 0
		global cart
		cart = {}
		global inventoryedit
		inventoryedit = False
		# Remove account select gui and show the main gui
		self.root.destroy()
		win2 = Tk()
		gui = Main(win2)


class Main:
	def __init__(self, master):
		# Initializing Main
		master.title('Kitchen Supply')
		self.root = master

		# Load Account Info
		self.loadaccinfo()

		# Buttons & Labels
		id = Label(master, text='Account ID: %s' % self.id, width=20)
		id.grid(column=0, row=0, sticky=W)
		name = Label(master, text='Name: %s' % user, width=20)
		name.grid(column=1, row=0)
		bal = Label(master, text='Balance: $%s' % self.bal, width=20)
		bal.grid(column=2, row=0)
		self.checkout = Button(master, text='Checkout: %s' % carttotal, command=self.checkout, width=20)
		self.checkout.grid(column=3, row=0)

		# Get Products
		self.products()
		# Add Them to Gui
		col = 0
		row = 1
		for id in self.productids:
			if col != 0:
				if col % 4 == 0:
					row += 1
					col = 0
			# Put id in a dummy variable so that the other buttons do not interfere
			prod = Button(master, text='ID: %s' % id, command=lambda j=id: self.prodinfo(j), width=10)
			prod.grid(column=col, row=row)
			col += 1

		# Quit Button
		quit1 = Button(master, text='Quit', command=self.quit2, width=20)
		quit1.grid(column=0, row=row+1)

		# Inventory Edit
		if employee == 'True':
			self.invedit = Button(master, text='Inventory Edit', command=lambda: self.editinv(True), width=20)
			self.invedit.grid(column=1, row=row + 1)
			self.newitem = Button(master, text='Add Product', command=self.newproduct, width=20)
			self.newitem.grid(column=2, row=row + 1)

		# Check if inventory edit is on
		if inventoryedit == True:
			self.editinv()


		# Center
		windowWidth = master.winfo_reqwidth()
		windowHeight = master.winfo_reqheight()
		positionRight = int(master.winfo_screenwidth() / 2 - windowWidth * 1.5)
		positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
		master.geometry("+{}+{}".format(positionRight, positionDown))

		# Loop
		master.mainloop()

	def quit2(self):
		self.root.destroy()
		sys.exit()

	def loadaccinfo(self):
		# Open file with accounts and loop over all accounts until it gets the users account then grabs user info
		global employee
		csvfile = open('customers.csv', 'r')
		reader = csv.DictReader(csvfile)
		self.accounts = []
		for r in reader:
			if r['Name'] == user:
				self.bal = r['Balance']
				self.id = r['AccountNumber']
				employee = r['Employee']
		csvfile.close()

	def products(self):
		# Opens products file and loops over all products appending the ids of them
		file = open('products.json', 'r')
		products = json.loads(file.read())
		self.productids = []
		for product in products:
			self.productids.append(products[product]['ID'])
		file.close()

	def prodinfo(self, id):
		# Remove main gui and show product info gui passing the id of the product to display
		self.root.destroy()
		win2 = Tk()
		gui2 = Product(win2, id)

	def checkout(self):
		# check if cart has items
		if carttotal > 0:
			# display cart and remove main gui
			self.root.destroy()
			win3 = Tk()
			gui3 = Checkout(win3)
		else:
			# show errors
			if inventoryedit == False:
				messagebox.showerror("Error", "No Items in Cart")
			else:
				messagebox.showerror("Error", "No Items in Inventory")

	def editinv(self, button=False):
		global inventoryedit
		# check if function was called from button click or just called
		if button == False:
			# Re enable inventory edit after gui is shown again
			inventoryedit = True
			self.checkout.config(text="Update Inventory: %s" % carttotal)
			self.invedit.config(text="Customer View")
		else:
			# check if inventory edit is already on and if so turn it off or turn it on
			if inventoryedit == False:
				inventoryedit = True
				self.checkout.config(text="Update Inventory: %s" % carttotal)
				self.invedit.config(text="Customer View")
			else:
				inventoryedit = False
				self.checkout.config(text="Checkout: %s" % carttotal)
				self.invedit.config(text="Inventory Edit")

	def newproduct(self):
		# remove main gui and show add product gui
		self.root.destroy()
		win4 = Tk()
		gui = AddProduct(win4)

class Product:
	def __init__(self, master, id):
		# Initializing Main
		master.title('Kitchen Supply')
		self.root = master
		self.id = id

		# Get Product Info
		self.iteminfo(id)

		# Buttons and Labels
		framehold = Frame(master)
		id = Label(framehold, text='ID: %s' % id, width=20)
		id.grid(column=0, row=0, sticky=W)
		price = Label(framehold, text='Price: $%s' % self.price, width=20)
		price.grid(column=1, row=0)
		available = Label(framehold, text='Available: %s' % self.ammount, width=20)
		available.grid(column=2, row=0)
		framehold.grid(columnspan=4, row=0)
		desc = Label(master, text='Description: %s' % self.desc, width=40)
		desc.grid(columnspan=4, row=1)
		framehold2 = Frame(master)
		if self.attachid != None:
			attid = Label(framehold2, text='Attached ID: %s' % self.attachid, width=20)
			attid.grid(column=0, row=2)
		if self.material != None:
			material = Label(framehold2, text='Material: %s' % self.material, width=20)
			material.grid(column=1, row=2)
		framehold2.grid(columnspan=4, row=2)
		back = Button(master, text='Back', command=self.back, width=20)
		back.grid(column=0, row=3)
		ammount_lb = Label(master, text='Amount:', width=20)
		ammount_lb.grid(column=1, row=3)
		self.purchaseamm = Entry(master, width=20)
		self.purchaseamm.grid(column=2, row=3)
		self.purchaseamm.insert(0, 1)
		self.purchaseamm.focus_set()
		if inventoryedit == True:
			addcart = Button(master, text='Add to Inventory', command=self.addcart, width=20)
		else:
			addcart = Button(master, text='Add to Cart', command=self.addcart, width=20)
		addcart.grid(column=3, row=3)



		# Center
		windowWidth = master.winfo_reqwidth()
		windowHeight = master.winfo_reqheight()
		positionRight = int(master.winfo_screenwidth() / 2 - windowWidth * 1.5)
		positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
		master.geometry("+{}+{}".format(positionRight, positionDown))

	def iteminfo(self, productid):
		# Open products file and loop over all products until it gets the desired one then grabs info on product
		file = open('products.json', 'r')
		products = json.loads(file.read())
		for product in products:
			if products[product]['ID'] == productid:
				self.price = products[product]['Price']
				self.ammount = int(products[product]['Quantity'])
				self.desc = products[product]['Description']
				if products[product]['AttachedID'] != {}:
					self.attachid = products[product]['AttachedID']
				else:
					self.attachid = None
				if products[product]['Material'] != {}:
					self.material = products[product]['Material']
				else:
					self.material = None

		file.close()

	def back(self):
		# remove product info gui and show main gui
		self.root.destroy()
		win2 = Tk()
		gui = Main(win2)

	def addcart(self):
		# Check to see if the desired quantity is equal to or less than what is in stock
		amm = int(self.purchaseamm.get())
		global carttotal
		if self.ammount >= amm:
			# If item is in cart already then update the dictionary with the new quantity
			if self.id in cart:
				currentamm = cart[self.id] + amm
				if self.ammount >= currentamm:
					cart[self.id] = currentamm
					carttotal += amm
					messagebox.showinfo("Success", "%s of Item ID: %s Added to Cart" % (amm, self.id))
				else:
					if inventoryedit == False:
						messagebox.showerror("Error", "Not Enough Available")
					else:
						cart[self.id] = currentamm
						carttotal += amm
						messagebox.showinfo("Success", "%s of Item ID: %s Added to Inventory" % (amm, self.id))

			else:
				cart[self.id] = amm
				carttotal += amm
				if inventoryedit == False:
					messagebox.showinfo("Success", "%s of Item ID: %s Added to Cart" % (amm, self.id))
				else:
					messagebox.showinfo("Success", "%s of Item ID: %s Added to Inventory" % (amm, self.id))
		else:
			if inventoryedit == False:
				messagebox.showerror("Error", "Not Enough Available")
			else:
				cart[self.id] = amm
				carttotal += amm
				messagebox.showinfo("Success", "%s of Item ID: %s Added to Inventory" % (amm, self.id))


class Checkout:
	def __init__(self, master):
		# Initializing Account Select
		master.title('Checkout')
		self.root = master

		# Checkout total
		self.items = {}
		self.checkoutcost(False)

		# Change display text of button
		if inventoryedit == False:
			self.purchasetxt = 'Purchase: $%s' % format(self.cost, ".2f")
		else:
			self.purchasetxt = 'Update Inventory: %s' % carttotal



		# Buttons & Labels
		frame = Frame(master)
		back = Button(frame, text='Back', command=self.back, width=20)
		back.grid(column=0, row=0, sticky=W)
		pin_lb = Label(frame, text='Pin:', width=20)
		pin_lb.grid(column=1, row=0)
		self.pin = Entry(frame, width=20)
		self.pin.grid(column=2, row=0)
		self.purchase = Button(frame, text=self.purchasetxt, command=self.purchase1, width=20)
		self.purchase.grid(column=3, row=0)
		frame.grid(columnspan=10, row=0)

		# Show Cart
		col = 0
		row = 1
		stringVars = []
		for id in cart:
			stringVar = StringVar()
			stringVar.trace("w", self.checkoutcost)
			stringVars.append(stringVar)
			if col != 0:
				if col % 6 == 0:
					row += 1
					col = 0

			prod = Label(master, text='ID: %s' % id, width=20)
			prod.grid(column=col, row=row)
			col += 1
			entry = Entry(master, width=20, text=stringVar)
			entry.grid(column=col, row=row)
			entry.insert(0, cart[id])
			self.items[id] = entry
			col += 1


		# Center
		windowWidth = master.winfo_reqwidth()
		windowHeight = master.winfo_reqheight()
		if len(cart) > 2:
			positionRight = int(master.winfo_screenwidth() / 2 - windowWidth * 2)
		else:
			positionRight = int(master.winfo_screenwidth() / 2 - windowWidth * 1.5)
		positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
		master.geometry("+{}+{}".format(positionRight, positionDown))

		# Loop
		master.mainloop()

	def back(self):
		# Remove cart gui and show main gui
		self.root.destroy()
		win2 = Tk()
		gui = Main(win2)

	def checkoutcost(self, var=True, *args):
		# Check product file for price on each product in cart then multiply by the ammount of that product in cart
		file = open('products.json', 'r')
		products = json.loads(file.read())
		global carttotal
		global cart
		self.cost = 0
		empty = True
		if var == False:
			for product in products:
				if products[product]['ID'] in cart:
					amm = int(cart[products[product]['ID']])
					price = float(products[product]['Price'])
					totalprice = amm * price
					self.cost += totalprice

		else:
			for product in products:
				if products[product]['ID'] in self.items:
					try:
						empty = False
						entry = self.items[products[product]['ID']].get()
						amm = int(entry)
						price = float(products[product]['Price'])
						totalprice = amm * price
						self.cost += totalprice
						orig = cart[products[product]['ID']]
						cart[products[product]['ID']] = amm
						new = amm - orig
						if new < 0 and inventoryedit == False:
							del cart[products[product]['ID']]
						else:
							carttotal += new
					except:
						pass

			if empty == False:
				if inventoryedit == False:
					self.purchasetxt = 'Purchase: $%s' % format(self.cost, ".2f")
				else:
					self.purchasetxt = 'Update Inventory: %s' % carttotal
				self.purchase.config(text=self.purchasetxt)
		file.close()

	def purchase1(self):
		# Get user balance and pin
		global cart
		global carttotal
		csvfile = open('customers.csv', 'r')
		reader = csv.DictReader(csvfile)
		self.accounts = []
		for r in reader:
			if r['Name'] == user:
				bal = float(r['Balance'])
				pin = r['Pin']
		csvfile.close()

		# Check if in inventory edit mode
		if inventoryedit == False:

			# Check if all items in cart quantity is 0
			proceed = False
			for cartitem in cart:
				if cart[cartitem] != 0:
					proceed = True

			if proceed == False:
				messagebox.showinfo("Success", "Item(s) have been removed from the cart")
				cart = {}
				carttotal = 0
				self.root.destroy()
				win2 = Tk()
				gui = Main(win2)

			else:
				# Check pin
				if pin == self.pin.get():
					# Get checkout total cost
					self.checkoutcost()
					# Check if user can afford
					if bal >= self.cost:
						# Get order log info
						with open('order_log.json') as file:
							data = json.load(file)

						date = str(datetime.now())

						# Create new key by checking the last key value and add one
						try:
							key = "Order" + str(int(list(data.keys())[-1][5:]) + 1)
						except:
							# First order ever logged
							key = "Order1"

						# Check if item quantity not specified and if so delete it from cart
						for item in self.items:
							if self.items[item].get() == '':
								del cart[item]

						# Add new entry to order log
						data.update({key: {"Name": user, "DateTime": date, "TotalPaid": format(self.cost, ".2f"), "Products": cart}})
						with open('order_log.json', 'w') as file:
							json.dump(data, file)

						# Update user balance
						with open('customers.csv', 'r') as input:
							reader = csv.reader(input)
							lines = list(reader)
							for r in lines:
								if r[2] == user:
									r[3] = format(bal - self.cost, ".2f")
							with open('customers.csv', 'w', newline='') as output:
								writer = csv.writer(output)
								writer.writerows(lines)


						# Load product info
						with open("products.json", "r") as file:
							data = json.load(file)

						# Update products' quantity
						for item in data:
							if data[item]['ID'] in cart:
								orig = int(data[item]["Quantity"])
								newval = orig - int(cart[data[item]['ID']])
								data[item]["Quantity"] = newval

						# Save
						with open("products.json", "w") as jsonFile:
							json.dump(data, jsonFile)


						# Show user info, reset variables for next use, remove cart gui and display main gui
						messagebox.showinfo("Success", "Purchase has been Processed")
						cart = {}
						carttotal = 0
						self.root.destroy()
						win2 = Tk()
						gui = Main(win2)

					else:
						messagebox.showerror("Error", "Not Enough Funds")
				else:
					messagebox.showerror("Error", "Invalid Pin")

		else:
			# Check pin
			if pin == self.pin.get():

				# Load product info
				with open("products.json", "r") as file:
					data = json.load(file)

				# Check if item quantity not specified and if so set it to 0
				for item in self.items:
					if self.items[item].get() == '':
						cart[item] = 0

				# Update products' quantity
				for item in data:
					if data[item]['ID'] in cart:
						data[item]["Quantity"] = cart[data[item]['ID']]

				# Save
				with open("products.json", "w") as jsonFile:
					json.dump(data, jsonFile)

				# Show user info, reset variables for next use, remove cart gui and display main gui
				messagebox.showinfo("Success", "Inventory has been Updated")
				cart = {}
				carttotal = 0
				self.root.destroy()
				win2 = Tk()
				gui = Main(win2)
			else:
				messagebox.showerror("Error", "Invalid Pin")

class AddProduct:
	def __init__(self, master):
		# Initializing Main
		master.title('Kitchen Supply')
		self.root = master

		# Buttons and Labels
		frame = Frame(master)
		id_lb = Label(frame, text='*ID:', width=20)
		id_lb.grid(column=0, row=0)
		self.id = Entry(frame, width=20)
		self.id.grid(column=1, row=0)
		price_lb = Label(frame, text='*Price:', width=20)
		price_lb.grid(column=2, row=0)
		self.price = Entry(frame, width=20)
		self.price.grid(column=3, row=0)
		frame.grid(columnspan=6, row=0)
		quantity_lb = Label(master, text='*Quantity:', width=20)
		quantity_lb.grid(column=0, row=1)
		self.quantity = Entry(master, width=20)
		self.quantity.grid(column=1, row=1)
		attachid_lb = Label(master, text='Attached ID:', width=20)
		attachid_lb.grid(column=2, row=1)
		self.attachid = Entry(master, width=20)
		self.attachid.grid(column=3, row=1)
		material_lb = Label(master, text='Material:', width=20)
		material_lb.grid(column=4, row=1)
		self.material = Entry(master, width=20)
		self.material.grid(column=5, row=1)
		desc_lb = Label(master, text='*Description:', width=20)
		desc_lb.grid(columnspan=6, row=2)
		self.desc = Entry(master, width=100)
		self.desc.grid(columnspan=6, row=3)
		back = Button(master, text='Back', command=self.back, width=20)
		back.grid(column=0, row=4)
		add = Button(master, text='Add Product', command=self.addprod, width=20)
		add.grid(column=5, row=4)

		# Center
		windowWidth = master.winfo_reqwidth()
		windowHeight = master.winfo_reqheight()
		positionRight = int(master.winfo_screenwidth() / 2 - windowWidth * 2)
		positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
		master.geometry("+{}+{}".format(positionRight, positionDown))

	def back(self):
		# remove add product gui and show main gui
		self.root.destroy()
		win2 = Tk()
		gui = Main(win2)

	def addprod(self):
		# Grab all entry values
		id = self.id.get()
		price = self.price.get()
		quantity = self.quantity.get()
		attachid = self.attachid.get()
		material = self.material.get()
		desc = self.desc.get()

		# Check if entry values not specified
		if id == '':
			messagebox.showerror("Error", "ID is required")
			return
		if price == '':
			messagebox.showerror("Error", "Price is required")
			return
		if quantity == '':
			messagebox.showerror("Error", "Quantity is required")
			return
		if desc == '':
			messagebox.showerror("Error", "Description is required")
			return
		if attachid == '':
			attachid = {}
		if material == '':
			material = {}

		# Load products info
		with open('products.json') as file:
			data = json.load(file)

		# Create new key by checking the last key value and add one
		try:
			key = "Prod" + str(int(list(data.keys())[-1][4:]) + 1)
		except:
			# First order ever logged
			key = "Prod1"

		# Add new product
		data.update({key: {"ID": id, "Price": price, "Description": desc, "Quantity": quantity, 'AttachedID': attachid, 'Material': material}})

		# Save
		with open('products.json', 'w') as file:
			json.dump(data, file)

		# Show user info, reset all entry fields for next use
		messagebox.showinfo("Success", "Product has been added")
		self.id.delete(0, 'end')
		self.price.delete(0, 'end')
		self.quantity.delete(0, 'end')
		self.attachid.delete(0, 'end')
		self.material.delete(0, 'end')
		self.desc.delete(0, 'end')


# Start Account Select Gui
win = Tk()
gui = AccountSelect(win)