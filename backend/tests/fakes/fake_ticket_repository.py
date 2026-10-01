from backend.repositories.ticket_repository import TicketRepository

class FakeTicketRepository(TicketRepository):
        

    def create(self, ticket: TicketAction) -> TicketAction:
        pass
            

    def get(self, ticket_id: int) -> TicketAction | None:
        pass
        
            
    def update(self, ticket: TicketAction) -> TicketAction:
        pass
            

    def list(self) -> list[TicketAction]:
        pass
        
    def searchTicket(self) -> list(TicketAction):
        pass
   
    def delete(self, ticket_id) -> Boolean:
        pass
        
    def clear(self):
        with self.session_factory() as session:
            session.execute(delete(TicketEntity))
            session.commit()