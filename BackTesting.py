import pandas as pd
import numpy as np
import logging

class BackTester:
    def __init__(self, strategy, historicalData):
        self.strategy = strategy, self.historicalData = historicalData

