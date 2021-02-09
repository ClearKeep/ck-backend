# import sqlalchemy as db
# from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from utils.config import get_system_config
from src.controllers import app

db = SQLAlchemy(app)