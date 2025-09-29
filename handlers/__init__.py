import importlib
import pkgutil
from aiogram import Dispatcher

def register_all_handlers(dp: Dispatcher):
    package = __name__
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        if hasattr(module, "router"):
            dp.include_router(module.router)
