# SGO plugins for Claude

The SGO plugin marketplace for Claude: Mistika Workflows and other SGO tools, with skills that help you install, set up and use them from Claude.

## Plugins

| Plugin | What it does |
| --- | --- |
| [`mistika-workflows`](plugins/mistika-workflows) | Install Mistika Workflows and connect it to Claude, so Claude can build and run your media workflows. |

## Install

In Claude (web, desktop or Cowork), open **Customize > Plugins**, add this marketplace (`madcodingrocks/claude-plugins`) and install the plugin you need.

In Claude Code:

```
/plugin marketplace add madcodingrocks/claude-plugins
/plugin install mistika-workflows@sgo
```

## Repository layout

- `.claude-plugin/marketplace.json`: the marketplace catalog (`sgo`).
- `plugins/<plugin>/`: one folder per plugin, each with its own `.claude-plugin/plugin.json`, README and skills.

## Privacy

The plugins in this marketplace collect no data. SGO products and websites are covered by the [SGO privacy policy](https://www.sgo.es/privacy-policy-statement/).
