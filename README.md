# SGO plugins for AI assistants

Put SGO tools to work for you, straight from a conversation with Claude or ChatGPT. Start with Mistika Workflows: describe the media task you need, such as a transcode, proxies, a metadata report or a delivery, and your assistant builds and runs it on your own computer.

## Plugins

| Plugin | What it does |
| --- | --- |
| [`mistika-workflows`](plugins/mistika-workflows) | Let your AI assistant handle your media tasks: transcodes and proxies, color, metadata, VFX pulls, AI dubbing and transcription, QC, deliveries and watch folders, built and run with Mistika Workflows on your own computer. |

## Install

### Claude

In Claude (web, desktop or Cowork), open **Customize > Plugins**, add this marketplace (`SGODeveloper/mistikaworkflows-ai-plugins`) and install the plugin you need.

In Claude Code:

```
/plugin marketplace add SGODeveloper/mistikaworkflows-ai-plugins
/plugin install mistika-workflows@sgo
```

### ChatGPT and Codex

Add this marketplace with the Codex CLI, which shares its configuration with the ChatGPT desktop app:

```
codex plugin marketplace add SGODeveloper/mistikaworkflows-ai-plugins
codex plugin add mistika-workflows@sgo
```

Or, after adding the marketplace, restart the ChatGPT desktop app and install the plugin from **Plugins**.

## Repository layout

- `.claude-plugin/marketplace.json`: the marketplace catalog (`sgo`), read by Claude, Codex and the ChatGPT desktop app.
- `plugins/<plugin>/`: one folder per plugin, with:
  - `.claude-plugin/plugin.json`: the manifest for Claude;
  - `plugin.json`: the portable [Agent Plugins](https://agent-plugins.org) manifest for ChatGPT and Codex, with the ChatGPT listing under `extensions.com.openai`;
  - `skills/`: the skills, shared by every app;
  - `assets/`, `README.md`, `LICENSE` and `NOTICE`.
- `scripts/checkManifests.py` (with `scripts/checkReport.py`): the release check.

## Releasing a new version

1. Change the plugin and raise its `version` in both manifests, `.claude-plugin/plugin.json` and `plugin.json`.
2. Run `python3 scripts/checkManifests.py`. It checks that both manifests agree on the package identity, that the ChatGPT listing fits the directory limits, that every referenced file exists and that every skill has a valid header.
3. Commit and push to `main`.

## Privacy

The plugins in this marketplace collect no data. SGO products and websites are covered by the [SGO privacy policy](https://www.sgo.es/privacy-policy-statement/).

## License

The contents of this repository are released under the [Apache License 2.0](LICENSE); see also [NOTICE](NOTICE). The license does not cover SGO products, which have their own license agreements, or the SGO and Mistika names and logos.
