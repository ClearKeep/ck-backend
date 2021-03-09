import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://localhost:6379/0', encoding='utf8')

  last_id = '0-0'
  while True:
    events = await redis.xread(['bigfoot:sightings:stream'], timeout=0, count=5, latest_ids=[last_id])
    for key, id, fields in events:
      pp(fields)
      last_id = id

asyncio.run(main())