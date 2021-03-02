import sys
from collections import OrderedDict
import services

class Simulation:

    def __init__(self):

        """The parameters below store dynamic data during the script."""
        self.store_state = OrderedDict()
        self.register_map = {}
        self.customerpool = []


        """The parameters below can be adjusted for testing."""
        self.trainee_count = 1  # Can be adjusted to see how much more time this process will take with more trainees.
        self.register_rates = {  # Additional employee types can be added
            'expert': 1,
            'trainee': 2,
        }
        self.testing = False
        self.testfilename = ''


    def run(self):
        if self.testing:
            data = services.read_file_test(self.testfilename)
        else:
            data = services.read_file(sys.argv)

        store_state, register_map, customerpool = services.import_data(data, self.trainee_count)

        t = 0
        while True:
            print('- - - - - - - TIME = ' + str(t) + ' - - - - - - -')
            store_state, customerpool = services.add_customers(t, store_state, customerpool)
            if services.check_status(store_state, customerpool) == 0:
                break
            services.onemin_operation(store_state, register_map, self.register_rates)
            t += 1
        print('Finished at: t={} minutes'.format(t))


s = Simulation()
s.run()