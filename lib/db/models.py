import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base
from models.user import User
from models.dealership import Dealership
from models.car import Car
from models.sale import Sale

# Import all models to ensure they're registered with Base