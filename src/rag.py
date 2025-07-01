import asyncio
import json
import time

from g4f.client import AsyncClient, Client


class RetrievalAugmentedGeneration:
    response_timeout_seconds: float = 30.0

    def __init__(self):
        self.client = AsyncClient()
        self.sync_client = Client()

    def generate_stream(self, query: str, model: str, context: str):
        start = time.time()

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": query, "additional_data": []},
        ]

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                verbose=False,
                silent=True,
                max_tokens=1000,
            )

            delay = 0.05
            max_iters = int(self.response_timeout_seconds // delay)
            try:
                for _ in range(max_iters):
                    chunk = loop.run_until_complete(
                        asyncio.wait_for(
                            response.__anext__(),  # type: ignore
                            timeout=self.response_timeout_seconds,
                        )
                    )

                    if chunk.choices[0].delta.content:
                        yield (
                            json.dumps(
                                {"type": "chunk", "data": chunk.choices[0].delta.content}
                            )
                            + "\n\n"
                        )
                    time.sleep(delay)
            except asyncio.TimeoutError as e:
                raise TimeoutError("Timed out waiting for the model response") from e
            except StopAsyncIteration:
                # Generator finished
                pass
            finally:
                loop.run_until_complete(response.aclose())  # type: ignore
                loop.close()

        except BaseException as e:
            yield json.dumps({"type": "error", "data": str(e)}) + "\n\n"

        yield (json.dumps({"type": "complete", "data": time.time() - start}) + "\n\n")

    async def get_answer_async(self, query: str, model: str, context: str) -> SyntaxError:
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": query, "additional_data": []},
        ]

        response = await self.client.chat.completions.create(
            model=model, messages=messages, web_search=False, stream=False
        )
        return response.choices[0].message.content
