import logging
from typing import List
from contextlib import contextmanager
from collections.abc import Generator

from kubernetes import client, config

logger = logging.getLogger()


class Context:
    ACTIVE = "(active_context)"

    def __init__(self, context: str) -> None:
        contexts, active_context = config.list_kube_config_contexts()
        if context == Context.ACTIVE:
            self._context = active_context
        else:
            try:
                self._context = next(ctx for ctx in contexts if ctx["name"] == context)
            except StopIteration:
                raise ValueError(f"Context '{context}' not found")

    def name(self) -> str:
        return self._context["name"]

    def api(self) -> client.CoreV1Api:
        return client.CoreV1Api(
            api_client=config.new_client_from_config(context=self.name())
        )


class Namespace:
    ALL: str = "(all_namespaces)"

    def __init__(self, name: str, client: "Client") -> None:
        if name == Namespace.ALL:
            self._all = True
            self._namespace = None
        else:
            self._all = False
            namespaces = client.namespaces()
            try:
                self._namespace = next(
                    ns for ns in namespaces.items if ns.metadata.name == name
                )
            except StopIteration:
                raise ValueError(
                    f"Namespace '{name}' not found in context '{self.context.name()}'"
                )

    def name(self) -> str:
        if self.all():
            raise RuntimeError("All Namespaces has no name")
        else:
            return self._namespace.metadata.name

    def all(self) -> bool:
        return self._all


class Client:
    def __init__(self, context: Context) -> None:
        self.context = context
        self._api = context.api()

    def pods(self, namespace: Namespace) -> List[str]:
        if namespace == Namespace.ALL:
            return self._api.list_pod_for_all_namespaces()
        else:
            return self._api.list_namespaced_pod(namespace.name())

    def namespaces(self) -> List[str]:
        return self._api.list_namespace()
