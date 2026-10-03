# Mistika Workflows for Claude

**Let Claude handle your media tasks.** Transcodes and proxies, color pipelines, metadata reports, VFX pulls, AI dubbing and transcription, quality checks, deliveries and watch folders: describe what you need, and Claude builds and runs it with [Mistika Workflows](https://www.sgo.es/mistika-workflows/), SGO's media automation software, on your own computer.

## What you can ask for

- "Transcode every .mov in D:/rushes to ProRes 422 HQ and put the results in D:/masters."
- "Make H.264 proxies of today's footage, upload them to Frame.io and email me when they are done."
- "Watch this folder and convert everything that lands in it to DNxHR LB for the editors."
- "Apply the CDLs from this EDL and render EXR plates in ACES for the VFX team."
- "Copy only the clips used in this EDL to the backup drive and create MD5 checksums."
- "Make an SDR version of this Dolby Vision HDR master."
- "Run an automated QC on these masters, send them to our Aspera server and post a message in Slack."
- "Dub this promo into Spanish with ElevenLabs."
- "Export the frame rate and resolution of these clips to a CSV file."
- "Build a workflow for this delivery and save it as a template, so I can reuse it."

Claude picks the right nodes, connects them, checks that the workflow is valid, runs it and tells you what it produced. When a value is missing, such as a destination or a login, Claude asks you instead of guessing.

## Why Mistika Workflows

- **Production-quality processing.** ProRes on Windows, macOS and Linux, DNxHD and DNxHR, XAVC, XDCAM, GPU-accelerated H.264 and H.265, OpenEXR and DPX, from camera RAW too (ARRI, RED, Sony, Canon, Blackmagic RAW, ProRes RAW), with color management and metadata preserved.
- **Your media stays on your computer.** The files are processed locally by Mistika Workflows; Claude works with the workflow, the file names and the results.
- **Nothing hidden.** Open Mistika Workflows to watch the workflows Claude builds, adjust them by hand and reuse them. Every run goes through the task queue, with its log.
- **More than transcoding.** More than 200 nodes:
  - **Color**: ACES (2.0 included), CDLs, 3D LUTs, CLF and Dolby Vision tone mapping.
  - **Editorial and VFX**: EDL-driven conforms and VFX pulls, reference movies, OpenTimelineIO timelines and ShotGrid publishing.
  - **Deliveries**: Aspera, Signiant, MASV, Filemail, FTP and SFTP, AWS S3, Azure, Google Drive, OneDrive, Dropbox, Frame.io, PIX, MediaSilo, YouTube and Vimeo, plus AS-11 masters and CableLabs ADI packages.
  - **Notifications**: email, Slack, Microsoft Teams, Discord and WhatsApp.
  - **Quality and AI**: automated QC with Pulsar and QScan, loudness checks, ElevenLabs dubbing and voice, Amberscript transcription and Pixell AI enhancement.
  - **Metadata and files**: reports to CSV and ALE, renaming with metadata tokens, sorting, checksums and MHL, burn-ins and slates.
  - **Integrations**: DaVinci Resolve, After Effects, Mistika Boutique, Ultima and VR, EditReady and the ARRI Reference Tool, plus your own Python nodes and command-line tools.
- **Hands-off automation.** While Mistika Workflows is running, watch folders start a workflow as soon as files arrive, with notifications when it finishes or fails.
- **Your templates, your way.** Claude can start from the templates you already use, or save the workflows it builds as new templates that your team can also launch from the Workflows Runner.

Services and applications from other companies, such as ElevenLabs, Amberscript, Pixell AI, QC tools, cloud storage, After Effects or DaVinci Resolve, need your own account or installation.

## Get started

1. Install this plugin.
2. Ask Claude: "Set up Mistika Workflows." If you do not have it yet, Claude helps you install it and get a license on the [Workflows Creator plans page](https://www.sgo.es/workflows-creator-plans/): the 30-day evaluation is free, includes every feature and needs no credit card.
3. Restart Claude and ask for your first task.

Requirements: Mistika Workflows 11.7 or later. The Mistika Workflows tools work in Claude Desktop (chat and Cowork) on Windows and macOS, and in Claude Code on Windows, macOS and Linux. They are not available in Claude on the web or on mobile, because Mistika Workflows runs on your computer.

## How it works

Mistika Workflows 11.7 and later include an MCP server, `workflowsMcpServer`. The Mistika Workflows installer installs it and connects it to the AI apps it finds on the computer, Claude Desktop included. This plugin adds two skills:

- **`media-tasks`**: when you ask for a media task, such as a transcode, proxies, a metadata report, a color pipeline, a VFX pull, AI dubbing or transcription, a quality check, a delivery or a watch folder, Claude does it with Mistika Workflows. If Mistika Workflows is not connected yet, Claude tells you what it takes and sets it up with you. It also answers what Mistika Workflows can do.
- **`get-started`**: installs and connects Mistika Workflows step by step. Claude checks whether it is installed and connected, helps you get a license (the evaluation is free) and the installer for your operating system, connects an existing installation to Claude Desktop or Claude Code, and troubleshoots a connection that fails.

## What this plugin runs, sends and fetches

The plugin contains instructions only (two skills). It runs no code when it is installed and it sends no data anywhere.

When you ask Claude to install or connect Mistika Workflows, Claude may, with your confirmation and only where it can run commands on your computer (Claude Code):

- download the latest Mistika Workflows installer for your system from SGO's download server (`cdn1.www.sgo.es`), check its signature and open it, so you complete the installation yourself;
- read the SGO installation file (`installation.xml`) to find where Mistika Workflows is installed and which version it is;
- run `workflowsMcpServer --register-client claude` or `claude mcp add` to connect the installed MCP server to Claude.

Everywhere else Claude gives you the links and the steps instead.

## Privacy

This plugin collects no data. Mistika Workflows and the sgo.es website are covered by the [SGO privacy policy](https://www.sgo.es/privacy-policy-statement/).

## Support

Visit [SGO support](https://support.sgo.es) or the [Mistika Workflows page](https://www.sgo.es/mistika-workflows/).

## License

This plugin is released under the [Apache License 2.0](LICENSE); see also [NOTICE](NOTICE). The license covers the contents of this plugin only. It does not cover Mistika Workflows, which has its own license agreement, or the SGO and Mistika names and logos.
