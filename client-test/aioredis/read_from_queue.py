import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://localhost:6379/0', encoding='utf-8')

  while True:
    sighting = await redis.blpop('bigfoot:sightings:received')
    pp(sighting)

asyncio.run(main())