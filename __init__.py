from model import *
from util import *

from datetime import datetime


@dataclass
class TestGetterConfig(GetterConfig):
    pass


@dataclass
class TestGetterInstanceConfig(GetterInstanceConfig):
    pass


class TestGetter(Getter[TestGetterConfig, TestGetterInstanceConfig]):
    async def list(self) -> list[str]:
        return [str(int(datetime.now().timestamp()))]

    async def detail(self, id: str) -> GetResult:
        content = Struct.template1(title=f'Test',
                                   content=f'content of {id}',
                                   ts=int(datetime.now().timestamp()))
        return GetResult('testusr001', int(datetime.now().timestamp()), content)

    async def details(self, ids: List[str]) -> GetResult:
        content = Struct.template1(title=f'Test',
                                   content=f'content of list: {", ".join(ids)}',
                                   ts=int(datetime.now().timestamp()))
        return GetResult('testusr001', int(datetime.now().timestamp()), content)
