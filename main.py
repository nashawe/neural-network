import numpy as np
from models.network import NeuralNetwork
from utils.activation import sigmoid, deriv_sig, tanh, deriv_tanh, relu, deriv_relu #imports all activation functions
from utils.loss import mse_loss, bce_loss  #imports all loss functions
from utils.winit import random_init, xavier_init, he_init

def clipped_bce_grad(y_pred, y_true, eps=1e-7): #defined as seperate function because BCE can cause issues if not clipped.
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return (y_pred - y_true) / (y_pred * (1 - y_pred))

WEIGHT_INITS = {
    1: random_init,
    2: xavier_init,
    3: he_init,
}

#dictionary of dictionaries for each component of each mode that can be selected.
MODES = {
    1: {  # Sigmoid + MSE
        "hidden_activation": sigmoid,
        "hidden_deriv": deriv_sig,
        "output_activation": sigmoid,
        "output_deriv": deriv_sig,
        "loss": mse_loss,
        "loss_grad": lambda y_pred, y_true: 2 * (y_pred - y_true),
        "normalize": True,
    },
    2: {  # Sigmoid + Binary Cross-Entropy
        "hidden_activation": sigmoid,
        "hidden_deriv": deriv_sig,
        "output_activation": sigmoid,
        "output_deriv": deriv_sig,
        "loss": bce_loss,
        "loss_grad": clipped_bce_grad,
        "normalize": True,
    },
    3: {  # Tanh + MSE
        "hidden_activation": tanh,
        "hidden_deriv": deriv_tanh,
        "output_activation": tanh,
        "output_deriv": deriv_tanh,
        "loss": mse_loss,
        "loss_grad": lambda y_pred, y_true: 2 * (y_pred - y_true),
        "normalize": False,
    },
    4: {  # ReLU + Sigmoid + Binary Cross-Entropy
        "hidden_activation": relu,
        "hidden_deriv": deriv_relu,
        "output_activation": sigmoid, #different than hidden activation because ReLu doesn't work for output neuron.
        "output_deriv": deriv_sig, 
        "loss": bce_loss,
        "loss_grad": clipped_bce_grad,
        "normalize": True,
    },
}

