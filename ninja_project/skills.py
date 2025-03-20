class SkillTree:
    def __init__(self):
        self.skills = {
            "shadow_clone": {"level": 0, "max_level": 3},
            "speed": {"level": 0, "max_level": 5},
        }

    def upgrade(self, skill):
        if self.skills[skill]["level"] < self.skills[skill]["max_level"]:
            self.skills[skill]["level"] += 1