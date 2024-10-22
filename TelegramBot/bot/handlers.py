from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pydantic import BaseModel, ValidationError
from bot.config import dp
from db.services import take_item_from_db

items = ["Cap", "T-shirt", "Hoodie", "Pants", "Shoes", "Socks"]

colors = ["Black", "White"]
sizes = ["Small", "Medium", "Large", "X-Large"]

class ItemSchema(BaseModel):
    name: str
    quantity: int
    color: str
    size: str


@dp.message_handler(commands="start")
async def start_command(message: types.Message, state: FSMContext):  
    print("Start command received!")

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.add(*items)
    await message.answer("Select the item that was taken:", reply_markup=keyboard)
    await state.set_state("awaiting_item_selection")


@dp.message_handler(lambda message: message.text in items, state="awaiting_item_selection")
async def process_item_selection(message: types.Message, state: FSMContext):
    selected_item = message.text
    await state.update_data(selected_item=selected_item)

    await message.answer("Select the color of the item:", reply_markup=ReplyKeyboardRemove())
    color_keyboard = InlineKeyboardMarkup(row_width=2)
    for color in colors:
        color_keyboard.add(InlineKeyboardButton(text=color, callback_data=f"color_{color}"))

    await message.answer("Please choose a color:", reply_markup=color_keyboard)
    await state.set_state("awaiting_item_color")


@dp.callback_query_handler(lambda c: c.data.startswith("color_"), state="awaiting_item_color")
async def process_item_color(callback_query: types.CallbackQuery, state: FSMContext):
    selected_color = callback_query.data.split("_")[1]
    await state.update_data(selected_color=selected_color)

    size_keyboard = InlineKeyboardMarkup(row_width=2)
    for size in sizes:
        size_keyboard.add(InlineKeyboardButton(text=size, callback_data=f"size_{size}"))

    await callback_query.message.answer("Select the size of the item:", reply_markup=size_keyboard)
    await state.set_state("awaiting_item_size")


@dp.callback_query_handler(lambda c: c.data.startswith("size_"), state="awaiting_item_size")
async def process_item_size(callback_query: types.CallbackQuery, state: FSMContext):
    selected_size = callback_query.data.split("_")[1]
    await state.update_data(selected_size=selected_size)

    await callback_query.message.answer("Enter the quantity of item:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("awaiting_item_quantity")


@dp.message_handler(state="awaiting_item_quantity")
async def process_item_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)

        await state.update_data(quantity=quantity)

        data = await state.get_data()
        selected_item = data.get("selected_item")
        selected_color = data.get("selected_color")
        selected_size = data.get("selected_size")
        item = ItemSchema(name=selected_item, quantity=quantity, color=selected_color, size=selected_size)
        await message.answer(f"You have selected {item.quantity} units of {item.name} "
                             f"(Color: {item.color}, Size: {item.size}).")

        confirmation_keyboard = InlineKeyboardMarkup(row_width=2)
        confirmation_keyboard.add(
            InlineKeyboardButton(text="Yes", callback_data="confirm_yes"),
            InlineKeyboardButton(text="No", callback_data="confirm_no")
        )
        
        await message.answer("Confirm quantity of item by Yes or No", reply_markup=confirmation_keyboard)
        await state.set_state("awaiting_quantity_confirmation")
    except ValueError:
        await message.answer("Please enter a valid number.")
    except ValidationError as e:
        await message.answer(f"Validation error: {e}")


@dp.callback_query_handler(lambda c: c.data in ["confirm_yes", "confirm_no"], state="awaiting_quantity_confirmation")
async def process_item_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_name = data.get("selected_item")
    quantity = data.get("quantity")
    color = data.get("selected_color")
    size = data.get("selected_size")

    print(f"Item name: {item_name}, Quantity: {quantity}, Color: {color}, Size: {size}")
    
    if callback_query.data == "confirm_yes":
        take_item_from_db(item_name, quantity, size, color)
        await callback_query.message.answer("Item was successfully taken. Thank you!\n"
                                             "Please press /start to take a new item", reply_markup=ReplyKeyboardRemove())
        
        await state.finish()
    else:
        await callback_query.message.answer("Please enter the quantity again:")
        await state.set_state("awaiting_item_quantity")

