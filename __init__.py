from model import *
from util import *
import image

from datetime import datetime


class MockAPI():  # This class is used to mock an api. Can be safely moved.
    def __init__(self, userid, token) -> None:
        self._data = {}
        self.userid = userid
        self.token = token

    def generate_blog(self):
        import random
        import string
        from datetime import datetime

        # Generate a 12-digit alphanumeric mixture
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        userid = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        # Get the current date and time
        now = datetime.now()
        # create content
        content = f"This is a blog with id {id}, generated at {now}, requested by user {self.userid}"

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

    def list(self, mock_new_book_count=2):
        """return blog id list"""
        return [self.generate_blog()['id'] for i in range(mock_new_book_count)]

    def detail(self, id):
        """return blog detail by id"""
        return self._data[id]


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
    # This is your adapter.
    # You should not write any logic to handle errors to avoid a function failing to return.
    # Framework will do it.

    def __init__(self, id=None) -> None:
        super().__init__(id)  # you must call super().__init__ then you can add your code

        # self.id is the unique id for adapter to indentify an instance.
        # You can use self.instance_config, self.config to access configs.
        self.api = MockAPI(self.id, self.instance_config.token)
        self.logger.info(f'{self.id} inited')

    async def list(self) -> list[str]:
        # Return list of message id.
        return self.api.list(self.config.get_list_option.count)

    async def detail(self, id: str) -> GetResult:
        # Return detail of message.
        detail = self.api.detail(id)

        content = Struct.template1(
            content=detail['content'],
            ts=detail['ts'],
            title='Test Title',
            url=detail['url'],
            username='Test User',
            images=await image.download_list(detail['picture']),  # You can use this builtin method to download pic easily
            ip='',
            detail=''
        )  # Framework provides builtin templates.
        # content = Struct().text(detail['content']).image(detail['picture']) # You can also combine a struct manually.

        return GetResult(user_id=detail['userid'], ts=detail['ts'], content=content)

    async def details(self, ids: List[str]) -> GetResult:
        # Complete this method to support merge multiple blogs into one blog
        raise NotImplementedError()
