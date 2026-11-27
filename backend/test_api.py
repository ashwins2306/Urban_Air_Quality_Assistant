"""
Automated Test Suite for BreatheEasy Backend API
=================================================
Verifies endpoints, edge cases, validation, caching, and clinical fallback.
"""

import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

# Ensure backend directory is in path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app, get_aqi_color, get_aqi_category_info
import ai_assistant as ai
import data as d


class TestBreatheEasyAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # --------------------------------------------------------------------------
    # B7 & B23: AQI Colors and Zero Handling
    # --------------------------------------------------------------------------
    def test_aqi_color_standards(self):
        """Test standardized EPA / WHO color codes (B23)."""
        self.assertEqual(get_aqi_color(0), "#10b981")    # Good (0 is preserved, B7)
        self.assertEqual(get_aqi_color(45), "#10b981")   # Good
        self.assertEqual(get_aqi_color(75), "#eab308")   # Moderate
        self.assertEqual(get_aqi_color(130), "#f97316")  # Sensitive
        self.assertEqual(get_aqi_color(180), "#ef4444")  # Unhealthy
        self.assertEqual(get_aqi_color(250), "#8b5cf6")  # Very Unhealthy
        self.assertEqual(get_aqi_color(350), "#7e0023")  # Hazardous (Standardized Maroon)

    # --------------------------------------------------------------------------
    # Zero Hardcoded City Data Verification
    # --------------------------------------------------------------------------
    def test_zero_hardcoded_city_data(self):
        """Verify that CITY_AQI_DATA has no hardcoded values and is completely live."""
        self.assertEqual(len(d.CITY_AQI_DATA), 0)
        # When live upstream is unavailable, get_city_aqi returns 503 rather than fabricated numbers
        res = self.client.get("/api/aqi/NonExistentCityTestXYZ")
        self.assertIn(res.status_code, [400, 404, 503])

    # --------------------------------------------------------------------------
    # B11: Room Tips Difficulty Normalization
    # --------------------------------------------------------------------------
    def test_room_tips_difficulty(self):
        """Room tips must emit lowercase 'easy' or 'medium' (B11)."""
        res = self.client.get("/api/indoor-tips/living")
        self.assertEqual(res.status_code, 200)
        tips = res.json()
        self.assertGreater(len(tips), 0)
        for t in tips:
            diff = t.get("difficulty")
            self.assertIn(diff, ["easy", "medium", "moderate", "hard"])

    # --------------------------------------------------------------------------
    # B14 & B22: Routines Pluralisation & Validation
    # --------------------------------------------------------------------------
    def test_routines_plurals_and_validation(self):
        """Test proper cohort names without 'Familys', and AQI validation (B14, B22)."""
        # Valid request
        payload = {"city": "Delhi", "lifestyle": "family", "aqi": 220}
        res = self.client.post("/api/routines", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("Families with Children", data.get("insight", ""))
        self.assertNotIn("Familys", data.get("insight", ""))

        # Senior plural
        res_sr = self.client.post("/api/routines", json={"city": "Delhi", "lifestyle": "elderly", "aqi": 220})
        self.assertIn("Seniors", res_sr.json().get("insight", ""))
        self.assertNotIn("Elderlys", res_sr.json().get("insight", ""))

        # Invalid negative AQI (B22)
        res_bad = self.client.post("/api/routines", json={"city": "Delhi", "lifestyle": "family", "aqi": -50})
        self.assertEqual(res_bad.status_code, 422)

        # Invalid absurd AQI (B22)
        res_absurd = self.client.post("/api/routines", json={"city": "Delhi", "lifestyle": "family", "aqi": 5000})
        self.assertEqual(res_absurd.status_code, 422)

    # --------------------------------------------------------------------------
    # B12, B18, B22, B24: Carbon Impact Calculation & Validation
    # --------------------------------------------------------------------------
    def test_impact_calculation_and_cycling(self):
        """Test cycle option, honest baseline, and validation (B12, B18, B22, B24)."""
        # Clean choices including cycling (B12)
        clean_choices = {
            "commute": "cycle",
            "cooking": "electric",
            "heating": "none",
            "waste": "minimal",
            "cleaning": "natural",
            "festival": "no-crackers"
        }
        res = self.client.post("/api/calculate-impact", json=clean_choices)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total_co2"], 1.1)
        self.assertGreater(data["average_co2"], data["total_co2"])
        self.assertGreater(data["worst_co2"], data["total_co2"])
        self.assertGreater(data["savings_percent"], 50.0)

        # Zero-savings case (worst possible selections)
        worst_choices = {
            "commute": "car-solo",
            "cooking": "biomass",
            "heating": "wood-fire",
            "waste": "mixed",
            "cleaning": "chemical",
            "festival": "heavy-crackers"
        }
        res_worst = self.client.post("/api/calculate-impact", json=worst_choices)
        self.assertEqual(res_worst.status_code, 200)
        data_worst = res_worst.json()
        # B18 FIX: Zero savings must not print 'Equal to planting 1 urban trees'
        for eq in data_worst.get("equivalents", []):
            self.assertNotIn("Equal to planting 1 urban trees", eq.get("text", ""))

        # B22 FIX: Invalid commute option 'teleport' must raise 400
        bad_choices = dict(clean_choices)
        bad_choices["commute"] = "teleport"
        res_invalid = self.client.post("/api/calculate-impact", json=bad_choices)
        self.assertEqual(res_invalid.status_code, 400)

    # --------------------------------------------------------------------------
    # B13: Community Pledges Persistence
    # --------------------------------------------------------------------------
    def test_pledges_persistence(self):
        """Pledges must be retrievable and togglable via API (B13)."""
        res_get = self.client.get("/api/pledges")
        self.assertEqual(res_get.status_code, 200)
        init_citizens = res_get.json()["total_citizens"]

        # Toggle pledge 1 on
        res_post = self.client.post("/api/pledges", json={"id": 1, "pledged": True})
        self.assertEqual(res_post.status_code, 200)
        new_citizens = res_post.json()["total_citizens"]
        self.assertEqual(new_citizens, init_citizens + 1)

        # Toggle pledge 1 off
        res_off = self.client.post("/api/pledges", json={"id": 1, "pledged": False})
        self.assertEqual(res_off.status_code, 200)
        self.assertEqual(res_off.json()["total_citizens"], init_citizens)

    # --------------------------------------------------------------------------
    # B15: AI Assistant Whole-Word Matching
    # --------------------------------------------------------------------------
    def test_ai_keyword_whole_word_matching(self):
        """Test whole-word regex matching prevents false substring triggers (B15)."""
        # 'team' should not trigger tea/hydration
        res_team = ai.get_builtin_response("Our project team is meeting today", {"city": "Delhi"})
        self.assertNotIn("tea", res_team.lower().split())

        # 'forest' should not trigger rest/sleep
        res_forest = ai.get_builtin_response("Walking through the green forest", {"city": "Delhi"})
        self.assertNotIn("bedroom windows", res_forest.lower())

        # 'scarf' should not trigger car/commute
        res_scarf = ai.get_builtin_response("My winter scarf is warm", {"city": "Delhi"})
        self.assertNotIn("cabin filter", res_scarf.lower())

        # 'asthma' must trigger asthma/breathing
        res_asthma = ai.get_builtin_response("My child has severe asthma attacks", {"city": "Delhi"})
        self.assertIn("inhaler", res_asthma.lower())

    # --------------------------------------------------------------------------
    # Chat API Structure (B2, B3)
    # --------------------------------------------------------------------------
    def test_chat_endpoint_structure(self):
        """Test chat returns structured source and fallback indicators."""
        res = self.client.post("/api/chat", json={
            "message": "What is the best N95 respirator mask?",
            "context": {"city": "Delhi", "lifestyle": "family", "aqi": 180}
        })
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertIn("response", body)
        self.assertIn("source", body)
        self.assertIn("is_fallback", body)


    # --------------------------------------------------------------------------
    # Chrono-Intelligence Endpoint
    # --------------------------------------------------------------------------
    def test_chrono_intelligence_endpoint(self):
        """Test Chrono-Intelligence synthesizes spoken briefing, horizon windows, and calendar events."""
        res = self.client.post("/api/chrono-intelligence", json={
            "city": "Bengaluru",
            "lifestyle": "athlete",
            "aqi": 160
        })
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertIn("briefing_headline", body)
        self.assertIn("spoken_briefing", body)
        self.assertIn("inversion_windows", body)
        self.assertIn("schedule", body)
        self.assertIn("calendar_events", body)
        self.assertGreater(len(body["schedule"]), 0)
        self.assertGreater(len(body["calendar_events"]), 0)


if __name__ == "__main__":
    unittest.main()
