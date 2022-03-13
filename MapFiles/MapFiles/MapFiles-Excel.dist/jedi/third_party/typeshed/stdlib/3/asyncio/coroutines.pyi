from typing import Any, Callable, Generator, List, TypeVar

__all__: List[str]

_F = TypeVar('_F', bound=Callable[..., Any])

def coroutine(func: _F) -> _F: ...
def iscoroutinefunction(func: Callable[..., Any]) -> bool: ...
def iscoroutine(obj: Any) -> bool: ...