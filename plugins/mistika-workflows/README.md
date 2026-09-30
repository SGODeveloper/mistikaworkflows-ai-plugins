# Mistika Workflows for Claude

**Let Claude handle your media tasks.** Transcoding, proxies, metadata, deliveries and notifications: describe what you need, and Claude builds and runs it with [Mistika Workflows](https://www.sgo.es/mistika-workflows/), SGO's media automation software, on your own computer.

## What you can ask for

- "Transcode every .mov in D:/rushes to ProRes 422 HQ and put the results in D:/masters."
- "Make H.264 proxies of today's footage and email me when they are done."
- "Upload the finished masters to our Aspera server and post a message in Slack."
- "Export the frame rate and resolution of these clips to a CSV file."
- "Run my 'Social deliveries' template on this folder."
- "Build a workflow for this delivery and save it as a template, so I can reuse it."

Claude picks the right nodes, connects them, checks that the workflow is valid, runs it and tells you what it produced. When a value is missing, such as a destination or a login, Claude asks you instead of guessing.

## Why Mistika Workflows

- **Production-quality processing.** ProRes on Windows, macOS and Linux, GPU-accelerated H.264 and H.265, OpenEXR and camera RAW, with color management and metadata preserved.
- **Your media stays on your computer.** The files are processed locally by Mistika Workflows; Claude works with the workflow, the file names and the results.
- **Nothing hidden.** Open Mistika Workflows to watch the workflows Claude builds, adjust them by hand and reuse them. Every run goes through the task queue, with its log.
- **More than transcoding.** Around 250 nodes: deliveries to Aspera, Signiant, Frame.io, Dropbox, AWS, YouTube, Vimeo and ShotGrid, email and Slack notifications, metadata and CDL handling, quality checks, AI nodes and your own Python nodes.
- **Your templates, your way.** Claude can start from the templates you already use, or save the workflows it builds as new templates.

## Get started

1. Install this plugin.
2. Ask Claude: "Set up Mistika Workflows." If you do not have it yet, Claude helps you get the [30-day free trial](https://www.sgo.es/checkout/?add-to-cart=198766) or a [subscription](https://www.sgo.es/mistika-workflows-plans/) and install it.
3. Restart Claude and ask for your first task.

Requirements: Mistika Workflows 11.7 or later. The Mistika Workflows tools work in Claude Desktop (chat and Cowork) on Windows and macOS, and in Claude Code on Windows, macOS and Linux. They are not available in Claude on the web or on mobile, because Mistika Workflows runs on your computer.

## How it works

Mistika Workflows 11.7 and later include an MCP server, `workflowsMcpServer`. The Mistika Workflows installer installs it and connects it to the AI apps it finds on the computer, Claude Desktop included. This plugin adds a setup skill that helps Claude to:

- check whether Mistika Workflows is installed and connected to Claude;
- help you install it when it is missing: the free trial or a subscription, the installer for your operating system and the steps after installing;
- connect an existing installation to Claude Desktop or Claude Code when its tools do not show up;
- troubleshoot a connection that fails.

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
