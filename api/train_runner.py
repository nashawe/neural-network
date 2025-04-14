import numpy as np
from models.network import NeuralNetwork #import the entire object with all of its functions (training, testing, etc)
from utils.config import MODES
from utils.winit import random_init, xavier_init, he_init

WEIGHT_INITS = {
    1: random_init,
    2: xavier_init,
    3: he_init,
}

def run_training_from_api( #setup function for API
    input_size,
    output_size,
    hidden_size,
    num_layers,
    dropout,
    optimizer_choice,
    mode_id,
    batch_size,
    learning_rate,
    epochs,
    data,
    labels
):
    # Get correct config and init function
    config = MODES[mode_id] #based on what user chose
    init_fn = WEIGHT_INITS[1]  # Default to random
    if mode_id in WEIGHT_INITS: 
        init_fn = WEIGHT_INITS[mode_id]

    # One-hot encode if needed
    if mode_id == 5: #if multi-class 
        def to_one_hot(index, num_classes):  #encode data in away computer can read
            one_hot = np.zeros(num_classes)
            one_hot[int(index)] = 1.0
            return one_hot
        labels = [to_one_hot(label, output_size) for label in labels] #new labels is the ones that have been encoded

    # Normalize if needed
    data = np.array(data, dtype=np.float64)
    labels = np.array(labels, dtype=np.float64)

    if config.get("normalize"): #if the mode the user chose calls for normalization, then normalize the data
        data = data / 10.0

    # Create and train model
    network = NeuralNetwork(
        input_size=input_size,
        hidden_size=hidden_size,
        num_layers=num_layers,
        output_size=output_size,
        config=config,
        dropout_rate=dropout,
        init_fn=init_fn,
        optimizer_choice=optimizer_choice
    )

    network.train(data, labels, learn_rate=learning_rate, epochs=epochs, bsize=batch_size)

    # You can return any metrics you want here
    return {
        "message": "Training complete",
        "samples": len(data),
        "epochs": epochs,
        "mode": mode_id,
        "output_size": output_size,
        "loss_history": network.loss_history,
        "accuracy_history": network.accuracy_history,
    }
