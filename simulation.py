import sys


class Simulation:

    def __init__(self):

        '''The parameters below store dynamic data during the script.'''
        self.store_state = {}
        self.register_map = {}
        self.customerpool = []

        '''The parameters below can be adjusted for testing.'''
        self.trainee_count = 1
        self.testing = True
        self.testfilename = 'testcases/test05.txt'


    class Customer:

        def __init__(self, c_type, c_start, c_items):
            self.c_type = c_type
            self.c_start = c_start
            self.c_items = c_items
            self.timeremaining = 0

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
        f = [row.strip() for row in f]
        print(f)

        total_registers = int(f[0])  # TODO catch error for too many trainees for number of registers
        for i, x in enumerate(range(total_registers, 0, -1)):
            register_id = x
            self.store_state[register_id] = []
            if i < self.trainee_count:
                self.register_map[register_id] = self.Register(register_id, 'trainee')
            else:
                self.register_map[register_id] = self.Register(register_id, 'expert')

        for row in f[1:]:
            x = row.split()
            customer = self.Customer(x[0], int(x[1]), int(x[2]))
            self.customerpool.append(customer)
            self.customerpool.sort(key=lambda x: (x.c_start, x.c_items, x.c_type))  # sorts first by smallest to largest time, least to greatest item count, then alphabetically from A > B

    def add_customers(self, t, customer, register):
        # customer needs to select which register they join based on self.store_state
        # assign customers' "timeremaining" attribute based on customer's item count and whether the cashier is in-training or not
        for i, customer in enumerate(self.customerpool):
            if customer.c_start == t:
                self.customerpool.pop(i)


    def onemin_operation(self):
        for register in self.store_state:
            if len(self.store_state[register]) != 0:
                for i, customer in enumerate(self.store_state[register]):
                    customer.timeremaining -= 1
                    if customer.timeremaining == 0:
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