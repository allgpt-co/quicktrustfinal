"""Seed default training courses and provide auto-assignment logic."""
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.training import TrainingCourse, TrainingAssignment
from app.models.user import User


DEFAULT_COURSES = [
    {
        "title": "Security Awareness Fundamentals",
        "description": "Learn the basics of information security including password hygiene, social engineering, physical security, and safe browsing. Required for all employees annually.",
        "course_type": "document",
        "required_roles": ["employee", "control_owner", "compliance_manager", "super_admin"],
        "duration_minutes": 30,
        "is_required": True,
        "content_url": "/training/security-awareness",
    },
    {
        "title": "Phishing Recognition & Prevention",
        "description": "How to identify phishing emails, spear phishing, vishing, and smishing. Includes real-world examples and interactive simulations.",
        "course_type": "quiz",
        "required_roles": ["employee", "control_owner", "compliance_manager", "super_admin"],
        "duration_minutes": 20,
        "is_required": True,
        "content_url": "/training/phishing-recognition",
    },
    {
        "title": "Data Handling & Classification",
        "description": "How to properly classify, store, transmit, and dispose of company data. Covers PII, PHI, financial data, and intellectual property.",
        "course_type": "document",
        "required_roles": ["employee", "control_owner", "compliance_manager"],
        "duration_minutes": 25,
        "is_required": True,
        "content_url": "/training/data-handling",
    },
    {
        "title": "Incident Reporting Procedures",
        "description": "What constitutes a security incident, how to report it, escalation procedures, and your responsibilities. Every minute counts in incident response.",
        "course_type": "document",
        "required_roles": ["employee", "control_owner", "compliance_manager", "super_admin"],
        "duration_minutes": 15,
        "is_required": True,
        "content_url": "/training/incident-reporting",
    },
    {
        "title": "Password Security & MFA Best Practices",
        "description": "Creating strong passwords, using password managers, enabling multi-factor authentication, and recognizing credential theft attempts.",
        "course_type": "quiz",
        "required_roles": ["employee", "control_owner", "compliance_manager", "super_admin"],
        "duration_minutes": 15,
        "is_required": True,
        "content_url": "/training/password-security",
    },
]


async def seed_default_courses(db: AsyncSession, org_id: UUID) -> int:
    """Seed default training courses for an organization. Returns count created."""
    existing = await db.execute(
        select(func.count()).select_from(TrainingCourse).where(
            TrainingCourse.org_id == org_id,
            TrainingCourse.title.in_([c["title"] for c in DEFAULT_COURSES]),
        )
    )
    if (existing.scalar() or 0) >= len(DEFAULT_COURSES):
        return 0

    count = 0
    for course_data in DEFAULT_COURSES:
        # Check if this specific course exists
        exists = await db.execute(
            select(TrainingCourse).where(
                TrainingCourse.org_id == org_id,
                TrainingCourse.title == course_data["title"],
            )
        )
        if exists.scalar_one_or_none():
            continue

        course = TrainingCourse(
            org_id=org_id,
            title=course_data["title"],
            description=course_data["description"],
            course_type=course_data["course_type"],
            required_roles=course_data["required_roles"],
            duration_minutes=course_data["duration_minutes"],
            is_required=course_data["is_required"],
            content_url=course_data["content_url"],
            is_active=True,
        )
        db.add(course)
        count += 1

    if count:
        await db.commit()
    return count


async def auto_assign_courses(
    db: AsyncSession, org_id: UUID, user_id: UUID, user_roles: list[str],
) -> int:
    """Auto-assign required courses to a user based on their roles. Returns count assigned."""
    # Get all required active courses
    result = await db.execute(
        select(TrainingCourse).where(
            TrainingCourse.org_id == org_id,
            TrainingCourse.is_active.is_(True),
            TrainingCourse.is_required.is_(True),
        )
    )
    courses = list(result.scalars().all())

    count = 0
    for course in courses:
        required_roles = course.required_roles or []
        # Check if any of user's roles match
        if not any(r in required_roles for r in user_roles):
            continue

        # Check if already assigned
        existing = await db.execute(
            select(TrainingAssignment).where(
                TrainingAssignment.org_id == org_id,
                TrainingAssignment.course_id == course.id,
                TrainingAssignment.user_id == user_id,
            )
        )
        if existing.scalar_one_or_none():
            continue

        from datetime import datetime, timezone, timedelta
        assignment = TrainingAssignment(
            org_id=org_id,
            course_id=course.id,
            user_id=user_id,
            status="assigned",
            due_date=datetime.now(timezone.utc) + timedelta(days=30),
        )
        db.add(assignment)
        count += 1

    if count:
        await db.commit()
    return count
