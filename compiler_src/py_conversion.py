
from typing import List

def assert_options(assertions_list, options):
    for a in assertions_list:
        if a not in options:
            raise Exception("Missing Option: " + a)


class DataSet:
    def __init__(self,label):
        self.label = label
        self.data_split = None
        self.target_var = None
        self.src_file_type = None

    #TODO: make all the functions accept inputs in the way defined here
    #all functions must take in 
    def create(self, options):
        '''
        options: Dictionary containing the following options
        o_type: .csv
        o_target: 'mpg'
        o_from: '/home/pratik/source.csv'
        '''
        assert_options(['from','type'],options)
        if 'target' in options:
            self.target_var = options['target'][0]
        #currently supporting only .csv
        self.src_file_type = options['type']
        return  ["{label} = pd.read_csv('{src}')".format(label=self.label, src=options['from'])]
    
    def display(self, o_num_rows):
        '''
        o_num_rows: 10 (rows to display)
        '''
        return ["{label}.head({rows})".format(label=self.label,rows = o_num_rows)]
    
    def modify(self, o_delete_col=None):
        '''
        o_delete_col = ['col1','col2']
        '''
        py_text = []
        if o_delete_col:
            py_text.append("{label}.drop({cols},axis=1)".format(label = self.label, cols=str(o_delete_col)))
        
        return py_text
    
    def preprocess(self, o_fillnan=None):
        '''
        o_fillna: [('col1','median'),('col2','mean')]
        '''
        py_text = []
        if o_fillnan:
            for fill in o_fillnan:
                py_text.append("{label}['{col}'].fillna({label}['{col}'].{strategy}(),inplace=True)".format(label = self.label, col=fill[0],strategy=fill[1]))
        
        return py_text
    
    def split(self, o_test_size):
        '''
        test_size: 0.2
        '''
        if not self.target_var:
            raise Exception('Target variable not defined')
        py_text = []
        if o_test_size:
            py_text.append("{label}_Y = {label}[['{target_var}']]".format(label=self.label, target_var = self.target_var))
            py_text.append("{label}_X = {label}.drop('{target_var}', axis = 1)".format(label=self.label, target_var = self.target_var))
            py_text.append("{label}_X_train, {label}_X_test, {label}_Y_train, {label}_Y_test = train_test_split({label}_X,{label}_Y,test_size={test_size})".format(label=self.label, test_size = o_test_size))
            self.data_split = {
                'X_train': "{label}_X_train".format(label=self.label),
                'Y_train': "{label}_Y_train".format(label=self.label),
                'X_test': "{label}_X_test".format(label=self.label),
                'Y_test': "{label}_Y_test".format(label=self.label)
            }

        return py_text


        
class Model:
    def __init__(self,label):
        self.label = label
        self.models_enabled = [] #[{'model_name':'model1','model_class':'linear-regresison','model_type':'regression'}]
    
    def create(self, o_models:List[str], o_dataset:DataSet):
        '''
        o_models: ['Linear-Regression','Decision-Tree-Regressor']
        o_dataset: DataSet object for the data to be used for fitting the regression
        '''
        self.dataset = o_dataset
        py_text = []
        #checking if data has been split
        if not self.dataset.data_split:
            #can throw warning here that model is being fit without defining the size of the training and testing data
            self.dataset.split(0.2)
            pass
        
        for m in o_models:
            #current supporting only Linear-Regression
            if m == 'linear-regression':
                py_text.append("{label}_linreg = LinearRegression()".format(label = self.label))
                py_text.append("{label}_linreg.fit({train},{test})".format(label = self.label, train = self.dataset.data_split['X_train'], test = self.dataset.data_split['Y_train']))
                self.models_enabled.append({'model_name':'{label}_linreg'.format(label = self.label),'model_class':'linear-regression', 'model_type':'regression'}) #regression model - udes to identify the type of model so that 
            
            
        return py_text



class Metrics:
    def __init__(self, label):
        self.label = label

    def display(self, o_from:Model):
        '''
        o_from: Model object whose metrics must be tested
        '''
        self.model = o_from
        py_text = []
        for m in o_from.models_enabled:
            #metrics display depends on whether the model is classification or whether it is a regression model
            if m['model_type'] == 'regression':
                #compute R2 and MSE
                py_text.append("{data_label}_Y_pred = {model_name}.predict({testing_set})".format(data_label = self.model.dataset.label, 
                                                                                                    model_name = m['model_name'],
                                                                                                    testing_set = self.model.dataset.data_split['X_test']))
                py_text.append("{model_name}_mse = mean_squarred_error({Y_test},{data_label}_Y_pred)".format(model_name = m['model_name'],
                                                                                                                 Y_test=self.model.dataset.data_split['Y_test'],
                                                                                                                 data_label = self.model.dataset.label))
                py_text.append("{model_name}_r2 = r2_score({Y_test},{data_label}_Y_pred)".format(model_name = m['model_name'],
                                                                                                                 Y_test=self.model.dataset.data_split['Y_test'],
                                                                                                                 data_label = self.model.dataset.label))
                py_text.append("print('Testing Set R2 Score for {model_class}',{model_name}_r2)".format(model_class=m['model_class'],model_name=m['model_name']))
                py_text.append("print('Testing Set MAE for {model_class}',{model_name}_mse)".format(model_class=m['model_class'],model_name=m['model_name']))
        
        return py_text






if __name__ == "__main__":
    data = DataSet('auto1')
    py_text = []
    py_text += data.create('/home/pratik/data1.csv',o_target='mpg')
    py_text += data.display(10)
    py_text += data.modify(o_delete_col = ['car name'])
    py_text += data.preprocess(o_fillnan=[('horsepower','median')])
    py_text += data.split(o_test_size=0.2)

    models = Model('regModels')
    py_text += models.create(['linear-regression'], data)

    metrics = Metrics('regMetrics')
    py_text += metrics.display(models)


    for text in py_text:
        print(text)




            
