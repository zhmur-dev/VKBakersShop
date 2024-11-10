from os import getenv

from dotenv.main import load_dotenv
from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import ui
from database import (
    BASE_DIR, get_categories, get_category_name,
    get_product_details, get_products
)

load_dotenv()


vk = VkApi(token=getenv('VK_TOKEN'))
group_id = getenv('VK_GROUP_ID')


def get_categories_menu():
    categories = get_categories()
    menu = VkKeyboard(inline=True)
    current_inline_buttons = 0
    for category in categories:
        if current_inline_buttons >= ui.MAX_INLINE_BUTTONS:
            menu.add_line()
            current_inline_buttons = 0
        menu.add_callback_button(
            label=category[1],
            color=VkKeyboardColor.PRIMARY,
            payload={
                'type': 'get_products',
                'category_id': category[0]
            }
        )
        current_inline_buttons += 1
    return menu


def get_products_menu(category_id):
    products = get_products(category_id)
    menu = VkKeyboard(inline=True)
    current_inline_buttons = 0
    for product in products:
        if current_inline_buttons >= ui.MAX_INLINE_BUTTONS:
            menu.add_line()
            current_inline_buttons = 0
        menu.add_callback_button(
            label=product[1],
            color=VkKeyboardColor.PRIMARY,
            payload={
                'type': 'get_product_details',
                'product_id': product[0]
            }
        )
        current_inline_buttons += 1
    menu.add_line()
    menu.add_callback_button(
        label=ui.BACK_TO_CATEGORIES,
        color=VkKeyboardColor.SECONDARY,
        payload={
            'type': 'get_categories',
        }
    )
    return menu


def get_back_to_products_menu(category_id):
    menu = VkKeyboard(inline=True)
    menu.add_callback_button(
        label=ui.BACK_TO_PRODUCTS.format(
            category_name=get_category_name(category_id=category_id)
        ),
        color=VkKeyboardColor.SECONDARY,
        payload={
            'type': 'get_products',
            'category_id': category_id
        }
    )
    return menu


def reply(user_id, message=None, keyboard=None, attachment=None):
    vk.method(
        'messages.send',
        {
            'user_id': user_id,
            'random_id': get_random_id(),
            'message': message,
            'keyboard': keyboard,
            'attachment': attachment,
        }
    )


def run_bot():
    for event in VkBotLongPoll(
        vk, group_id=group_id,
    ).listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            reply(
                user_id=event.message.from_id,
                message=(
                    ui.GREETINGS_MESSAGE + '\n\n' + ui.GET_CATEGORIES_MESSAGE
                ),
                keyboard=get_categories_menu().get_keyboard()
            )
        if event.type == VkBotEventType.MESSAGE_EVENT:
            next_message = ui.ERROR_MESSAGE
            next_menu = get_categories_menu()
            attachment = None
            if event.object.payload.get('type') == 'get_categories':
                next_message = ui.GET_CATEGORIES_MESSAGE
            elif event.object.payload.get('type') == 'get_products':
                category_id = event.object.payload.get('category_id')
                next_message = ui.GET_PRODUCTS_MESSAGE.format(
                    category_name=get_category_name(category_id=category_id)
                )
                next_menu = get_products_menu(
                    category_id=category_id
                )
            elif event.object.payload.get('type') == 'get_product_details':
                product = get_product_details(
                    product_id=event.object.payload.get('product_id')
                )
                next_message = product[3]
                photo = VkUpload(vk).photo_messages(
                    str(BASE_DIR / product[4])
                )
                attachment = f'photo{photo[0]['owner_id']}_{photo[0]['id']}'
                next_menu = get_back_to_products_menu(
                    category_id=product[2]
                )
            vk.method(
                'messages.sendMessageEventAnswer',
                {
                    'user_id': event.object.user_id,
                    'event_id': event.object.event_id,
                    'peer_id': event.object.peer_id,
                    'event_data': event.object.event_data
                }
            )
            reply(
                user_id=event.object.user_id,
                message=next_message,
                keyboard=next_menu.get_keyboard(),
                attachment=attachment
            )


if __name__ == '__main__':
    run_bot()
