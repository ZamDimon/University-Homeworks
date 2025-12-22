import numpy as np

class Client:
    def __init__(self, inputs, desired_outputs):
        assert len(inputs) == len(desired_outputs), "Inputs and outputs sets must be of the same size"
        assert len(inputs) > 0, "At least something should be tested :)"
        
        self.inputs = inputs
        self.outputs = desired_outputs
        
    def print_wrong_answer(self, test_number, expected_value, input_value, actual_output):
        print("#{}: WRONG ANSWER, expected {} for {}, got {}".format(test_number, expected_value, input_value, actual_output))
    
    def print_unexpected_behaviour(self, test_number):
        print("#{}: UNEXPECTED BEHAVIOUR".format(test_number))
    
    def print_correct_answer(self, test_number):
        print("#{}: CORRECT ANSWER".format(test_number))
    
    def test(self, tested_function_name, tested_function):
        print("Testing {}...".format(tested_function_name))
        
        for k in range(len(self.inputs)):
            actual_output = None
            
            try:
                actual_output = tested_function(self.inputs[k])
            except:
                self.print_unexpected_behaviour(k)
                continue
            
            actual_output_np = np.array(actual_output)
            real_output_np = np.array(self.outputs[k])
            
            if not (actual_output_np.shape == real_output_np.shape):
                self.print_wrong_answer(k, self.outputs[k], self.inputs[k], actual_output)
                continue
            if not (actual_output_np == real_output_np).all():
                self.print_wrong_answer(k, self.outputs[k], self.inputs[k], actual_output)
                continue
            
            self.print_correct_answer(k)