from random import randint
from numpy.linalg import norm
from numpy import arccos, ones, ndarray
from matplotlib.pyplot import ylim, xlim, plot, show, annotate, title

from elementary_cellular_automata import ElementaryCellularAutomata


def cosine_similarity(a:ndarray, b:ndarray) -> float:
    result = a @ b.T
    result /= (norm(a)*norm(b))+1e-9
    return result

def angle(x:ndarray, origin:ndarray) -> float:
    cos_theta = cosine_similarity(a=origin,b=x)
    return arccos(cos_theta)



#2d plot below
width = 8

ref_point_a = ones(shape=(width))
ref_point_a[::2] -= 1
ref_point_b = ones(shape=(width))

#DIsplay the configurations on the map
from numpy import array
seen = set()
for ic in range(2**width):
    config = ElementaryCellularAutomata.create_binary_lattice_from_number(
        state_number=ic,
        lattice_width=width
    )
    x = angle(x=array(config),origin=ref_point_a)
    y = angle(x=array(config),origin=ref_point_b)
    if (x,y) in seen:
        x += 10
        y += 10
    else:
        seen.add((x,y))
    annotate(
        ElementaryCellularAutomata.stringify_configuration(
            configuration=config
        ), 
        xy=(x,y),
        fontsize=5
    )


#Display all trajectories
rule = 3
T = 2
for ic in range(2**width):
    ca =  ElementaryCellularAutomata(
        lattice_width=width,
        initial_state= ic,
        time_steps=T,
        transition_rule_number=rule
    )
    xs = list(map(lambda x:angle(x=x,origin=ref_point_a),ca))
    ys = list(map(lambda x:angle(x=x,origin=ref_point_b),ca))
    plot(xs,ys,'-->',color='pink')

#Display a trajectory
T = 100
ic = randint(0,2**width)
ca =  ElementaryCellularAutomata(
    lattice_width=width,
    initial_state= ic,
    time_steps=T,
    transition_rule_number=rule
)
xs = list(map(lambda x:angle(x=x,origin=ref_point_a),ca))
ys = list(map(lambda x:angle(x=x,origin=ref_point_b),ca))
plot(xs,ys,'-->',color='red')


title(rule)
xlim(-0.2,2)
ylim(-0.2,2)
show()


#["m","tab:brown","c","g","b"]
#cmap = LinearSegmentedColormap.from_list("", ["y","tab:orange","r","tab:pink","tab:purple","tab:blue","tab:gray"])
#even_indexes = range(0,width,2)
#odd_indexes = range(1,width,2)
#initial_configuration = [0 for _ in range(width)]

#Go through states evenly
# ca =  ElementaryCellularAutomata(
#     lattice_width=width,
#     initial_state= 0,
#     time_steps=T,
#     transition_rule_number=rule
# )
# for i in even_indexes:
#     initial_configuration[i] = 1
#     initial_configuration_ = deepcopy(initial_configuration)
#     for j in odd_indexes:
#         initial_configuration_[j] = 1
#         xs = list(map(angle,ca))
#         #us = [y-x for x,y in zip(xs[:-1],xs[1:])]
#         #arrow_colours = [cmap(index/len(us)) for index in range(len(us))]

#         #quiver(xs[:-2],xs[1:-1],us[:-1],us[1:],color=arrow_colours)
#         plot(xs[:-1],xs[1:],'-->')
#         ca =  ElementaryCellularAutomata(
#             lattice_width=width,
#             initial_state= int(''.join(map(str,initial_configuration_)),2),
#             time_steps=T,
#             transition_rule_number=rule
#         )
# show()

#get a new trajectory

# initial_configuration = [0 for _ in range(width)]
# initial_configuration_ = deepcopy(initial_configuration)
# max_even = choice(even_indexes)
# max_odd = choice(odd_indexes)
# for i in range(0,max_even,2):
#     initial_configuration[i] = 1
#     initial_configuration_ = deepcopy(initial_configuration)
#     for j in range(0,max_odd,2):
#         initial_configuration_[j] = 1
# ca =  ElementaryCellularAutomata(
#     lattice_width=width,
#     initial_state= int(''.join(map(str,initial_configuration_)),2),
#     time_steps=T,
#     transition_rule_number=rule
# )
# xs = list(map(angle,ca))

# plot(xs[:-1],xs[1:],'-->',color='red')
# xlabel("theta(t)")
# ylabel("theta(t+1)")
# show()