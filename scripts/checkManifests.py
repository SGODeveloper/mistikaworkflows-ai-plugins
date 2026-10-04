#!/usr/bin/env python3
"""Checks the plugins of this marketplace before a release.

Each plugin is described twice: once for Claude (.claude-plugin/plugin.json)
and once in the portable Agent Plugins format used by ChatGPT and Codex
(plugin.json, with the OpenAI listing under extensions.com.openai). This
script checks that both manifests agree on the package identity (name,
version, author, links, license, keywords), that the OpenAI listing fits the
directory limits, that every referenced file exists, and that every skill has
a valid header.

Usage: python3 scripts/checkManifests.py   (from anywhere; exit code 1 on errors)
"""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path
from typing import Any, Dict

from checkReport import CcheckReport

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_FILE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
CLAUDE_MANIFEST = Path(".claude-plugin") / "plugin.json"
PORTABLE_MANIFEST = Path("plugin.json")

AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PORTABLE_ROOT_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
PLUGIN_NAME_PATTERN = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")

# Fields both manifests must share.
SHARED_FIELDS = ("name", "version", "author", "homepage", "repository", "license", "keywords")

# OpenAI listing limits (plugin submission reference).
TEXT_LIMITS = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
REQUIRED_INTERFACE_FIELDS = ("displayName", "shortDescription", "longDescription", "developerName", "category", "logo")
URL_FIELDS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
IMAGE_FIELDS = ("composerIcon", "composerIconDark", "logo", "logoDark")
MAX_PROMPTS, MAX_PROMPT_LENGTH = 3, 128
MAX_CAPABILITIES, MAX_CAPABILITY_LENGTH = 20, 120
MAX_IMAGE_BYTES = 5 * 1024 * 1024
MIN_ICON_SIZE = 48
COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


def loadJson(path: Path, report: CcheckReport) -> Dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(str(path.relative_to(REPO_ROOT)), "file not found")
    except json.JSONDecodeError as exception:
        report.error(str(path.relative_to(REPO_ROOT)), f"invalid JSON ({exception})")
    return None


def pngSize(path: Path) -> tuple[int, int] | None:
    """Width and height of a PNG file, None when it is not a PNG."""
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", header[16:24])


def checkRelativeFile(pluginDir: Path, value: str, where: str, report: CcheckReport) -> Path | None:
    if not value.startswith("./"):
        report.error(where, f"path '{value}' must start with './'")
        return None
    path = (pluginDir / value).resolve()
    if pluginDir.resolve() not in path.parents:
        report.error(where, f"path '{value}' is outside the plugin folder")
        return None
    if not path.is_file():
        report.error(where, f"file '{value}' not found")
        return None
    return path


def checkPortableManifest(manifest: Dict[str, Any], where: str, report: CcheckReport) -> None:
    if manifest.get("$schema") != AGENT_PLUGINS_SCHEMA:
        report.error(where, f"$schema must be {AGENT_PLUGINS_SCHEMA}")
    for key in sorted(set(manifest) - PORTABLE_ROOT_KEYS):
        report.error(where, f"'{key}' is not allowed at the root of an Agent Plugins manifest")
    name = manifest.get("name", "")
    if not isinstance(name, str) or len(name) > 64 or not PLUGIN_NAME_PATTERN.match(name):
        report.error(where, f"invalid plugin name '{name}'")
    if not manifest.get("version"):
        report.error(where, "version is required for submission")


