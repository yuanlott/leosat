from hypatia import simulator
from satgenpy import constellation
import json

def create_telesat_config():
    # Create a constellation similar to Telesat LEO
    conf = constellation.generate_telesat_like_constellation(
        num_planes=13,
        sats_per_plane=12,
        altitude_km=1000,
        inclination_deg=99.5
    )
    return conf

def run_simulation(duration=600, step=1):
    conf = create_telesat_config()
    sim = simulator.HypatiaSim(config=conf)

    # Add a fixed UT and a mobile UT
    sim.add_user_terminal("fixed_ut", coordinates=(45.4215, -75.6992))  # Ottawa
    sim.add_user_terminal("mobile_ut", trajectory=[
        (40.7128, -74.0060),  # Start near NYC
        (41.0, -73.0),        # Move northeast
        (42.0, -72.0)
    ])

    sim.run(duration=duration, step=step)

    data = []
    for t in range(0, duration, step):
        positions = sim.get_satellite_positions(timestamp=t)
        path = sim.get_routing_path("mobile_ut", "fixed_ut", timestamp=t)
        data.append({"timestamp": t, "positions": positions, "path": path})

    return data

def export_to_json(data, filename="sim_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f)
