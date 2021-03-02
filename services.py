import sys
import models

def read_file(argv):
    if not len(argv) == 2:
        raise Exception("Please input 1 and only 1 input file.")
    filename = argv[1]

    with open(filename, 'r') as input_file:
        lines = input_file.readlines()
        data = [row.strip() for row in lines]
        return data

def read_file_test(testfilename):
    print('- - - - - TESTING MODE ON - - - - -')
    with open(testfilename, 'r') as input_file:
        lines = input_file.readlines()
        data = [row.strip() for row in lines]
        return data

def import_data(data, trainee_count):
    total_registers = int(data[0])
    if total_registers < trainee_count:
        raise Exception('Assigned too many trainees for the registers!\nRegisters: {} | Trainees: {}'.format(total_registers, trainee_count))

    store_state = {}
    register_map = {}
    for i, x in enumerate(range(1, total_registers + 1)):
        register_id = x
        store_state[register_id] = []
        if i < total_registers - trainee_count:
            register_map[register_id] = models.Register(register_id, 'expert')
        else:
            register_map[register_id] = models.Register(register_id, 'trainee')

    customerpool = []
    for i,row in enumerate(data[1:]):
        x = row.split()
        customer = models.Customer(i+1, x[0], float(x[1]), float(x[2]))
        customerpool.append(customer)
        customerpool.sort(key=lambda x: (x.c_start, x.c_items, x.c_type))  # sorts first by smallest to largest time, least to greatest item count, then alphabetically from A > B

    return store_state, register_map, customerpool

def add_customers(t, store_state, customerpool):
    updatedpool = []
    for customer in customerpool:
        if customer.c_start != t:
            updatedpool.append(customer)
        else:
            customer_added = False
            for register in store_state:  # customer joins first empty line if there is one
                if store_state[register] == []:
                    store_state[register].append(customer)
                    customer_added = True
                    break
            if customer_added:
                continue
            else:
                if customer.c_type == 'A':  # customer chooses register with shortest number of customers in line, defaulting to the lower id# if there is a tie
                    reg_customer_count = {key: len(value) for key, value in store_state.items()}
                    shortestline = min(reg_customer_count, key=reg_customer_count.get)
                    store_state[shortestline].append(customer)
                elif customer.c_type == 'B':  # customer chooses register whose last customer in line has the fewest items, defaulting to the lower id# if there is a tie
                    lastcustomer_items = {key: value[-1].c_items for key, value in store_state.items()}
                    leastitems = min(lastcustomer_items, key=lastcustomer_items.get)
                    store_state[leastitems].append(customer)

    return store_state, updatedpool



def onemin_operation(store_state, register_map, register_rates):  # TODO cashier only operates on the first person in line!
    for register in store_state:
        if len(store_state[register]) != 0:
            minperitem = register_rates[register_map[register].r_type]
            store_state[register][0].c_items -= 1/minperitem
            if store_state[register][0].c_items == 0:
                store_state[register].pop(0)

def check_status(store_state, customerpool):
    remainingcustomers = len(customerpool)
    for register in store_state:
        remainingcustomers += len(store_state[register])
        print('Register [{}]:'.format(register))
        for customer in store_state[register]:
            print('\tCustomer ID: {} | type: {} | start: {} | items: {}'.format(
                customer.c_id,
                customer.c_type,
                customer.c_start,
                customer.c_items
            ))
    print('Customer pool:')
    for customer in customerpool:
        print('\tCustomer ID: {} | type: {} | start: {} | items: {}'.format(
            customer.c_id,
            customer.c_type,
            customer.c_start,
            customer.c_items
        ))
    print('TOTAL remaining customers: ' + str(remainingcustomers) + '\n')
    return remainingcustomers