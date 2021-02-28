import sys
from collections import OrderedDict


class Simulation:

    def __init__(self):

        """The parameters below store dynamic data during the script."""
        self.store_state = OrderedDict()
        self.register_map = {}
        self.register_rates = {
            'expert': 1,  # expert takes 1 min to process 1 item
            'trainee': 2,  # trainee takes 2 min to process 1 item
        }
        self.customerpool = []

        """The parameters below can be adjusted for testing."""
        self.trainee_count = 1
        self.testing = True
        self.testfilename = 'testcases/test05.txt'


    class Customer:

        def __init__(self, c_type, c_start, c_items):
            self.c_type = c_type
            self.c_start = c_start
            self.c_items = c_items

    class Register:

        def __init__(self, r_id, r_type):
            self.r_id = r_id
            self.r_type = r_type


    def read_file(self):
        if self.testing:
            print('Testing mode on.')
            filename = self.testfilename
        else:
            print('Testing mode off.')
            if not len(sys.argv) == 2:
                raise Exception("Please input 1 and only 1 input file.")
            filename = sys.argv[1]

        f = open(filename, 'r').readlines()
        data = [row.strip() for row in f]
        f.close()
        print(data)

        total_registers = int(data[0])  # TODO catch error for too many trainees for number of registers
        for i, x in enumerate(range(1, total_registers + 1)):
            register_id = x
            self.store_state[register_id] = []
            if i < total_registers - self.trainee_count:
                self.register_map[register_id] = self.Register(register_id, 'expert')
            else:
                self.register_map[register_id] = self.Register(register_id, 'trainee')

        for row in data[1:]:
            x = row.split()
            customer = self.Customer(x[0], int(x[1]), int(x[2]))
            self.customerpool.append(customer)
            self.customerpool.sort(key=lambda x: (x.c_start, x.c_items, x.c_type))  # sorts first by smallest to largest time, least to greatest item count, then alphabetically from A > B

    def add_customers(self, t, customer, register):
        # customer needs to select which register they join based on self.store_state
        for i, customer in enumerate(self.customerpool):
            if customer.c_start == t:
                self.customerpool.pop(i)
                for register in self.store_state:  # customer joins first empty line if there is one
                    customer_added = False
                    if self.store_state[register] == []:
                        self.store_state[register].append(customer)
                        customer_added = True
                        break
                if customer_added:
                    continue
                else:
                    if customer.c_type == 'A':  # customer chooses register with shortest number of customers in line, defaulting to the lower id# if there is a tie
                        reg_customer_count = {key: len(value) for key, value in self.store_state.items()}
                        shortestline = min(reg_customer_count, key=reg_customer_count.get)
                        self.store_state[shortestline].append(customer)
                    elif customer.c_type == 'B':  # customer chooses register whose last customer in line has the fewest items, defaulting to the lower id# if there is a tie
                        lastcustomer_items = {key: value[-1].c_items for key, value in self.store_state.items()}
                        leastitems = min(lastcustomer_items, key=lastcustomer_items.get)
                        self.store_state[leastitems].append(customer)

    def onemin_operation(self):
        for register in self.store_state:
            if len(self.store_state[register]) != 0:
                for i, customer in enumerate(self.store_state[register]):
                    customer.c_items -= 1/self.register_rates[register.r_type]
                    if customer.c_items == 0:
                        self.store_state[register].pop(i)

    def remainingcustomers(self):
        remainingcustomers = len(self.customerpool)
        for register in self.store_state:
            remainingcustomers += (self.store_state[register])
        return remainingcustomers

    def run(self):
        t = 0
        while True:
            # add customers that have c_start = 0... evaluate which register they join based on parameters
            self.add_customers(t)
            self.onemin_operation
            t += 1
            if self.remainingcustomers() == 0:
                print('No more customers in the store.')
                break
            else:
                print('Remaining customers: ' + int(self.remainingcustomers()))

        print('Total time: ' + str(t))



s = Simulation()
s.read_file()
x = 5