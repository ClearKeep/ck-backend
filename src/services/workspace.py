from src.services.base import BaseService
from src.models.workspace import Workspace

class WorkspaceService(BaseService):
    def __init__(self):
        super().__init__(Workspace())
