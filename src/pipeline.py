import typing

from src.rag import RetrievalAugmentedGeneration
from src.types import Context

# from src.rag_local import RetrievalAugmentedGenerationLocal

PipelineOutput = tuple[
    str, list[tuple[str, float]]
]  # (spell correction, [(doc path, score)])

ApiModel = typing.Literal[
    "command-r",
    "evil",
    "gpt-4o",
    "qwen-3-8b",
    "wizardlm-2-7b",
    "wizardlm-2-8x22b",
    "dolphin-2.6",
    "dolphin-2.9",
    "glm-4",
]

LocalModel = typing.Literal["arnir0/Tiny-LLM", "sshleifer/tiny-gpt2"]


class RAGPipeline:
    _available_api_models: list[ApiModel] = list(typing.get_args(ApiModel))
    # _available_local_models: list[LocalModel] = list(typing.get_args(LocalModel))
    _available_local_models: list[LocalModel] = []

    def __init__(self, context: Context) -> None:
        self.rag = RetrievalAugmentedGeneration()
        self.context = context
        self._available_specialists: list[str] = list(self.context.keys())

    def request(
        self,
        query: str,
        model: ApiModel | LocalModel,
        specialist: str,
    ):
        if specialist not in self._available_specialists:
            raise RuntimeError(f"Unknown specialist '{specialist}'")

        try:
            specialist_context = self.context[specialist]
        except KeyError:
            raise RuntimeError(f"No context found for specialist '{specialist}'")

        if model in self._available_api_models:
            return self.rag.generate_stream(query, model, specialist_context["prompt"])
        elif model in self._available_local_models:
            # return self.rag_local.generate_stream(query, model, context)
            raise NotImplementedError("RAG local not implemented yet")

        else:
            raise RuntimeError(f"Unknown model '{model}'")

    async def request_async(
        self,
        query: str,
        model: ApiModel | LocalModel,
        specialist: str,
    ) -> str:
        if specialist not in self._available_specialists:
            raise RuntimeError(f"Unknown specialist '{specialist}'")

        try:
            specialist_context = self.context[specialist]
        except KeyError:
            raise RuntimeError(f"No context found for specialist '{specialist}'")

        if model in self._available_api_models:
            return await self.rag.get_answer_async(
                query, model, specialist_context["prompt"]
            )  # type: ignore
        elif model in self._available_local_models:
            # return self.rag_local.get_answer_async(query, model, context)
            raise NotImplementedError("RAG local not implemented yet")

        else:
            raise RuntimeError(f"Unknown model '{model}'")

    @property
    def available_models(self) -> list[ApiModel | LocalModel]:
        return self._available_api_models + self._available_local_models

    @property
    def available_specialists(self) -> list[dict]:
        return [
            {"id": k, "opened": v["opened"], "label": v["label"]}
            for k, v in self.context.items()
        ]
