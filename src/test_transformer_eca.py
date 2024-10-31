from numpy import ndarray, array, append

from predictors.neural_predictor.transformer import Transformer
from predictors.neural_predictor.train import train_model_with_target_indices #train_model_with_target_embeddings
from predictors.neural_predictor.predict import predict_n
from dynamical_system.eca.elementary_cellular_automata import ElementaryCellularAutomata
from utils_projection import projector
from utils_encoder import eca_encoder #, eca_decoder
from utils_plotting import plot_trajectories, plot_spacetime_diagrams#plot_spacetime_diagrams_binarised
#==========UTILITIES==================

def generate_dataset(
    lattice_width:int,
    batch_size:int,
    max_sequence_length:int
) -> tuple[ndarray, ndarray, list[int]]:
    
    cas = [
        ElementaryCellularAutomata(
            lattice_width=lattice_width,
            time_steps=max_sequence_length*2,
            transition_rule_number=3
        ) for _ in range(batch_size)
    ]

    original_to_mini_index_mapping = set()
    for ca in cas:
        original_to_mini_index_mapping |= set(ca.info().lattice_evolution)
    original_to_mini_index_mapping = list(original_to_mini_index_mapping)
    original_to_mini_index_mapping.sort()


    before,after = [],[]
    for ca in cas:
        metadata = ca.info()
        before.append(metadata.lattice_evolution[:max_sequence_length])
        after_ = metadata.lattice_evolution[max_sequence_length:]
        after_encoded = [
            original_to_mini_index_mapping.index(index) for index in after_
        ]
        after.append(after_encoded)
    
    return array(before),array(after),original_to_mini_index_mapping



#==========SETUP==================

lattice_width = 50
max_seq_length = 50
batch_size = 3
n_epochs = 100
#binary_threshold = 0.5
source_data, target_data, new_index_mapping = generate_dataset(
    lattice_width=lattice_width,
    batch_size=batch_size,
    max_sequence_length=max_seq_length
) 
tgt_vocab_size = len(new_index_mapping)

model = Transformer(
    src_vocab_size=lattice_width, 
    tgt_vocab_size=tgt_vocab_size, 
    max_seq_length=max_seq_length, 
    src_encoder=eca_encoder,
    tgt_encoder=lambda index,array_size: eca_encoder(
        index=new_index_mapping[index],
        array_size=array_size
    )
)

#==========TRAINING==================

train_model_with_target_indices( 
    n_epochs=n_epochs,
    model=model,
    x_train=source_data,
    y_train=target_data,
)


#==========PREDICTIONS=============
seed_indexes = array([
    [new_index_mapping.index(i) for i in source_data[b]]
    for b in range(batch_size)
])[:,1:2]
_,predicted_data_encoded = predict_n(
    model=model, 
    source=source_data[:,:1],
    target=seed_indexes,
    max_sequence_length=max_seq_length, 
    batch_size=batch_size,
    lattice_width=lattice_width,
    forecast_horizon=max_seq_length,
    original_to_mini_index_mapping=new_index_mapping
)

#======DISPLAY PREDICTIONS================
target_data_encoded=[
    [
        eca_encoder(
            index=new_index_mapping[i],
            array_size=lattice_width
        ) for i in target_data[b]
    ]
    for b in range(batch_size)
]
plot_spacetime_diagrams(
    target=target_data_encoded,
    predicted=predicted_data_encoded,
    batch_size=batch_size
)


plot_trajectories(
    target=[
        [
            projector(
                embedding=embedding,
                lattice_width=lattice_width
            ) for embedding in target_data_encoded[b]
        ]
        for b in range(batch_size)
    ], 
    predicted=[
        [
            projector(
                embedding=embedding,
                lattice_width=lattice_width
            ) for embedding in predicted_data_encoded[b]
        ]
        for b in range(batch_size)
    ],
    batch_size=batch_size
)



#TODO:
# - try predicting by adding additional / emergent features
