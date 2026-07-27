import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.environment import Environment
from app.db.models.service import Service
from app.db.models.incident import Incident
from app.db.models.incident_timeline import IncidentTimeline
from app.db.models.enums import ServiceType, RuntimeType, ServiceTier, ServiceStatus
from app.db.models.enums import IncidentStatus, IncidentSeverity, IncidentPriority, IncidentSource, TimelineEvent

async def seed_incident_domain(session: AsyncSession) -> None:
    # Get first project and environment
    org_result = await session.execute(select(Organization).limit(1))
    org = org_result.scalars().first()
    
    project_result = await session.execute(select(Project).limit(1))
    project = project_result.scalars().first()
    
    env_result = await session.execute(select(Environment).limit(1))
    env = env_result.scalars().first()
    
    if not org or not project or not env:
        print("Cannot seed incident domain without Organization, Project, and Environment")
        return
        
    print(f"Seeding Incident Domain for Project '{project.name}' in '{env.name}'...")
    
    # Create Services
    payment_api = Service(
        organization_id=org.id,
        project_id=project.id,
        environment_id=env.id,
        name="Payment API",
        slug="payment-api",
        description="Core payment processing service",
        service_type=ServiceType.API,
        runtime=RuntimeType.PYTHON,
        tier=ServiceTier.TIER_1,
        status=ServiceStatus.DEGRADED,
        owner_team="billing-team"
    )
    
    auth_service = Service(
        organization_id=org.id,
        project_id=project.id,
        environment_id=env.id,
        name="Authentication Service",
        slug="auth-service",
        description="User authentication and OAuth",
        service_type=ServiceType.API,
        runtime=RuntimeType.GO,
        tier=ServiceTier.TIER_1,
        status=ServiceStatus.HEALTHY,
        owner_team="security-team"
    )
    
    session.add_all([payment_api, auth_service])
    await session.commit()
    await session.refresh(payment_api)
    
    # Create Incident
    incident = Incident(
        organization_id=org.id,
        project_id=project.id,
        service_id=payment_api.id,
        number="INC-000001",
        title="High Latency in Payment Processing",
        description="Stripe webhook endpoint is experiencing high latency.",
        status=IncidentStatus.INVESTIGATING,
        severity=IncidentSeverity.SEV_2,
        priority=IncidentPriority.P2,
        source=IncidentSource.ALERT
    )
    
    session.add(incident)
    await session.commit()
    await session.refresh(incident)
    
    # Create Timeline
    timeline_1 = IncidentTimeline(
        incident_id=incident.id,
        event_type=TimelineEvent.STATUS_CHANGED,
        message="Incident detected by Datadog High Latency Alert."
    )
    timeline_2 = IncidentTimeline(
        incident_id=incident.id,
        event_type=TimelineEvent.STATUS_CHANGED,
        message="Status updated to INVESTIGATING by On-Call Engineer."
    )
    
    session.add_all([timeline_1, timeline_2])
    await session.commit()
    
    from app.db.seeds.alert_seeds import seed_alerts
    await seed_alerts(session, payment_api.id)
    
    print(f"Incident Domain seeded successfully. Created incident {incident.number} for service {payment_api.name}.")
