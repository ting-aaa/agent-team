"""初始化脚本"""
from agents.roles import Producer, Designer, Programmer, Artist, DevOps


def init_team():
    """初始化团队"""
    team = {
        "producer": Producer("Producer"),
        "designer": Designer("Designer"),
        "programmer": Programmer("Programmer"),
        "artist": Artist("Artist"),
        "devops": DevOps("DevOps"),
    }

    # 保存所有Agent
    for agent in team.values():
        agent.save()

    return team


if __name__ == "__main__":
    team = init_team()
    print("[OK] Team initialized")
    for name, agent in team.items():
        print(f"  - {agent.name} ({agent.role.value})")
