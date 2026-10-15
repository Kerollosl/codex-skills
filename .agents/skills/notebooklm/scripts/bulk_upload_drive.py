#!/usr/bin/env python3
"""
Bulk upload Google Drive documents to NotebookLM.

Extracts Drive IDs from .gdoc/.gsheet/.gslides shortcut files (which are
JSON pointers, not real files) and adds them to a NotebookLM notebook
via the notebooklm-rest-api server.

Usage:
    python bulk_upload_drive.py --dir <path> --title "<notebook title>"
    python bulk_upload_drive.py --dir <path> --notebook-id <existing-id>
    python bulk_upload_drive.py --dir <path> --title "..." --dry-run

Prerequisites:
    1. notebooklm-rest-api server running on localhost:8000
       (https://github.com/gnh1201/notebooklm-rest-api)
    2. Authenticated via `notebooklm login` (one-time setup)

Why this script exists:
    Google Drive shortcut files (.gdoc, .gsheet, .gslides) cannot be
    uploaded directly — they're JSON pointers containing a `doc_id` field
    that references the actual cloud document. This script extracts those
    IDs, builds shareable Drive URLs, and adds them as URL sources.
"""

import argparse
import glob
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("❌ Missing dependency: pip install requests")
    sys.exit(1)


DEFAULT_BASE_URL = "http://localhost:8000"
SUPPORTED_EXTENSIONS = ['.gdoc', '.gslides', '.gsheet']


def extract_drive_id(file_path):
    """Extract Drive ID from a .gdoc/.gsheet/.gslides shortcut file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        drive_id = data.get('doc_id') or data.get('id') or data.get('resourceName')
        if drive_id and '/' in str(drive_id):
            drive_id = drive_id.split('/')[-1]
        return drive_id
    except (json.JSONDecodeError, OSError):
        return None


def find_drive_documents(directory):
    """Recursively find all Google Drive shortcut files and extract IDs."""
    docs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                drive_id = extract_drive_id(file_path)
                if drive_id:
                    docs.append({
                        'name': os.path.basename(file_path),
                        'path': file_path,
                        'drive_id': drive_id,
                        'url': f"https://drive.google.com/file/d/{drive_id}/view",
                    })
    return sorted(docs, key=lambda d: d['name'])


def check_server(base_url):
    """Verify the notebooklm-rest-api server is reachable."""
    try:
        requests.get(f"{base_url}/v1/notebooks", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False


def create_notebook(base_url, title):
    """Create a new notebook and return its ID."""
    response = requests.post(
        f"{base_url}/v1/notebooks",
        json={"title": title},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    # Response shape: {"ok": True, "notebook": {"id": "...", ...}}
    notebook_id = (
        data.get("notebook", {}).get("id")
        or data.get("id")
        or data.get("notebook_id")
    )
    if not notebook_id:
        raise ValueError(f"Could not extract notebook ID from response: {data}")
    return notebook_id


def add_url_source(base_url, notebook_id, url, wait=False):
    """Add a single Drive URL as a source to the notebook."""
    response = requests.post(
        f"{base_url}/v1/notebooks/{notebook_id}/sources/url",
        json={"url": url, "wait": wait},
        timeout=60,
    )
    return response.status_code in (200, 201)


def main():
    parser = argparse.ArgumentParser(
        description="Bulk upload Google Drive documents to NotebookLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--dir', default='.', help='Directory to scan (default: current)')
    parser.add_argument('--title', help='Title for new notebook')
    parser.add_argument('--notebook-id', help='Existing notebook ID to add to')
    parser.add_argument('--base-url', default=DEFAULT_BASE_URL, help='REST API base URL')
    parser.add_argument('--delay', type=float, default=0.3, help='Delay between uploads (seconds)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be uploaded without doing it')
    args = parser.parse_args()

    if not args.title and not args.notebook_id and not args.dry_run:
        parser.error("Either --title (for new notebook) or --notebook-id (to add to existing) is required")

    print("=" * 60)
    print("📚 NotebookLM Drive Bulk Upload")
    print("=" * 60)

    # Find documents
    print(f"\n🔍 Scanning: {os.path.abspath(args.dir)}")
    docs = find_drive_documents(args.dir)
    if not docs:
        print("❌ No Google Drive shortcut files (.gdoc/.gsheet/.gslides) found")
        sys.exit(1)
    print(f"✅ Found {len(docs)} documents")

    if args.dry_run:
        print("\n📋 Dry run — would upload:")
        for doc in docs:
            print(f"   • {doc['name']}")
        print(f"\n📊 Total: {len(docs)} documents")
        return

    # Verify server
    print(f"\n🔌 Checking server at {args.base_url}...")
    if not check_server(args.base_url):
        print(f"❌ Server unreachable. Start it with:")
        print(f"   uvicorn app:app --host 0.0.0.0 --port 8000")
        sys.exit(1)
    print("✅ Server is running")

    # Get or create notebook
    if args.notebook_id:
        notebook_id = args.notebook_id
        print(f"\n📘 Using existing notebook: {notebook_id}")
    else:
        print(f"\n📘 Creating notebook: {args.title}")
        try:
            notebook_id = create_notebook(args.base_url, args.title)
            print(f"✅ Created: {notebook_id}")
        except Exception as e:
            print(f"❌ Failed to create notebook: {e}")
            sys.exit(1)

    # Upload
    print(f"\n📤 Adding {len(docs)} documents...")
    print("-" * 60)
    success = failed = 0
    for i, doc in enumerate(docs, 1):
        if add_url_source(args.base_url, notebook_id, doc['url']):
            print(f"[{i}/{len(docs)}] ✅ {doc['name']}")
            success += 1
        else:
            print(f"[{i}/{len(docs)}] ⚠️  {doc['name']}")
            failed += 1
        if args.delay > 0:
            time.sleep(args.delay)

    # Summary
    print("-" * 60)
    print(f"\n📊 Summary: ✅ {success} added, ⚠️  {failed} failed, total {len(docs)}")
    print(f"🔗 https://notebooklm.google.com/notebook/{notebook_id}")
    print("⏳ Documents process in the background — check NotebookLM in a few minutes.\n")


if __name__ == "__main__":
    main()
