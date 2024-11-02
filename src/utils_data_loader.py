from numpy import ndarray, array

from dynamical_system.eca.elementary_cellular_automata import ElementaryCellularAutomata

def generate_dataset(
    rule_number:int,
    lattice_width:int,
    batch_size:int,
    context_sequence_length:int,
    max_sequence_length:int
) -> tuple[ndarray, ndarray, list[int]]:
    
    cas = [
        ElementaryCellularAutomata(
            lattice_width=lattice_width,
            time_steps=context_sequence_length + max_sequence_length,
            transition_rule_number=rule_number
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
        before.append(metadata.lattice_evolution[:context_sequence_length])
        after_ = metadata.lattice_evolution[context_sequence_length:]
        after_encoded = [
            original_to_mini_index_mapping.index(index) for index in after_
        ]
        after.append(after_encoded)
    
    return array(before),array(after),original_to_mini_index_mapping
