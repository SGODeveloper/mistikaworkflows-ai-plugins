# Mistika Workflows for Claude

[Mistika Workflows](https://www.sgo.es/mistika-workflows/) is SGO's node-based automation tool for media: transcoding and encoding, clip metadata, file operations, deliveries and transfers, notifications, QC and AI nodes. It runs on Windows, macOS and Linux.

Mistika Workflows 11.7 and later include an MCP server, `workflowsMcpServer`. The Mistika Workflows installer installs it and connects it to the AI apps it finds on the computer, Claude Desktop included. Through it, Claude can build, configure and run workflows and templates in your own Mistika Workflows installation.

This plugin gets you there. Its skill helps Claude to:

- check whether Mistika Workflows is installed and connected to Claude;
- help you install it when it is missing: the 30-day free trial or a subscription, the installer for your operating system and the steps after installing;
- connect an existing installation to Claude Desktop or Claude Code when its tools do not show up;
- troubleshoot a connection that fails.

## Requirements

- Mistika Workflows 11.7 or later, with an evaluation or a purchased license.
- The Mistika Workflows tools are available in Claude Desktop (chat and Cowork) and in Claude Code. They are not available in Claude on the web or on mobile, because the MCP server runs on your computer.

## What this plugin runs, sends and fetches

The plugin contains instructions only (one skill). It runs no code when it is installed and it sends no data anywhere.

When you ask Claude to install or connect Mistika Workflows, Claude may, with your confirmation and only where it can run commands on your computer (Claude Code):

- download the Mistika Workflows installer from sgo.es and open it, so you complete the installation yourself;
- read the SGO installation file (`installation.xml`) to find where Mistika Workflows is installed and which version it is;
- run `workflowsMcpServer --register-client claude` or `claude mcp add` to connect the installed MCP server to Claude.

Everywhere else Claude gives you the links and the steps instead.

## Privacy

This plugin collects no data. Mistika Workflows and the sgo.es website are covered by the [SGO privacy policy](https://www.sgo.es/privacy-policy-statement/).

## Support

Visit [SGO support](https://support.sgo.es) or the [Mistika Workflows page](https://www.sgo.es/mistika-workflows/).

## License

This plugin is released under the [Apache License 2.0](LICENSE); see also [NOTICE](NOTICE). The license covers the contents of this plugin only. It does not cover Mistika Workflows, which has its own license agreement, or the SGO and Mistika names and logos.
