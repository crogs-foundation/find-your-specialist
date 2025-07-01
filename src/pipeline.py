import typing

from src.rag import RetrievalAugmentedGeneration

# from src.rag_local import RetrievalAugmentedGenerationLocal

PipelineOutput = tuple[
    str, list[tuple[str, float]]
]  # (spell correction, [(doc path, score)])

ApiModel = typing.Literal[
    "qwen-2-72b",
    "gpt-4o",
    "wizardlm-2-7b",
    "wizardlm-2-8x22b",
    "dolphin-2.6",
    "dolphin-2.9",
    "glm-4",
    "evil",
    "command-r",
]

LocalModel = typing.Literal["arnir0/Tiny-LLM", "sshleifer/tiny-gpt2"]

Specialist = typing.Literal["lawyer", "chef", "psychologist"]

SpecialistContext: dict[Specialist, str] = {
    "lawyer": "You are professional Russian lawyer. You purpose is to help user in law questions. \
        The user can ask you about any law related questions (in Russia), and you should answer \
        in Russian with as much references as possible. If the question is unrelated to law,\
        answer 'Sorry, the question is unrelated' ",
    "chef": "You are professional chef or cook. You purpose is to help user in cooking questions. \
        The user can ask you about any cooking related questions (in Russia), and you should answer \
        in Russian with as much references as possible. If the question is unrelated to cooking,\
        answer 'Sorry, the question is unrelated' ",
    "psychologist": "You are professional psychologist. You purpose is to help user in psychological questions. \
        The user can ask you about any psychology related questions (in Russia), and you should answer \
        in Russian with as much references as possible. If the question is unrelated to psychology,\
        answer 'Sorry, the question is unrelated' ",
}


class RAGPipeline:
    _available_api_models: list[ApiModel] = list(typing.get_args(ApiModel))
    # _available_local_models: list[LocalModel] = list(typing.get_args(LocalModel))
    _available_local_models: list[LocalModel] = []
    _available_specialists: list[Specialist] = list(typing.get_args(Specialist))

    def __init__(self) -> None:
        self.rag = RetrievalAugmentedGeneration()
        # self.rag_local = RetrievalAugmentedGenerationLocal()

    def request(
        self,
        query: str,
        model: ApiModel | LocalModel,
        specialist: Specialist,
    ):
        if specialist not in self._available_specialists:
            raise RuntimeError(f"Unknown specialist '{specialist}'")

        context = SpecialistContext.get(specialist, "")

        if model in self._available_api_models:
            return self.rag.generate_stream(query, model, context)
        elif model in self._available_local_models:
            # return self.rag_local.generate_stream(query, model, context)
            raise NotImplementedError("RAG local not implemented yet")

        else:
            raise RuntimeError(f"Unknown model '{model}'")

    async def request_async(
        self,
        query: str,
        model: ApiModel | LocalModel,
        specialist: Specialist,
    ) -> str:
        if specialist not in self._available_specialists:
            raise RuntimeError(f"Unknown specialist '{specialist}'")

        context = SpecialistContext.get(specialist, "")
        if model in self._available_api_models:
            return await self.rag.get_answer_async(query, model, context)  # type: ignore
        elif model in self._available_local_models:
            # return self.rag_local.get_answer_async(query, model, context)
            raise NotImplementedError("RAG local not implemented yet")

        else:
            raise RuntimeError(f"Unknown model '{model}'")

    @property
    def available_models(self) -> list[ApiModel | LocalModel]:
        return self._available_api_models + self._available_local_models

    @property
    def available_specialists(self) -> list[Specialist]:
        return self._available_specialists