if __name__ == '__main__':
    # User input for network parameters and training data
    print("Choose a model setup (activation function + loss function):")
    print("1 - Sigmoid + Mean Squared Error (Good for regression or simple binary classification; not ideal for probabilities)")
    print("2 - Sigmoid + Binary Cross-Entropy (Best for binary classification; outputs are probabilities)")
    print("3 - Tanh + Mean Squared Error (Works for values between -1 and 1; can suffer from vanishing gradients)")
    print("4 - ReLU (hidden) + Sigmoid (output) + Binary Cross-Entropy (Fast and accurate for deeper models)")
    
    
    model_setup = int(input("Enter the number of your chosen setup (1-4): "))
    config = MODES[model_setup]
    
    if model_setup == 1:
        print_model = "Sigmoid + Mean Squared Error"
    elif model_setup == 2:
        print_model = "Sigmoid + Binary Cross-Entropy"
    elif model_setup == 3:
        print_model = "Tanh + Mean Squared Error"
    elif model_setup == 4:
        print_model = "ReLU (hidden) + Sigmoid (output) + Binary Cross-Entropy"    
        
    input_size = int(input("Enter the number of inputs per sample (if using default dataset, input 3): "))
    
    bs = input("Would you like to use Mini-Batch training? (y/n) ")
    if bs == "y":
        bsize = int(input("How many samples per mini-batch? (eg. 16, 32, 64) "))
    elif bs == "n":
        print("Ok. Model will be trained on each sample, one by one.")
    else:
        print("Not a valid answer. Please pick y or n.")
        bs = input("Would you like to use Mini-Batch training? (y/n) ")
        
    do = input("Would you like to use dropout? (y/n) ")
    if do == "y":
        dropout_rate = float(input("Enter dropout rate (e.g., 0.2 for 20% dropout) "))
    elif do == "n":
        print("Ok. Model will not use dropout and all neurons will be used 100% of the time.")
    else:
        print("Not a valid answer. Please pick y or n.")
        do = input("Would you like to use dropout? (y/n) ")
    
    print("Choose a weight initialization setup:")
    print("1 - Random weight initialization")
    print("2 - Xavier weight initialization")
    print("3 - He weight initialization")
        
    init_method = int(input("Enter the number of your chosen weight initialization method (1-3): "))
    weight_init = WEIGHT_INITS[init_method]
    
    if init_method == 1:
        init_print = "Random weight initialization"
    elif init_method == 2:
        init_print = "Xavier weight initialization"
    elif init_method == 3:
        init_print = "He weight initialization"
    
    num_layers = int(input("Enter the number of hidden layers: "))
    hidden_size = int(input("Enter the number of hidden neurons: "))
    learn_rate = float(input("Enter the learning rate (e.g., 0.05): "))
    
    print("Choose an optimizer:")
    print("1 - Gradient Descent (Vanilla)")
    print("2 - RMSprop")
    print("3 - Adam")
    optimizer_choice = int(input("Enter the number of your chosen optimizer: "))
    
    if optimizer_choice == 1:
        print_opt = "Gradient Descent (Vanilla)"
    elif optimizer_choice == 2:
        print_opt = "RMSprop"
    elif optimizer_choice == 3:
        print_opt = "Adam"
    
    epochs = int(input("Enter the number of epochs for training: "))

    print("Do you want to use the default dataset? (y/n)")
    use_default = input().strip().lower()
    
    if use_default == "y":
        data_lines = [
            "1,2,1",
            "2,4,2",
            "3,3,1",
            "4,5,3",
            "5,5,5",
            "6,4,6",
            "7,6,6",
            "8,7,7",
            "9,8,8",
            "10,9,9",
            "1,1,0",
            "2,2,1",
            "3,1,2",
            "4,2,1",
            "5,3,2",
            "6,2,3",
            "7,3,4",
            "8,4,5",
            "9,5,6",
            "10,6,7",
            "1,0,0",
            "2,1,1",
            "3,2,1",
            "4,3,2",
            "5,4,2",
            "6,5,3",
            "7,5,4",
            "8,6,5",
            "9,7,5",
            "10,8,6"
        ]
        labels_input = "0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1"
    else:
        # Get training data block input
        print("\nPaste your training data here.")
        print("Each line should represent a sample with comma-separated values.")
        print("When you're done, enter an empty line to finish:")
        data_lines = []
        
        while True:
            line = input()
            if line.strip() == "":
                break
            data_lines.append(line)
        
        labels_input = input("\nPaste the labels for each sample, separated by commas: ")

    # Parse the data
    data = np.array([[float(value.strip()) for value in line.split(',')] for line in data_lines])
    labels = np.array([float(label.strip()) for label in labels_input.split(',')], dtype=np.float64)

    # Optional normalization
    if config.get("normalize"):
        data = data / 10.0
      
    # Create and train the neural network
    network = NeuralNetwork(input_size, hidden_size, num_layers, config, dropout_rate=dropout_rate if do == "y" else 0, init_fn=weight_init)
    network.train(data, labels, learn_rate=learn_rate, epochs=epochs)
    print(f"\nTraining complete. The model used:\nMode: {print_model}\nNumber of inputs: {input_size}\nMini-batch size: {bsize}\nDropout rate: {dropout_rate}\nWeight Initialization: {init_print}\nOptimizer function: {print_opt}\nNumber of hidden layers: {num_layers}\nNumber of neurons per layer: {hidden_size}\nLearning rate: {learn_rate}\nNumber of epochs: {epochs}")
    
    # Ask the user if they'd like to test the model
    test_choice = input("Would you like to test the model with new data? (y/n): ").strip().lower()
    if test_choice == 'y':
        print("\nPaste your test data here (each line is a sample, comma-separated values).")
        print("When you're done, enter an empty line to finish:")
        test_data_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            test_data_lines.append(line)
        test_data = np.array([[float(value.strip()) for value in line.split(',')] for line in test_data_lines])
        if config.get("normalize"):
            test_data = test_data / 10.0

        print("\nModel predictions:")
        for sample in test_data:
            prediction = network.feedforward(sample)
            print(f"Input: {sample} so prediction: {prediction}")
    else:
        print("Testing skipped. Good job on training your model!")
