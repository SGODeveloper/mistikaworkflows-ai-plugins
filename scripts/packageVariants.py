"""The packages of the plugins for directories with their own listing rules.

The skills and the README of a plugin are written once, for every app, and
the Claude directory and the marketplace in this repository use them as they
are. The Claude directory does not list software that generates audio, video
or images with an AI model, so the plugin folder leaves those features of
Mistika Workflows out and tells the assistant not to use them
(scripts/checkManifests.py checks it). A directory whose rules differ gets a
variant of the package, built by scripts/buildPackages.py:

- openai: the OpenAI plugin directory (ChatGPT and Codex). Its guidelines do
  not allow advertising pricing, subscriptions, free trials, discounts or
  promotions, linking to checkout, plans or upgrade pages, or displaying
  subscription plans. Its package leaves out the free evaluation and the
  plans page: for licenses it points to the Mistika Workflows page, the same
  page as the websiteURL of the listing. Its review also flags descriptions
  that reference another AI assistant, so the skill descriptions and the
  introduction of the README name no other assistant. Its package offers
  every feature of Mistika Workflows, the AI dubbing, voice and enhancement
  services included.
"""

from __future__ import annotations

from typing import Tuple

from checkManifests import PORTABLE_MANIFEST, checkPortablePackage
from forbiddenText import CforbiddenText
from packageVariant import CpackageVariant
from textReplacement import CtextReplacement

# Where the OpenAI package sends the user for licenses.
WORKFLOWS_PAGE_LINK = "[Mistika Workflows page](https://www.sgo.es/mistika-workflows/)"

# Text that the OpenAI guidelines do not allow, or that points to the plans
# page; the build fails when any of it is left in the package.
OPEN_AI_FORBIDDEN_TEXT = CforbiddenText(
    patterns=(
        r"\bfree\b",
        r"\btrials?\b",
        r"\bevaluation\b",
        r"\bcredit cards?\b",
        r"\bpaid\b",
        r"\bsubscri",
        r"\bdiscounts?\b",
        r"\bpromotions?\b",
        r"\b(buy|purchase|checkout)\b",
        r"workflows-creator-plans|\bplans page\b",
        r"[$€£]\s?\d",  # prices in dollars, euros or pounds
    ),
    scope="the openai package",
    fix="reword it or add a replacement in scripts/packageVariants.py",
)

GET_STARTED = "skills/get-started/SKILL.md"
MEDIA_TASKS = "skills/media-tasks/SKILL.md"
README = "README.md"
NOTICE = "NOTICE"
MANIFEST = PORTABLE_MANIFEST.as_posix()

# The free evaluation and the plans page give way to the Mistika Workflows page.
OPEN_AI_LICENSING = (
    CtextReplacement(
        GET_STARTED,
        "step by step, from the evaluation license to the installer for your system and the connection to Claude Desktop, Claude Code or Codex (tasks in the ChatGPT desktop app and the Codex CLI).",
        "step by step, from the installer for your system to the connection to Codex (tasks in the ChatGPT desktop app and the Codex CLI) and the other AI apps on the computer.",
    ),
    CtextReplacement(
        GET_STARTED,
        "First tell the user that Mistika Workflows needs a license, and that they get it on the [Workflows Creator plans page](https://www.sgo.es/workflows-creator-plans/):\n"
        "\n"
        "- **The 30-day evaluation is free**: free for the whole evaluation period, with no credit card or payment needed to get it. It is the way to start. On the page, the user chooses **30-Day Trial**, not the paid 30-day license.\n"
        "- Subscriptions and licenses are on the same page. Do not quote prices or terms: send the user to the page.\n",
        f"First tell the user that Mistika Workflows needs a license from SGO, which they activate in Mistika Workflows, and that the {WORKFLOWS_PAGE_LINK} explains how to get one. Do not quote prices or terms: send the user to the page.\n",
    ),
    CtextReplacement(
        GET_STARTED,
        "give the user the installer link for their system and the plans page.",
        "give the user the installer link for their system and the Mistika Workflows page.",
    ),
    CtextReplacement(
        GET_STARTED,
        "activates the license they got on the [plans page](https://www.sgo.es/workflows-creator-plans/). If they do not have one yet, send them there for the free evaluation (**30-Day Trial**).",
        f"activates their license. If they do not have one yet, send them to the {WORKFLOWS_PAGE_LINK}.",
    ),
    CtextReplacement(
        GET_STARTED,
        "or gets one from the [plans page](https://www.sgo.es/workflows-creator-plans/), where the evaluation is free.",
        f"or finds how to get one on the {WORKFLOWS_PAGE_LINK}.",
    ),
    CtextReplacement(
        GET_STARTED,
        "For prices, terms and anything else, send the user to the plans page.",
        "For prices, terms and anything else, send the user to the Mistika Workflows page.",
    ),
    CtextReplacement(
        MEDIA_TASKS,
        "getting a license; the 30-day evaluation is free and needs no credit card)",
        "getting a license from SGO)",
    ),
    CtextReplacement(
        README,
        "the assistant helps you install it and get a license on the [Workflows Creator plans page](https://www.sgo.es/workflows-creator-plans/): the 30-day evaluation is free, includes every feature and needs no credit card.",
        f"the assistant helps you install it. Mistika Workflows needs a license from SGO: the {WORKFLOWS_PAGE_LINK} explains how to get one.",
    ),
    CtextReplacement(
        README,
        "helps you get a license (the evaluation is free) and the installer for your operating system",
        "gives you the installer for your operating system",
    ),
)

