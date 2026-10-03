# SGO plugins for Claude

Put SGO tools to work for you, straight from a conversation with Claude. Start with Mistika Workflows: describe the media task you need, such as a transcode, proxies, a metadata report or a delivery, and Claude builds and runs it on your own computer.

## Plugins

| Plugin | What it does |
| --- | --- |
| [`mistika-workflows`](plugins/mistika-workflows) | Let Claude handle your media tasks: transcodes and proxies, color, metadata, VFX pulls, AI dubbing and transcription, QC, deliveries and watch folders, built and run with Mistika Workflows on your own computer. |

## Install

In Claude (web, desktop or Cowork), open **Customize > Plugins**, add this marketplace (`SGODeveloper/claude-plugins`) and install the plugin you need.

In Claude Code:

```
/plugin marketplace add SGODeveloper/claude-plugins
/plugin install mistika-workflows@sgo
```

## Repository layout

- `.claude-plugin/marketplace.json`: the marketplace catalog (`sgo`).
- `plugins/<plugin>/`: one folder per plugin, each with its own `.claude-plugin/plugin.json`, README and skills.

## Privacy

The plugins in this marketplace collect no data. SGO products and websites are covered by the [SGO privacy policy](https://www.sgo.es/privacy-policy-statement/).

## License

The contents of this repository are released under the [Apache License 2.0](LICENSE); see also [NOTICE](NOTICE). The license does not cover SGO products, which have their own license agreements, or the SGO and Mistika names and logos.
