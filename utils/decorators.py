import asyncio
import random


def handle_retries(max_retries=3):
    def decorator(func):
        async def wrapper(self):
            for _ in range(max_retries):
                delay=random.randint(15, 45)
                if not await func(self):
                    await asyncio.sleep(delay)
                    continue
                return
        return wrapper
    return decorator
              