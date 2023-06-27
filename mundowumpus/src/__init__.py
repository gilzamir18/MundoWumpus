from gym.envs.registration import register
from mundowumpus.wumpus import MeuAmbiente

register (
    id='Wumpus-v0',
    entry_point='mundowumpus.wumpus:MeuAmbiente',
)
