"""流程状态机"""
from enum import Enum
from typing import Dict, Callable, Optional, List
from dataclasses import dataclass
from agents.roles import WorkflowState, Agent, AgentRole


@dataclass
class WorkflowTransition:
    """工作流转移"""
    from_state: WorkflowState
    to_state: WorkflowState
    required_role: AgentRole
    action: Optional[Callable] = None


class Workflow:
    """工作流引擎"""

    # 定义工作流转移规则
    TRANSITIONS = [
        WorkflowTransition(WorkflowState.IDLE, WorkflowState.BLUEPRINT, AgentRole.PRODUCER),
        WorkflowTransition(WorkflowState.BLUEPRINT, WorkflowState.DESIGN, AgentRole.DESIGNER),
        WorkflowTransition(WorkflowState.DESIGN, WorkflowState.DESIGN_REVIEW, AgentRole.PRODUCER),
        WorkflowTransition(WorkflowState.DESIGN_REVIEW, WorkflowState.PRESENTATION, AgentRole.DESIGNER),
        WorkflowTransition(WorkflowState.PRESENTATION, WorkflowState.DESIGN_ADJUST, AgentRole.DESIGNER),
        WorkflowTransition(WorkflowState.DESIGN_ADJUST, WorkflowState.DESIGN_CONFIRM, AgentRole.PRODUCER),
        WorkflowTransition(WorkflowState.DESIGN_CONFIRM, WorkflowState.REQUIREMENT_ANALYSIS, AgentRole.PROGRAMMER),
        WorkflowTransition(WorkflowState.REQUIREMENT_ANALYSIS, WorkflowState.ENVIRONMENT_SETUP, AgentRole.PROGRAMMER),
        WorkflowTransition(WorkflowState.ENVIRONMENT_SETUP, WorkflowState.DEVELOPMENT, AgentRole.PROGRAMMER),
        WorkflowTransition(WorkflowState.DEVELOPMENT, WorkflowState.RESOURCE_CREATION, AgentRole.ARTIST),
        WorkflowTransition(WorkflowState.RESOURCE_CREATION, WorkflowState.DEPLOYMENT, AgentRole.DEVOPS),
        WorkflowTransition(WorkflowState.DEPLOYMENT, WorkflowState.COMPLETED, AgentRole.DEVOPS),
    ]

    def __init__(self):
        self.current_state = WorkflowState.IDLE
        self.transition_map: Dict[WorkflowState, List[WorkflowTransition]] = {}
        self._build_transition_map()

    def _build_transition_map(self):
        """构建转移映射"""
        for transition in self.TRANSITIONS:
            if transition.from_state not in self.transition_map:
                self.transition_map[transition.from_state] = []
            self.transition_map[transition.from_state].append(transition)

    def can_transition(self, agent: Agent) -> bool:
        """检查是否可以转移"""
        if self.current_state not in self.transition_map:
            return False

        for transition in self.transition_map[self.current_state]:
            if transition.required_role == agent.role:
                return True
        return False

    def transition(self, agent: Agent) -> bool:
        """执行转移"""
        if not self.can_transition(agent):
            return False

        for transition in self.transition_map[self.current_state]:
            if transition.required_role == agent.role:
                self.current_state = transition.to_state
                if transition.action:
                    transition.action()
                return True
        return False

    def get_next_state(self) -> Optional[WorkflowState]:
        """获取下一个状态"""
        if self.current_state in self.transition_map:
            transitions = self.transition_map[self.current_state]
            if transitions:
                return transitions[0].to_state
        return None

    def get_required_role(self) -> Optional[AgentRole]:
        """获取当前状态所需的角色"""
        if self.current_state in self.transition_map:
            transitions = self.transition_map[self.current_state]
            if transitions:
                return transitions[0].required_role
        return None

    def reset(self):
        """重置工作流"""
        self.current_state = WorkflowState.IDLE
