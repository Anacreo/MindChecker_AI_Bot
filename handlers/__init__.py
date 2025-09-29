import importlib
import pkgutil
import logging
from aiogram import Dispatcher

def register_all_handlers(dp: Dispatcher):
    package = __name__
    seen_routers = set()

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        full_module_name = f"{package}.{module_name}"
        module = importlib.import_module(full_module_name)

        if hasattr(module, "router"):
            router = getattr(module, "router")
            if id(router) not in seen_routers:
                dp.include_router(router)
                seen_routers.add(id(router))
                logging.info(f"✅ Registered router from {full_module_name}")
            else:
                logging.warning(f"⚠️ Skipped duplicate router from {full_module_name}")
