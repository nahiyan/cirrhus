from threading import Thread

# print(threading.activeCount())
# print(threading.currentThread())
# print(threading.enumerate())


def alternate_numbers(number):
	print(number)

	if number < 100:
		alternate_numbers(number + 2)


class AlternateNumber (Thread):
    def __init__(self, starting_number):
        Thread.__init__(self)
        # self.threadID = counter
        # self.name = name
        # self.counter = counter
        self.starting_number = starting_number

    def run(self):
        print("Starting " + self.name)
        alternate_numbers(self.starting_number)
        print("Exiting " + self.name)


# Create new threads
thread1 = AlternateNumber(1)
thread2 = AlternateNumber(2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()