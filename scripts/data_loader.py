import os.path
from os import path
from tdc.multi_pred import DDI



'''
from tdc.multi_pred import DDI
data = DDI(name = 'DrugBank')
split = data.get_split()
'''

DATA_DIR = '../data'

TRAIN_DIR = f'{DATA_DIR}/train.csv'
VALID_DIR = f'{DATA_DIR}/valid.csv'
TEST_DIR = f'{DATA_DIR}/test.csv'

#OUTPUT_DIR = f'{DATA_DIR}/output'

class DataLoader:
    def __init__(self):
        self.data = None
        self.split = None
        self.train_data = None
        self.valid_data = None
        self.test_data = None
        

    def load_data(self):
        try:
            print('downloading data')
            self.data = DDI(name = 'DrugBank')
            self.split = self.data.get_split()
            [self.train_data, self.test_data, self.valid_data] = self.split['train'], self.split['test'], self.split['valid']
            print('data downloaded')
            return self.train_data.to_csv(TRAIN_DIR), self.valid_data.to_csv(VALID_DIR), self.test_data.to_csv(TEST_DIR)

        except Exception as e:
           print(f'The following error occured: {e}')

            
DataLoader().load_data()
    

       
          
    
        
    
    