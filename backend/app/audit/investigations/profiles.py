from typing import Dict, Any

class SavedInvestigationProfiles:
    """
    Pre-configured search filters for common investigation scenarios.
    Allows one-click loading of complex queries.
    """
    
    PROFILES = {
        "failed_logins": {
            "name": "Failed Login Investigation",
            "description": "Finds all failed authentication attempts across the organization.",
            "filters": {
                "action": ["LOGIN_FAILED", "MFA_FAILED"],
                "severity": ["WARNING", "ERROR", "CRITICAL"]
            }
        },
        "critical_incidents": {
            "name": "Critical Incident Activity",
            "description": "Tracks all updates, escalations, and AI resolutions for critical incidents.",
            "filters": {
                "event_type": "Incident",
                "severity": ["CRITICAL"]
            }
        },
        "ai_operations": {
            "name": "AI Operations (Last 24h)",
            "description": "Monitors all AI suggestions, root cause analyses, and automated actions.",
            "filters": {
                "source": "AI_ENGINE"
            }
        },
        "permission_changes": {
            "name": "Permission & Role Changes",
            "description": "Audits any changes made to RBAC roles or user memberships.",
            "filters": {
                "action": ["ROLE_CREATED", "ROLE_UPDATED", "ROLE_DELETED", "MEMBER_ADDED", "MEMBER_REMOVED", "PERMISSION_GRANTED"]
            }
        }
    }

    @classmethod
    def get_profile(cls, profile_id: str) -> Dict[str, Any]:
        return cls.PROFILES.get(profile_id)
        
    @classmethod
    def list_profiles(cls) -> Dict[str, Any]:
        return cls.PROFILES
