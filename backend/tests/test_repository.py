import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain.task_info import TaskInfo
from backend.domain.ticket import Ticket, TicketStatus
from backend.persistence.sqlalchemy_base import SQLAlchemyBase
from backend.persistence.ticket_entity import TicketEntity
from backend.persistence.ticket_mapper import TicketMapper
from backend.repositories.sqlalquemy_ticket_repository import SQLAlchemyTicketRepository


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
    
    yield repository
    
    SQLAlchemyBase.metadata.drop_all(engine)
        
@pytest.fixture
def ticket():

    ticket = Ticket(
        id=1,
        info=TaskInfo(
            name="Name",
            appliance="Appliance",
            address="Address",
            failure="Failure",
            other_details="Other details",
        ),
        status=TicketStatus.ACTIVE
    )
    
    yield ticket
        
def test_create(repository, ticket):
    ticket.id = None
    repository.create(ticket)
    
    with repository.session_factory() as session:
        entity: TicketEntity = session.get(TicketEntity, 1)
        
    assert entity is not None    
    assert entity.id == 1
    assert entity.name == ticket.info.name
    assert entity.appliance == ticket.info.appliance
    assert entity.address == ticket.info.address
    assert entity.failure == ticket.info.failure
    assert entity.other_details == ticket.info.other_details
    assert entity.status == ticket.status.value

    
def test_get_existing(repository, ticket):
    
    ticket.id = 5
    
    with repository.session_factory() as session:
        session.add(TicketMapper.to_entity(ticket))
        session.commit();
        
    get_ticket: Ticket = repository.get(ticket.id)
    
    assert get_ticket is not None
    assert get_ticket.id == ticket.id
    assert get_ticket.info.name == ticket.info.name
    assert get_ticket.info.appliance == ticket.info.appliance
    assert get_ticket.info.address == ticket.info.address
    assert get_ticket.info.failure == ticket.info.failure
    assert get_ticket.info.other_details == ticket.info.other_details
    assert get_ticket.status == ticket.status
    
def test_get_missing(repository, ticket):
    
    ticket.id = 5
    
    with repository.session_factory() as session:
        session.add(TicketMapper.to_entity(ticket))
        session.commit();
        
    get_ticket = repository.get(999)
    
    assert get_ticket is None
        
def test_list(repository, ticket):
    ticket.id = 5
    
    with repository.session_factory() as session:
        ticket.id = 1
        session.add(TicketMapper.to_entity(ticket))
        ticket.id = 2
        session.add(TicketMapper.to_entity(ticket))
        ticket.id = 3
        session.add(TicketMapper.to_entity(ticket))
        session.commit();
        
    tickets_list = repository.list()
    assert len(tickets_list) == 3
    assert tickets_list[0].id == 1
    assert tickets_list[1].id == 2
    assert tickets_list[2].id == 3

    assert True

@pytest.mark.parametrize("status", list(TicketStatus))
def test_mapper_round_trip(ticket, status):
    ticket.status = status
    entity = TicketMapper.to_entity(ticket)
    assert entity.id == ticket.id
    assert entity.status == status.value
    assert TicketMapper.to_domain(entity) == ticket


def test_update(repository, ticket):
    with repository.session_factory() as session:
        session.add(TicketMapper.to_entity(ticket))
        session.commit()

    ticket.info.failure = "Updated failure"
    ticket.status = TicketStatus.COMPLETED
    updated = repository.update(ticket)

    assert updated == ticket
    with repository.session_factory() as session:
        entity = session.get(TicketEntity, ticket.id)
        assert entity.failure == "Updated failure"
        assert entity.status == "completed"


@pytest.mark.parametrize(
    "name,address,expected",
    [(None, None, False), (None, " address ", True), (" name ", None, True)],
)
def test_search_with_nullable_info(repository, ticket, name, address, expected):
    from backend.domain.ticket_action import TicketAction, TicketActionType

    with repository.session_factory() as session:
        session.add(TicketMapper.to_entity(ticket))
        session.commit()
    action = TicketAction(
        action_type=TicketActionType.UPDATE,
        info=TaskInfo(name=name, appliance=None, address=address, failure=None, other_details=None),
    )
    assert repository.searchTicket(action) == ([ticket] if expected else [])


def test_database_rejects_null_status(repository, ticket):
    from sqlalchemy.exc import IntegrityError

    entity = TicketMapper.to_entity(ticket)
    entity.status = None
    with repository.session_factory() as session:
        session.add(entity)
        with pytest.raises(IntegrityError):
            session.commit()



def test_create_from_action(repository, ticket):
    from backend.domain.ticket_action import TicketAction, TicketActionType

    action = TicketAction(info=ticket.info, action_type=TicketActionType.NEW)
    new_ticket = TicketMapper.to_new_ticket(action)

    assert new_ticket.id is None
    assert new_ticket.info == action.info
    assert new_ticket.status == TicketStatus.ACTIVE

    stored = repository.create(new_ticket)
    assert stored.id == 1
    assert stored.info == action.info
    assert stored.status == TicketStatus.ACTIVE
