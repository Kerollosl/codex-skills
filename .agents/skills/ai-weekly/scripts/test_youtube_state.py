"""Offline regression fixtures; never touch live Drive state."""
import unittest
from youtube_state import migrate, plan, record_channel

C = "PaulJLipsky"
G = "Good__News"
NOW = "2026-10-03T16:00:00Z"
A, B, F = "Reviewed001", "SameDay0001", "Failed00001"


class TrackingTests(unittest.TestCase):
    def setUp(self):
        self.legacy = {"youtube_last_checked": {C: "2026-10-03", G: "2026-10-03"},
                       "ipo_status": {"openai": "unchanged"},
                       "history": [{"date": "2026-09-30", "extra": [1, 2]}],
                       "last_full_digest_run": "2026-10-03"}
        self.state = migrate(self.legacy)
        self.state["youtube_processed_video_ids"][C] = [A]
        self.state["youtube_last_checked_at"][C] = "2026-10-03T10:00:00Z"

    def test_migration_preserves_legacy_and_is_idempotent(self):
        new = migrate(self.legacy)
        for key, value in self.legacy.items():
            self.assertEqual(new[key], value)
        self.assertIsNone(new["youtube_last_checked_at"][C])
        self.assertEqual(new["youtube_processed_video_ids"][C], [])
        self.assertEqual(migrate(new), new)

    def test_repeated_run_skips_success(self):
        result = plan(self.state, C, NOW, [{"id": A, "upload_date": "2026-10-03"}])
        self.assertEqual(result["review"], [])

    def test_new_same_day_upload_after_check_is_selected(self):
        result = plan(self.state, C, NOW, [
            {"id": A, "published_at": "2026-10-03T08:00:00Z", "date_certain": True},
            {"id": B, "published_at": "2026-10-03T12:00:00Z", "date_certain": True}])
        self.assertEqual([v["id"] for v in result["review"]], [B])

    def test_inclusive_boundary_and_uncertain_dates(self):
        result = plan(self.state, C, NOW, [
            {"id": B, "upload_date": "2026-10-01", "date_certain": True},
            {"id": F, "upload_date": "2026-09-01", "date_certain": False}])
        self.assertEqual(len(result["review"]), 2)
        self.assertEqual(result["inclusive_upload_date_floor"], "2026-10-01")

    def test_failure_retries_even_when_missing_and_old(self):
        result = record_channel(self.state, C, NOW, [
            {"id": B, "status": "reviewed"},
            {"id": F, "status": "failed", "upload_date": "2026-09-01",
             "date_certain": True, "source_url": "https://www.youtube.com/watch?v=" + F}],
            discovery_complete=True)
        self.assertIn(B, result["youtube_processed_video_ids"][C])
        self.assertNotIn(F, result["youtube_processed_video_ids"][C])
        self.assertEqual(result["youtube_last_checked_at"][C], self.state["youtube_last_checked_at"][C])
        self.assertEqual([v["id"] for v in plan(result, C, NOW, [])['review']], [F])
        retried = record_channel(result, C, NOW, [{"id": F, "status": "reviewed"}],
                                 discovery_complete=True)
        self.assertIn(F, retried["youtube_processed_video_ids"][C])
        self.assertEqual(retried["youtube_retry_videos"][C], {})
        self.assertEqual(retried["youtube_last_checked_at"][C], NOW)
        self.assertEqual(retried["history"], self.legacy["history"])

    def test_unread_and_incomplete_discovery_do_not_advance(self):
        new = record_channel(self.state, C, NOW, [{"id": F, "status": "unread"}],
                             discovery_complete=False)
        self.assertIn(F, new["youtube_retry_videos"][C])
        self.assertEqual(new["youtube_last_checked_at"][C], self.state["youtube_last_checked_at"][C])

    def test_good_news_failed_image_reuses_inventory(self):
        entry = {"id": B, "status": "reviewed", "items": ["A factual story."],
                 "source_url": "https://www.youtube.com/watch?v=" + B}
        staged = record_channel(self.state, G, NOW, [entry], discovery_complete=True)
        self.assertNotIn(B, staged["youtube_processed_video_ids"][G])
        self.assertIsNone(staged["youtube_last_checked_at"][G])
        next_plan = plan(staged, G, NOW, [{"id": B}])
        self.assertEqual(next_plan["review"], [])
        self.assertEqual(next_plan["pending_good_news"][B]["items"], entry["items"])
        delivered = record_channel(staged, G, NOW, [], discovery_complete=True,
                                   good_news_delivered=True)
        self.assertEqual(delivered["youtube_processed_video_ids"][G], [B])
        self.assertEqual(delivered["youtube_pending_good_news"], {})
        self.assertEqual(delivered["youtube_last_checked_at"][G], NOW)

    def test_format_only_has_no_state_effects(self):
        result = record_channel(self.legacy, G, NOW, [{"id": B, "status": "reviewed"}],
                                 discovery_complete=True, good_news_delivered=True,
                                 format_only=True)
        self.assertEqual(result, self.legacy)

    def test_custom_channel_in_new_map_is_preserved_and_initialized(self):
        legacy = dict(self.legacy, youtube_processed_video_ids={"CustomChannel": [A]})
        new = migrate(legacy)
        self.assertEqual(new["youtube_processed_video_ids"]["CustomChannel"], [A])
        self.assertIsNone(new["youtube_last_checked_at"]["CustomChannel"])
        self.assertEqual(new["youtube_retry_videos"]["CustomChannel"], {})

    def test_good_news_no_items_still_requires_verified_delivery(self):
        incomplete = record_channel(self.state, G, NOW, [], discovery_complete=True)
        self.assertIsNone(incomplete["youtube_last_checked_at"][G])
        complete = record_channel(incomplete, G, NOW, [], discovery_complete=True,
                                  good_news_delivered=True)
        self.assertEqual(complete["youtube_last_checked_at"][G], NOW)

    def test_ipo_only_migration_does_not_advance_tracking(self):
        new = migrate(self.state)
        self.assertEqual(new, self.state)

    def test_checkpoint_uses_scan_start_and_never_moves_back(self):
        new = record_channel(self.state, C, "2026-10-03T09:00:00Z", [],
                             discovery_complete=True)
        self.assertEqual(new["youtube_last_checked_at"][C], "2026-10-03T10:00:00Z")
        advanced = record_channel(new, C, NOW, [], discovery_complete=True)
        self.assertEqual(advanced["youtube_last_checked_at"][C], NOW)


if __name__ == "__main__":
    unittest.main()
