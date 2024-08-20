import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from database.base import Base
from core.config import settings

# Bu Alembic Config obyekti bo'lib, u
# foydalanilayotgan .ini faylidagi qiymatlarga
# kirish imkonini beradi.
config = context.config

config.set_main_option("sqlalchemy.url", settings.db.db_url)

# Konfiguratsiya faylini Python logging uchun talqin etish.
# Ushbu qator logglarni asosiy ravishda sozlaydi.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sizning modelingizning MetaData obyekti shu yerga qo'shilishi kerak
# 'avto-generatsiya' qo'llab-quvvatlash uchun
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# env.py ehtiyojlariga qarab, konfiguratsiyadan boshqa
# qiymatlarni olish mumkin:
# my_important_option = config.get_main_option("my_important_option")
# ... va boshqalar.


def run_migrations_offline() -> None:
    """Migratsiyalarni 'offline' rejimida ishga tushiring.

    Bu kontekstni faqat URL bilan sozlaydi
    va Engine bilan emas, lekin bu yerda Engine ham qabul qilinadi.
    Engine yaratishni o'chirib tashlash orqali
    biz DBAPI bo'lishi ham shart emas.

    Bu yerda context.execute() chaqiruvi berilgan satrni
    skript chiqishiga chiqaradi.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    # Migratsiyalarni bajarish uchun konfiguratsiya
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Bu holatda biz Engine yaratishimiz va
    kontekst bilan bog'lashimiz kerak.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Migratsiyalarni 'onlayn' rejimida ishga tushiring."""

    asyncio.run(run_async_migrations())


# Agar kontekst 'offline' rejimida bo'lsa,
# migratsiyalarni offline rejimida bajaradi.
if context.is_offline_mode():
    run_migrations_offline()
# Aks holda, onlayn rejimda migratsiyalarni bajaradi.
else:
    run_migrations_online()
