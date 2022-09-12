import logging
from functools import wraps

logger = logging.getLogger(__name__)

def workspace_tolerance(func):
	@wraps(func)
	async def wrapper(*args, **kwargs):
		try:
			return await func(*args, **kwargs)
		except Exception as e:
			logger.error(e, exc_info=True)

	return wrapper
