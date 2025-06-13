from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio


class Base(DeclarativeBase):
    pass


class Term(Base):
    __tablename__ = "terms"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))

# TODO: Valute's stuff

async def get_engine(database_url: str):
    engine = create_async_engine(database_url)
    return engine


class DbHandler:
    def __init__(self, database_url: str):
        self._engine = None
        self._session = None
        self._database_url = database_url

    async def init(self):
        self.engine = await get_engine(self._database_url)
        self.session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def create_term(self, term: Term):
        async with self.session() as session:
            session.add(term)
            await session.commit()
    
    async def get_term(self, term_id: int):
        async with self.session() as session:
            term = await session.get(Term, term_id)
            return term
    
    async def update_term(self, term_id: int, new_description: str):
        async with self.session() as session:
            term = await session.get(Term, term_id)
            term.description = new_description
            await session.commit()
    
    async def delete_term(self, term_id: int):
        async with self.session() as session:
            term = await session.get(Term, term_id)
            session.delete(term)
            await session.commit()
    
    async def get_all_terms(self):
        async with self.session() as session:
            terms = await session.execute(select(Term))
            return terms.scalars().all()
