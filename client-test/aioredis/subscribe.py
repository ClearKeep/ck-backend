import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://localhost:6379/0', encoding='utf-8')

  [channel] = await redis.psubscribe('bigfoot:broadcast:channel:*')

  while True:
    message = await channel.get()
    pp(message)

asyncio.run(main())