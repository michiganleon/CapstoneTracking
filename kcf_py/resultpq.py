from Queue import PriorityQueue

class ReusltQueue(PriorityQueue):
	def __init__(self, limit):
		PriorityQueue.__init__(self)
		self.counter = 0
		self.upperlimmit = limit
		self.lowesrscore = 0

	def put(self, item):
		if (item[4] > self.lowesrscore):
			PriorityQueue.put(self, (item[4], self.counter, item))
			self.counter += 1
			if(self.counter == 1):
				self.lowesrscore = item[4]

			if(self.counter > self.upperlimmit):
				while((self.counter > self.upperlimmit) and (PriorityQueue.empty(self) == False)):
					PriorityQueue.get(self)
					self.counter = self.counter - 1
				new_small = PriorityQueue.get(self)[2]
				self.lowesrscore = new_small[4]
				PriorityQueue.put(self, (new_small[4], self.counter, new_small))
	
	def show(self):
		result = []
		while(PriorityQueue.empty(self) == False):
			result.append(PriorityQueue.get(self))
		return result


def resultQ(limit):
	return ReusltQueue(limit)