def checkOpenAiListing(pluginDir: Path, manifest: Dict[str, Any], where: str, report: CcheckReport) -> None:
    openAi = manifest.get("extensions", {}).get("com.openai")
    if openAi is None:
        report.warning(where, "no extensions.com.openai: the ChatGPT listing will need to be filled in the dashboard")
        return
    interface = openAi.get("interface", {})
    listing = f"{where} (com.openai.interface)"

    for field in REQUIRED_INTERFACE_FIELDS:
        if not interface.get(field):
            report.error(listing, f"'{field}' is required for submission")
    for field, limit in TEXT_LIMITS.items():
        text = interface.get(field, "")
        if len(text) > limit:
            report.error(listing, f"'{field}' has {len(text)} characters (limit {limit})")

    prompts = interface.get("defaultPrompt", [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    if len(prompts) > MAX_PROMPTS:
        report.error(listing, f"{len(prompts)} default prompts (limit {MAX_PROMPTS})")
    if len(set(prompts)) != len(prompts):
        report.error(listing, "default prompts must be unique")
    for prompt in prompts:
        if len(prompt) > MAX_PROMPT_LENGTH:
            report.error(listing, f"default prompt longer than {MAX_PROMPT_LENGTH} characters: '{prompt}'")

    capabilities = interface.get("capabilities", [])
    if len(capabilities) > MAX_CAPABILITIES:
        report.error(listing, f"{len(capabilities)} capabilities (limit {MAX_CAPABILITIES})")
    for capability in capabilities:
        if len(capability) > MAX_CAPABILITY_LENGTH:
            report.error(listing, f"capability longer than {MAX_CAPABILITY_LENGTH} characters: '{capability}'")

    for field in URL_FIELDS:
        url = interface.get(field)
        if url is not None and not url.startswith("https://"):
            report.error(listing, f"'{field}' must be an HTTPS URL")
    if "termsOfServiceURL" not in interface:
        report.warning(listing, "no termsOfServiceURL: required only if the plugin gets an MCP server")

    for field in ("brandColor", "brandColorDark"):
        color = interface.get(field)
        if color is not None and not COLOR_PATTERN.match(color):
            report.error(listing, f"'{field}' must be #RRGGBB")

    for field in IMAGE_FIELDS:
        value = interface.get(field)
        if value is None:
            continue
        path = checkRelativeFile(pluginDir, value, f"{listing} {field}", report)
        if path is None:
            continue
        if path.stat().st_size > MAX_IMAGE_BYTES:
            report.error(listing, f"'{field}' is larger than 5 MiB")
        size = pngSize(path) if path.suffix.lower() == ".png" else None
        if size is not None and (size[0] != size[1] or size[0] < MIN_ICON_SIZE):
            report.error(listing, f"'{field}' must be square and at least {MIN_ICON_SIZE}x{MIN_ICON_SIZE} (it is {size[0]}x{size[1]})")

    onboardingSkill = openAi.get("onboardingSkill")
    if onboardingSkill is not None:
        checkRelativeFile(pluginDir, onboardingSkill, f"{where} onboardingSkill", report)


def readFrontmatter(text: str) -> Dict[str, str] | None:
    """Plain 'key: value' pairs of a SKILL.md header, None without a header."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return None


def checkSkills(pluginDir: Path, where: str, report: CcheckReport) -> None:
    skillFiles = sorted((pluginDir / "skills").glob("*/SKILL.md"))
    if not skillFiles:
        report.error(where, "no skills/<name>/SKILL.md found")
    for skillFile in skillFiles:
        skillWhere = str(skillFile.relative_to(REPO_ROOT))
        fields = readFrontmatter(skillFile.read_text(encoding="utf-8"))
        if fields is None:
            report.error(skillWhere, "missing '---' header")
            continue
        if fields.get("name") != skillFile.parent.name:
            report.error(skillWhere, f"name '{fields.get('name')}' must match its folder '{skillFile.parent.name}'")
        description = fields.get("description", "")
        if not description:
            report.error(skillWhere, "description is required")
        elif ": " in description:
            # ': ' inside a plain YAML scalar breaks the header.
            report.error(skillWhere, "description contains ': ', which breaks the YAML header")


def checkAscii(pluginDir: Path, report: CcheckReport) -> None:
    for path in sorted(pluginDir.rglob("*")):
        if path.suffix.lower() in (".md", ".json") and path.is_file():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if any(ord(character) > 127 for character in line):
                    report.warning(f"{path.relative_to(REPO_ROOT)}:{number}", "non-ASCII characters")


def checkPlugin(entry: Dict[str, Any], report: CcheckReport) -> None:
    source = entry.get("source", "")
    pluginDir = (REPO_ROOT / source).resolve()
    where = source or "<no source>"
    if not isinstance(source, str) or not pluginDir.is_dir():
        report.error(where, "marketplace source folder not found")
        return

    claudeManifest = loadJson(pluginDir / CLAUDE_MANIFEST, report)
    if claudeManifest is None:
        return
    if claudeManifest.get("name") != entry.get("name"):
        report.error(where, "the marketplace entry and .claude-plugin/plugin.json have different names")

    portablePath = pluginDir / PORTABLE_MANIFEST
    if not portablePath.is_file():
        report.warning(where, "no plugin.json: Claude-only plugin (ChatGPT and Codex fall back to the Claude manifest)")
    else:
        portableManifest = loadJson(portablePath, report)
        if portableManifest is not None:
            portableWhere = str(portablePath.relative_to(REPO_ROOT))
            checkPortableManifest(portableManifest, portableWhere, report)
            for field in SHARED_FIELDS:
                if claudeManifest.get(field) != portableManifest.get(field):
                    report.error(where, f"'{field}' differs between .claude-plugin/plugin.json and plugin.json")
            checkOpenAiListing(pluginDir, portableManifest, portableWhere, report)

    checkSkills(pluginDir, where, report)
    checkAscii(pluginDir, report)


def main() -> int:
    report = CcheckReport()
    marketplace = loadJson(MARKETPLACE_FILE, report)
    entries = marketplace.get("plugins", []) if marketplace else []
    for entry in entries:
        checkPlugin(entry, report)

    for warning in report.warnings:
        print(f"warning: {warning}")
    for error in report.errors:
        print(f"error: {error}")
    names = ", ".join(entry.get("name", "?") for entry in entries)
    print(f"{len(entries)} plugin(s) checked ({names}): {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
