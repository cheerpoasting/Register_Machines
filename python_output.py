class Register:
	def __init__(self, name):
		self.name = name
		self.value=0

	def increment(self):
		self.value += 1
	def decrement(self):
		self.value -= 1
		if self.value < 1:
			self.value = 0

A = Register("A")
B = Register("B")

A.increment()
B.increment()
B.decrement()
B.decrement()

print(A.value)
print(B.value)
