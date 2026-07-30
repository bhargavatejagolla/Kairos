import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.signal import Signal
from app.repositories.signal import SignalRepository
from app.schemas.signal import SignalIn

logger = logging.getLogger(__name__)

class SignalService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.signal_repo = SignalRepository(session)
        # Note: RuleEngine will be injected here during actual runtime orchestration
        
    async def ingest(self, service_id: UUID, signal_data: SignalIn) -> Signal:
        """
        Validates, normalizes, and stores a single signal.
        """
        signal_model = Signal(
            service_id=service_id,
            signal_type=signal_data.signal_type,
            source=signal_data.source,
            value=signal_data.value,
            unit=signal_data.unit,
            metadata_=signal_data.metadata_,
            received_at=signal_data.received_at
        )
        self.session.add(signal_model)
        await self.session.commit()
        await self.session.refresh(signal_model)
        
        # Next steps: Evaluate signal via RuleEngine
        return signal_model

    async def bulk_ingest(self, service_id: UUID, signals: list[SignalIn]) -> None:
        """
        Optimized append-only ingestion for multiple telemetry points.
        """
        signal_models = [
            Signal(
                service_id=service_id,
                signal_type=s.signal_type,
                source=s.source,
                value=s.value,
                unit=s.unit,
                metadata_=s.metadata_,
                received_at=s.received_at
            )
            for s in signals
        ]
        self.session.add_all(signal_models)
        await self.session.commit()
