# SGO plugins for AI assistants

Put SGO tools to work for you, straight from a conversation with Claude or ChatGPT. Start with Mistika Workflows: describe the media task you need, such as a transcode, proxies, a metadata report or a delivery, and your assistant builds and runs it on your own computer.

## Plugins

| Plugin | What it does |
| --- | --- |
| [`mistika-workflows`](plugins/mistika-workflows) | Let your AI assistant handle your media tasks: transcodes and proxies, color, metadata, VFX pulls, transcription, QC, deliveries and watch folders, built and run with Mistika Workflows on your own computer. |

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

Then quit the ChatGPT desktop app completely and open it again: it reads new marketplaces and plugins only when it starts, so until then the plugin is missing from **Plugins** and from the `@` menu. In the Codex CLI, start a new session.

Or, after adding the marketplace, restart the ChatGPT desktop app and install the plugin from **Plugins**.

The Mistika Workflows tools work in Codex tasks of the ChatGPT desktop app and in the Codex CLI. ChatGPT conversations (Chat and Work) run in the cloud and cannot use them.

## Repository layout

- `.claude-plugin/marketplace.json`: the marketplace catalog (`sgo`), read by Claude, Codex and the ChatGPT desktop app.
- `plugins/<plugin>/`: one folder per plugin, with:
  - `.claude-plugin/plugin.json`: the manifest for Claude;
  - `plugin.json`: the portable [Agent Plugins](https://agent-plugins.org) manifest for ChatGPT and Codex, with the ChatGPT listing under `extensions.com.openai`;
  - `skills/`: the skills, shared by every app;
  - `assets/`, `README.md`, `LICENSE` and `NOTICE`.
- `PRIVACY.md`: the privacy policy of the plugins, linked from the ChatGPT listing.
- `scripts/checkManifests.py` (with `scripts/checkReport.py`): the release check.
- `scripts/buildPackages.py` (with `packageVariants.py`, `packageVariant.py`, `textReplacement.py` and `forbiddenText.py` in `scripts/`): builds the package for the OpenAI plugin directory in `dist/`, which git ignores.

## Releasing a new version

1. Change the plugin and raise its `version` in both manifests, `.claude-plugin/plugin.json` and `plugin.json`.
2. Run `python3 scripts/checkManifests.py`. It checks that both manifests agree on the package identity, that the Claude listing fields (icon, links) and the ChatGPT listing fit their directories (including that the ChatGPT listing names no other AI assistant or AI service), that every referenced file exists, that every skill has a valid header, and that nothing the Claude directory reads (the plugin folders, the marketplace and this README) offers AI generation of audio, video or images, which the Claude directory does not list.
3. Commit and push to `main`.
4. For the OpenAI plugin directory, run `python3 scripts/buildPackages.py openai` and upload `dist/openai/<plugin>-<version>.zip` at [platform.openai.com/plugins](https://platform.openai.com/plugins) as a new version of the plugin.

### The package for the OpenAI plugin directory

The Claude directory and this marketplace use the plugin folder as it is. The OpenAI plugin directory gets a package built from it, because its guidelines differ: `scripts/packageVariants.py` replaces the passages about the free evaluation and the plans page with neutral text that points to the Mistika Workflows page, because its guidelines do not allow advertising free trials or linking to plans or checkout pages; removes the names of other AI assistants from the skill descriptions and the introduction of the README, which its review flags; adapts the features of Mistika Workflows that the plugin describes to the ones that directory lists; and leaves `.claude-plugin/` out. The build checks the package with the same rules as `checkManifests.py` and fails when one of those passages changes in the plugin, or when text that the OpenAI guidelines do not allow is left in the package; update `scripts/packageVariants.py` then.

## Privacy

The plugins in this marketplace collect no data: see their [privacy policy](PRIVACY.md). SGO products and websites are covered by the [SGO privacy policy](https://www.sgo.es/privacy-policy-statement/).

## License

The contents of this repository are released under the [Apache License 2.0](LICENSE); see also [NOTICE](NOTICE). The license does not cover SGO products, which have their own license agreements, or the SGO and Mistika names and logos.
