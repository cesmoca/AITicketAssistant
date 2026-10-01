import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.repositories.sqlalquemy_ticket_repository import SQLAlchemyTicketRepository
from backend.domain.ticket_action import TicketAction, TicketActionType
from backend.persistence.ticket_entity import TicketEntity
from backend.persistence.ticket_mapper import TicketMapper
from backend.tests.fakes.fake_database import FakeDatabase
from backend.persistence.sqlalchemy_base import SQLAlchemyBase


@pytest.fixture
def repository():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    
    SQLAlchemyBase.metadata.create_all(engine)
    
    TestSessionLocal = sessionmaker(bind=engine)

    repository = SQLAlchemyTicketRepository(
        session_factory=TestSessionLocal
    )
    
    ticket = TicketAction(
        ticket_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        other_details="Other details",
        ticket_type = TicketActionType.NEW
    )
    
    yield repository
    
    SQLAlchemyBase.metadata.drop_all(engine)
        
@pytest.fixture
def ticket():

    ticket = TicketAction(
        ticket_id=None,
        name="Name",
        appliance="Appliance",
        address="Address",
        failure="Failure",
        other_details="Other details",
        ticket_type = TicketActionType.NEW
    )
    
    yield ticket
        
def test_create(repository, ticket):
    
    repository.create(ticket)
    
    with repository.session_factory() as session:
        entity: TicketEntity = session.get(TicketEntity, 1)
        
    assert entity is not None    
    assert entity.ticket_id == 1
    assert entity.name == ticket.name
    assert entity.appliance == ticket.appliance
    assert entity.address == ticket.address
    assert entity.failure == ticket.failure
    assert entity.other_details == ticket.other_details
    assert entity.ticket_type == ticket.ticket_type

    
def test_get_existing(repository, ticket):
    
    ticket.ticket_id = 5
    
    with repository.session_factory() as session:
        session.add(TicketMapper.to_entity(ticket))
        session.commit();
        
    get_ticket: TicketAction = repository.get(ticket.ticket_id)
    
    assert get_ticket is not None
    assert get_ticket.ticket_id == ticket.ticket_id
    assert get_ticket.name == ticket.name
    assert get_ticket.appliance == ticket.appliance
    assert get_ticket.address == ticket.address
    assert get_ticket.failure == ticket.failure
    assert get_ticket.other_details == ticket.other_details
    assert get_ticket.ticket_type == ticket.ticket_type
    
def test_get_missing(repository, ticket):
    
    ticket.ticket_id = 5
    
    with repository.session_factory() as session:
        session.add(TicketMapper.to_entity(ticket))
        session.commit();
        
    get_ticket = repository.get(999)
    
    assert get_ticket is None
        
def test_list(repository, ticket):
    ticket.ticket_id = 5
    
    with repository.session_factory() as session:
        ticket.ticket_id = 1
        session.add(TicketMapper.to_entity(ticket))
        ticket.ticket_id = 2
        session.add(TicketMapper.to_entity(ticket))
        ticket.ticket_id = 3
        session.add(TicketMapper.to_entity(ticket))
        session.commit();
        
    tickets_list = repository.list()
    assert len(tickets_list) == 3
    assert tickets_list[0].ticket_id == 1
    assert tickets_list[1].ticket_id == 2
    assert tickets_list[2].ticket_id == 3

    assert True