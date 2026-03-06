from enum import StrEnum


class ControlStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    NOT_IMPLEMENTED = "not_implemented"
    NOT_APPLICABLE = "not_applicable"
    NEEDS_REVIEW = "needs_review"


class ControlEffectiveness(StrEnum):
    EFFECTIVE = "effective"
    PARTIALLY_EFFECTIVE = "partially_effective"
    NOT_EFFECTIVE = "not_effective"
    NOT_RATED = "not_rated"
    NOT_ASSESSED = "not_assessed"


class AutomationLevel(StrEnum):
    MANUAL = "manual"
    SEMI_AUTOMATED = "semi_automated"
    AUTOMATED = "automated"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(StrEnum):
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    FINANCIAL = "financial"


class RiskTreatment(StrEnum):
    MITIGATE = "mitigate"
    ACCEPT = "accept"
    TRANSFER = "transfer"
    AVOID = "avoid"


class EvidenceStatus(StrEnum):
    PENDING = "pending"
    COLLECTED = "collected"
    APPROVED = "approved"
    EXPIRED = "expired"
    REJECTED = "rejected"


class IncidentSeverity(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class VendorRiskTier(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PolicyStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class AuditType(StrEnum):
    EXTERNAL = "external"
    INTERNAL = "internal"


class ReportFormat(StrEnum):
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"


class UserRole(StrEnum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    COMPLIANCE_MANAGER = "compliance_manager"
    CONTROL_OWNER = "control_owner"
    EMPLOYEE = "employee"
    EXECUTIVE = "executive"
    AUDITOR_INTERNAL = "auditor_internal"
    AUDITOR_EXTERNAL = "auditor_external"


class MonitorSchedule(StrEnum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"


class FindingSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REMEDIATED = "remediated"
    ACCEPTED = "accepted"
    CLOSED = "closed"


class AuditStatus(StrEnum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MonitorCheckType(StrEnum):
    MANUAL = "manual"
    AUTOMATED = "automated"
    HYBRID = "hybrid"


class AlertSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
