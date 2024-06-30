"""docker build -t emergence_metrics . && docker run -p 8080:8080 -it emergence_metrics"""

from matplotlib.pyplot import imshow
from nicegui import ui

from eca import OneDimensionalElementaryCellularAutomata
from transfer_entropy import pointwise_transfer_entropy
from integrated_information import IntegratedInformation
from jpype import startJVM, getDefaultJVMPath

startJVM(getDefaultJVMPath(), f"-Djava.class.path=/app/infodynamics.jar")

def display_ca(width:int, time_steps:int, rule:int, emergence_filter:callable) -> None:    
    ca =  OneDimensionalElementaryCellularAutomata(
        lattice_width=width,
    )
    for _ in range(time_steps):
        ca.transition(rule_number=rule)

    filtered_spacetime = emergence_filter(
        evolution=ca.evolution(), 
    )
    emergence_window.clear()
    with emergence_window as splitter:
        with splitter.before:
            with ui.pyplot(figsize=(5, 10)):
                imshow(ca.evolution(), cmap='gray')
        with splitter.after:
            with ui.pyplot(figsize=(5, 10)):
                imshow(filtered_spacetime)
            

ui.label('width')
width = ui.slider(
    min=3, 
    max=300, 
    value=50, 
    step=1, 
).props('label-always')
time_steps = ui.number(label='Time Steps', value=500, min=1, max=1000, step=1)
rule = ui.number(label='Rule', value=110, min=0, max=256, step=1)
ui.chip('Run', icon='ads_click', on_click=lambda: display_ca(
    width=width.value,
    time_steps=int(time_steps.value),
    rule=int(rule.value),
    emergence_filter=lambda evolution: IntegratedInformation(phi_k=4)( #rule 54: k=4, rule 110: k=5
        train_evolution=evolution,
        test_evolution=evolution
    ) #pointwise_transfer_entropy
))
emergence_window = ui.splitter()

ui.run()