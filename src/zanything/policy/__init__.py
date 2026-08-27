"""Policy & Confirmation Engine: Action classification and policy-as-code."""

from enum import StrEnum
from typing import ClassVar

from pydantic import BaseModel

from zanything.auth import Principal, Role
from zanything.logging import get_logger

logger = get_logger("zanything.policy")


class ActionClass(StrEnum):
    """Action risk classification."""

    READ_ONLY = "read_only"  # Autonomous execution allowed
    REVERSIBLE_WRITE = "reversible_write"  # Standard logging & validation
    HIGH_IMPACT = "high_impact"  # Requires explicit confirmation/dual control


class ApprovalStatus(StrEnum):
    """Approval lifecycle states."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    BYPASSED = "bypassed"


class PolicyDecision(BaseModel):
    """Result of policy evaluation for an action."""

    allowed: bool
    action_class: ActionClass
    requires_approval: bool
    reason: str
    approvers_required: int = 1


class PolicyEngine:
    """Evaluates security policies and approval requirements for actions."""

    HIGH_IMPACT_KEYWORDS: ClassVar[set[str]] = {
        "deploy",
        "delete",
        "drop",
        "purge",
        "terminate",
        "production",
        "release",
    }
    WRITE_KEYWORDS: ClassVar[set[str]] = {
        "create",
        "update",
        "write",
        "post",
        "edit",
        "modify",
        "send",
    }

    def classify_action(self, action_name: str) -> ActionClass:
        """Classify action risk based on name and keywords."""
        lower = action_name.lower()
        if any(kw in lower for kw in self.HIGH_IMPACT_KEYWORDS):
            return ActionClass.HIGH_IMPACT
        if any(kw in lower for kw in self.WRITE_KEYWORDS):
            return ActionClass.REVERSIBLE_WRITE
        return ActionClass.READ_ONLY

    def evaluate(self, principal: Principal, action_name: str) -> PolicyDecision:
        """Evaluate policy for principal and action."""
        action_class = self.classify_action(action_name)

        if action_class == ActionClass.HIGH_IMPACT:
            # High impact actions require explicit human operator confirmation
            return PolicyDecision(
                allowed=principal.has_role(Role.OPERATOR),
                action_class=action_class,
                requires_approval=True,
                reason="High-impact actions require explicit operator confirmation.",
                approvers_required=2 if principal.has_role(Role.ADMIN) is False else 1,
            )

        if action_class == ActionClass.REVERSIBLE_WRITE:
            allowed = principal.has_role(Role.OPERATOR)
            return PolicyDecision(
                allowed=allowed,
                action_class=action_class,
                requires_approval=False,
                reason="Standard write permitted for operators.",
            )

        return PolicyDecision(
            allowed=True,
            action_class=ActionClass.READ_ONLY,
            requires_approval=False,
            reason="Read-only operations permitted.",
        )
