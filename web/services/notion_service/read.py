from typing import List

from notion.client import NotionClient
from notion.collection import CollectionRowBlock

from web.utils import clean_title
from web.utils import remove_newlines


def get_page_url(page_id: str, page_title: str) -> str:
    url = clean_title(page_title) + page_id.replace('-', '')
    return f"notion://www.notion.so/{url}"


def make_card_from_text_page(page_id, page_title) -> str:
    return f"{page_id};<a href='{get_page_url(page_id, page_title)}'>{page_title}</a>;"


def make_image_card_from_page(page_id, page_title, image_url, compression) -> str:
    return f"{page_id};<img src='{image_url}'>;<a href='{get_page_url(page_id, page_title)}'>{page_title}</a><br><p>{compression}</p>"


def make_card_from_person_page(row) -> str:
    full_name = row.first_name.split(' ')[0] + ' ' + row.last_name
    next_question = remove_newlines(row.next_question_to_ask_them)
    return f"{row.id};" \
        f"<a href='{get_page_url(row.id, row.title)}'>{full_name}</a>;" \
        f"<b>Compression:</b> {row.compression}<br>" \
        f"<b>Next Q:</b> {next_question}<br>" \
        f"<b>Groups:</b> {', '.join(row.groups)}<br>" \
        f"<b>Location:</b> {', '.join(row.location)}<br>" \
        f"<b>Edited:</b> {row.edited.strftime('%-m/%-d/%y')}<br>" \
        f"<b>Added:</b> {row.added.strftime('%-m/%-d/%y')}"


def get_client() -> NotionClient:
    token_v2 = open('token_v2').read().strip()
    return NotionClient(token_v2=token_v2, monitor=True)


def get_db_row_urls(block: CollectionRowBlock) -> List[str]:
    return block.views[0].get()['page_sort']
