from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]


class PieRuntimeVerificationPolicyTest(unittest.TestCase):
    def test_mcp_pie_runtime_verification_requires_mobile_simulation(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        integration = (
            SKILL_ROOT / "references" / "mcp-integration.md"
        ).read_text(encoding="utf-8")

        self.assertIn('simulation_platform="mobile"', skill)
        self.assertIn('simulation_platform="mobile"', integration)
        self.assertIn("existing PIE session is not mobile", integration)
        self.assertIn('"simulation_platform":"mobile"', integration)


if __name__ == "__main__":
    unittest.main()
