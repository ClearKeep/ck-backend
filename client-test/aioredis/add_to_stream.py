import asyncio
import aioredis

async def main():

  redis = await aioredis.create_redis('redis://localhost:6379/0', encoding='utf-8')

  await asyncio.gather(
    add_to_stream(redis, 1, 'Possible vocalizations east of Makanda', 'Class D'),
    add_to_stream(redis, 2, 'Sighting near the Columbia River', 'Class D'),
    add_to_stream(redis, 3, 'Chased by a tall hairy creature', 'Class D'))

  redis.close()
  await redis.wait_closed()

def add_to_stream(redis, id, title, classification):
  return redis.xadd('bigfoot:sightings:stream', {
    'id': id, 'title': title, 'classification': classification })

asyncio.run(main())