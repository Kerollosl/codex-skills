"""Pure tracking operations; no network, Drive writes, or image generation.

CLI: python3 youtube_state.py migrate INPUT OUTPUT
     python3 youtube_state.py plan STATE CHANNEL UTC_NOW CANDIDATES_JSON
Candidates contain id and optionally published_at (UTC), upload_date, date_certain.
Import record_channel for checkpointing actual review outcomes.
"""
import argparse
import copy
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

CHANNELS = ("PaulJLipsky", "Chase-H-AI", "GoogleDevelopers", "OpenAI",
            "claude", "NikiasMolina", "Good__News")


def utc(value):
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise ValueError("An actual timezone-qualified UTC timestamp is required")
    return dt


def video_id(value):
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        raise ValueError("Use the observed canonical 11-character video ID")
    return value


def migrate(state):
    result = copy.deepcopy(state)
    channels = set(CHANNELS)
    for key in ("youtube_last_checked", "youtube_last_checked_at",
                "youtube_processed_video_ids", "youtube_retry_videos"):
        channels.update(result.get(key, {}))
    for key, default in (("youtube_last_checked_at", None),
                         ("youtube_processed_video_ids", []),
                         ("youtube_retry_videos", {})):
        mapping = result.setdefault(key, {})
        for channel in channels:
            mapping.setdefault(channel, copy.deepcopy(default))
    result.setdefault("youtube_pending_good_news", {})
    return result


def scan_floor(state, channel, now):
    """Inclusive UTC date floor: boundary day plus two preceding days."""
    now_dt = utc(now)
    stamp = state.get("youtube_last_checked_at", {}).get(channel)
    legacy = state.get("youtube_last_checked", {}).get(channel)
    if stamp:
        anchor = utc(stamp)
    elif legacy:
        anchor = datetime.fromisoformat(legacy).replace(tzinfo=timezone.utc)
    else:
        return (now_dt - timedelta(days=7)).date().isoformat()
    return (anchor - timedelta(days=2)).date().isoformat()


def plan(state, channel, now, candidates):
    state = migrate(state)
    floor = scan_floor(state, channel, now)
    processed = set(state["youtube_processed_video_ids"].get(channel, []))
    staged = set(state["youtube_pending_good_news"]) if channel == "Good__News" else set()
    retry = state["youtube_retry_videos"].get(channel, {})
    pool = {video_id(v["id"]): copy.deepcopy(v) for v in candidates}
    for vid, entry in retry.items():
        pool.setdefault(video_id(vid), dict(entry, id=vid))
    selected = []
    for vid, entry in pool.items():
        if vid in processed or vid in staged:
            continue
        date = entry.get("upload_date")
        if entry.get("published_at"):
            date = utc(entry["published_at"]).date().isoformat()
        if vid in retry or not date or not entry.get("date_certain", False) or date >= floor:
            selected.append(entry)
    return {"inclusive_upload_date_floor": floor, "review": selected,
            "pending_good_news": copy.deepcopy(state["youtube_pending_good_news"])
            if channel == "Good__News" else {}}


def record_channel(state, channel, scan_started_at, outcomes, *,
                   discovery_complete=False, good_news_delivered=False,
                   format_only=False):
    """Checkpoint read successes and retries; advance only complete coverage.

    outcomes: [{id, status: reviewed|failed|unread, ...}]. Good News reviewed
    outcomes must include items (complete inventory) and source_url. Delivery
    means every staged item was verified and delivered, not merely generated.
    discovery_complete means every planned candidate was accounted for and
    the full inclusive window was enumerated (including Good News Shorts).
    """
    if format_only:
        return copy.deepcopy(state)
    utc(scan_started_at)
    result = migrate(state)
    processed = result["youtube_processed_video_ids"].setdefault(channel, [])
    retry = result["youtube_retry_videos"].setdefault(channel, {})
    staged = result["youtube_pending_good_news"]
    for outcome in outcomes:
        entry = copy.deepcopy(outcome)
        vid = video_id(entry.pop("id"))
        status = entry.get("status")
        if status not in ("reviewed", "failed", "unread"):
            raise ValueError("Unknown review outcome")
        if vid in processed:
            continue
        if status == "reviewed":
            if channel == "Good__News":
                if not isinstance(entry.get("items"), list) or not entry.get("source_url"):
                    raise ValueError("Persist the complete Good News inventory and source URL")
                staged[vid] = entry
            elif vid not in processed:
                processed.append(vid)
            retry.pop(vid, None)
        else:
            if channel == "Good__News" and vid in staged:
                continue  # Already read; retry delivery using the stored inventory.
            retry[vid] = entry
    complete = discovery_complete and not retry
    if channel == "Good__News":
        if complete and good_news_delivered:
            for vid in staged:
                if vid not in processed:
                    processed.append(vid)
            staged.clear()
        complete = complete and good_news_delivered and not staged
    if complete:
        old = result["youtube_last_checked_at"].get(channel)
        if old is None or utc(scan_started_at) >= utc(old):
            result["youtube_last_checked_at"][channel] = scan_started_at
            result.setdefault("youtube_last_checked", {})[channel] = utc(scan_started_at).date().isoformat()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    migration = commands.add_parser("migrate")
    migration.add_argument("input")
    migration.add_argument("output")
    planning = commands.add_parser("plan")
    for field in ("state", "channel", "utc_now", "candidates"):
        planning.add_argument(field)
    args = parser.parse_args()
    if args.command == "migrate":
        result = migrate(json.loads(Path(args.input).read_text()))
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    else:
        result = plan(json.loads(Path(args.state).read_text()), args.channel,
                      args.utc_now, json.loads(Path(args.candidates).read_text()))
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
