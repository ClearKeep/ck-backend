import asyncio
import aioredis

async def main():

  redis = await aioredis.create_redis('redis://:foobared@localhost:6379/0', encoding='utf-8')

  await asyncio.gather(
    publish(redis, 1, 'Possible vocalizations east of Makanda'),
    publish(redis, 2, 'Sighting near the Columbia River'),
    publish(redis, 2, 'Chased by a tall hairy creature')
  )

  redis.close()
  await redis.wait_closed()

def publish(redis, channel, message):
  return redis.publish(f'bigfoot:broadcast:channel:{channel}', message)

asyncio.run(main())