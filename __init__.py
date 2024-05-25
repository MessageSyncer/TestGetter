from model import *
from util import *

from datetime import datetime


class _MockAPI():  # This class is used to mock an api. Can be safely moved.
    def __init__(self) -> None:
        self._data = {}

    def generate_blog(self, request_user_id):
        import random
        import string
        from datetime import datetime

        # Generate a 12-digit alphanumeric mixture
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        userid = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        # Get the current date and time
        now = datetime.now()
        # create content
        content = f"This is a blog with id {id}, generated at {now}, requested by user {request_user_id}"

        result = {
            "id": id,
            "content": content,
            'userid': userid,
            'ts': int(now.timestamp()),
            'url': f'https://mock.url/{id}',
            'picture': [
                'https://pure80spop.co.uk/wp-content/uploads/2020/04/Rick-Astley-1600x1069.jpg'
            ]
        }
        self._data[id] = result

        return result

    def list(self, request_user_id, token, mock_new_book_count=2):
        """return blog id list"""
        return [self.generate_blog(request_user_id)['id'] for i in range(mock_new_book_count)]

    def detail(self, request_user_id, token, id):
        """return blog detail by id"""
        return self._data[id]


_mockapi = _MockAPI()


@dataclass
class GetListOption:
    count: int = 2


@dataclass
class TestGetterConfig(GetterConfig):  # Config of the adapter
    trigger: list[str] = field(default_factory=lambda: ['* * * * * */10'])  # override this field to specify triggers
    get_list_option: GetListOption = field(default_factory=GetListOption)


@dataclass
class TestGetterInstanceConfig(GetterInstanceConfig):  # Config of an instance
    token: str = '230qr98hjfr'


class TestGetter(Getter[TestGetterConfig, TestGetterInstanceConfig]):
    async def list(self) -> list[str]:
        # Return list of message id.

        self.logger  # self.logger

        # self.id is the unique id for adapter to indentify an instance.
        # You can use self.instance_config, self.config to access configs.
        return _mockapi.list(self.id, self.instance_config.token, self.config.get_list_option.count)

    async def detail(self, id: str) -> GetResult:
        # Return detail of message.
        detail = _mockapi.detail(self.id, self.instance_config.token, id)

        content = Struct.template1(
            content=detail['content'],
            ts=detail['ts'],
            title='Test Title',
            url=detail['url'],
            username='Test User',
            images=detail['picture'],
            ip='',
            detail=''
        )  # Framework provides builtin templates.
        # content = Struct().text(detail['content']).image(detail['picture']) # You can also combine a struct manually.

        return GetResult(user_id=detail['userid'], ts=detail['ts'], content=content)

    async def details(self, ids: List[str]) -> GetResult:
        # Complate this method to support merge multiple blogs into one blog
        raise NotImplementedError()