# No other AI assistant named where the OpenAI review reads.
OPEN_AI_ASSISTANT_NAMES = (
    CtextReplacement(
        README,
        "describe what you need, and Claude or ChatGPT builds and runs it",
        "describe what you need, and your AI assistant builds and runs it",
    ),
    CtextReplacement(
        NOTICE,
        "Mistika Workflows plugin for Claude\n",
        "Mistika Workflows plugin for ChatGPT and Codex\n",
    ),
)

# The AI dubbing, voice and enhancement services of Mistika Workflows, which
# the plugin folder leaves out for the Claude directory.
OPEN_AI_GENERATIVE_FEATURES = (
    CtextReplacement(
        MANIFEST,
        "VFX pulls, transcription, QC, deliveries",
        "VFX pulls, AI dubbing and transcription, QC, deliveries",
    ),
    CtextReplacement(
        MANIFEST,
        '    "qc",\n    "transcription",\n',
        '    "qc",\n    "dubbing",\n    "transcription",\n',
    ),
    CtextReplacement(
        MANIFEST,
        "automated QC and loudness checks, transcription, deliveries and transfers",
        "automated QC and loudness checks, AI dubbing and transcription, deliveries and transfers",
    ),
    CtextReplacement(
        MANIFEST,
        "such as transcription services, QC tools or cloud storage",
        "such as AI dubbing and transcription services, QC tools or cloud storage",
    ),
    CtextReplacement(
        MEDIA_TASKS,
        "automate VFX pulls and EDL-based conforms, transcribe speech to text, run QC",
        "automate VFX pulls and EDL-based conforms, dub, transcribe and enhance with AI, run QC",
    ),
    CtextReplacement(
        MEDIA_TASKS,
        "## No AI generation of media\n"
        "\n"
        "Do not build, change or run a workflow with a node that generates audio, speech, video or images with an AI model, such as nodes that synthesize or clone voices, replace the speech of a clip with a voice in another language, or invent image detail to enhance or upscale footage. This includes such nodes in templates and in the user's own workflows, and you do not offer them. If the user asks for one, tell them plainly that you do not build or run AI generation of audio, voice, video or images, and offer to do the rest of the task. Transcription, which turns speech into text, is fine.\n"
        "\n",
        "",
    ),
    CtextReplacement(
        MEDIA_TASKS,
        "- **Transcription**: speech to text with Amberscript.\n",
        "- **AI**: dubbing, text to speech and speech to speech with ElevenLabs, transcription with Amberscript, and enhancement and upscaling with Pixell AI.\n",
    ),
    CtextReplacement(
        MEDIA_TASKS,
        "(Amberscript, Pulsar, QScan,",
        "(ElevenLabs, Amberscript, Pixell AI, Pulsar, QScan,",
    ),
    CtextReplacement(
        README,
        "VFX pulls, transcription, quality checks,",
        "VFX pulls, AI dubbing and transcription, quality checks,",
    ),
    CtextReplacement(
        README,
        '- "Transcribe these interviews with Amberscript."\n',
        '- "Dub this promo into Spanish with ElevenLabs."\n',
    ),
    CtextReplacement(
        README,
        "  - **Quality and transcription**: automated QC with Pulsar and QScan, loudness checks and Amberscript transcription.\n",
        "  - **Quality and AI**: automated QC with Pulsar and QScan, loudness checks, ElevenLabs dubbing and voice, Amberscript transcription and Pixell AI enhancement.\n",
    ),
    CtextReplacement(
        README,
        "such as Amberscript, QC tools,",
        "such as ElevenLabs, Amberscript, Pixell AI, QC tools,",
    ),
    CtextReplacement(
        README,
        "a VFX pull, transcription, a quality check,",
        "a VFX pull, AI dubbing or transcription, a quality check,",
    ),
)

MISTIKA_WORKFLOWS_FOR_OPEN_AI = CpackageVariant(
    target="openai",
    plugin="mistika-workflows",
    manifest=MANIFEST,
    excludedPaths=(".claude-plugin",),
    replacements=OPEN_AI_LICENSING + OPEN_AI_ASSISTANT_NAMES + OPEN_AI_GENERATIVE_FEATURES,
    forbiddenText=OPEN_AI_FORBIDDEN_TEXT,
    checkPackage=checkPortablePackage,
)

VARIANTS: Tuple[CpackageVariant, ...] = (MISTIKA_WORKFLOWS_FOR_OPEN_AI,)
