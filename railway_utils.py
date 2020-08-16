import pickle

from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.schedule_generators import sparse_schedule_generator


# Helper function to load in precomputed railway networks
def load_precomputed_railways(project_root, flags):
    with open(project_root / f'railroads/rail_networks_{flags.num_agents}x{flags.grid_width}x{flags.grid_height}.pkl', 'rb') as file:
        data = pickle.load(file)
        rail_networks = iter(data)
        print(f"Loading {len(data)} railways...")
    with open(project_root / f'railroads/schedules_{flags.num_agents}x{flags.grid_width}x{flags.grid_height}.pkl', 'rb') as file:
        schedules = iter(pickle.load(file))

    rail_generator = lambda *args: next(rail_networks)
    schedule_generator = lambda *args: next(schedules)
    return rail_generator, schedule_generator


env_params = {
    # small_v0 config
    "n_agents": 5,
    "x_dim": 35,
    "y_dim": 35,
    "n_cities": 4,
    "max_rails_between_cities": 2,
    "max_rails_in_city": 3,

    "seed": 42,
    "observation_tree_depth": 2,
    "observation_radius": 10,
    "observation_max_path_depth": 30
}

# Helper function to generate railways on the fly
def create_random_railways(project_root):
    speed_ration_map = {
        1 / 1:  1.0,   # Fast passenger train
        1 / 2.: 0.0,   # Fast freight train
        1 / 3.: 0.0,   # Slow commuter train
        1 / 4.: 0.0 }  # Slow freight train

    rail_generator = sparse_rail_generator(grid_mode=False, 
                                        max_num_cities=env_params["n_cities"], 
                                        max_rails_between_cities=env_params["max_rails_between_cities"], 
                                        max_rails_in_city=env_params["max_rails_in_city"])
    schedule_generator = sparse_schedule_generator(speed_ration_map)
    return rail_generator, schedule_generator