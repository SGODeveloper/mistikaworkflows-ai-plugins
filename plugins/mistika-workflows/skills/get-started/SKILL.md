---
name: get-started
description: Get Mistika Workflows working with Claude, so Claude can transcode, make proxies, manage metadata, apply color pipelines, dub and transcribe with AI, check quality and deliver media for the user, on their own computer. Use when the user asks what Mistika Workflows can do, wants to use it but its tools (names starting with workflows_) are not available, asks how to get, install, update or license it, or when its connection to Claude fails.
---

# Get started with Mistika Workflows

Mistika Workflows is SGO's node-based media automation application, for Windows, macOS and Linux. Version 11.7 and later include an MCP server, `workflowsMcpServer` (server name `workflowsMcp`), that gives Claude tools whose names start with `workflows_`: with them Claude builds, configures and runs workflows and templates in the user's own installation. The Mistika Workflows installer installs that server and registers it in the AI apps it finds on the computer, Claude Desktop included (the "AI Agents" components of the installer).

This skill answers what Mistika Workflows can do, and takes the user from "no Mistika Workflows tools" to "tools available". It does not cover using the tools: once they are available, the server's own instructions and `workflows_getting_started` do.

## What Mistika Workflows can do

Use this list to answer "what can Mistika Workflows do?" and to show users what they get before they install it. It comes from the nodes and templates that ship with Mistika Workflows:

- **Transcoding and proxies**: ProRes on Windows, macOS and Linux, DNxHD and DNxHR (OP-Atom included), XAVC, XDCAM, GPU-accelerated H.264 and H.265, OpenEXR in ACES AP0, camera RAW sources, Dolby Vision to SDR, plus resolution changes, trims and watermarks.
- **Deliveries and transfers**: Aspera, Signiant Media Shuttle, MASV, FileMail, FTP, AWS S3, Azure, Google Drive, OneDrive, Dropbox, Object Matrix, Frame.io, PIX, MediaSilo, YouTube and Vimeo, and AS-11 and DCP deliverables.
- **Notifications**: email (Gmail included), Slack, Microsoft Teams, Discord and WhatsApp.
- **Metadata and file management**: metadata reports to CSV, ALE and Excel; files sorted by metadata, extension, size, age or aspect ratio; checksums; copies, moves and renames with naming conventions built from metadata tokens.
- **Color**: ACES workflows, CDLs, 3D LUTs and color space transformations.
- **VFX pulls**: EDLs to markers and CC files, EXR plates, reference movies and ShotGrid publishing.
- **Quality control and audio**: automated QC with Pulsar and Qscan, and loudness measurement with Youlean.
- **AI**: dubbing, text to speech and speech to speech with ElevenLabs, transcription with Amberscript, and image enhancement with Pixell AI.
- **Your own logic**: Python nodes and reusable templates, which the team can also launch from the Workflows Runner.

Be accurate when you describe it:

- The services of other companies (ElevenLabs, Amberscript, Pixell AI, Pulsar, Qscan and the cloud storage and delivery services) need the user's own account with them.
- Everything runs in the user's installation, on their computer: the media is processed locally.
- Once the tools are available, check the exact nodes with `workflows_node_catalog` and the templates with `workflows_v2_listTemplates` before promising a specific one.

## 1. Check the connection first

If tools whose names start with `workflows_` are available, Mistika Workflows is already connected. Set nothing up: call `workflows_getting_started` and continue with the user's request.

The tools run on the user's computer, so they are only available in Claude Desktop (chat and Cowork) and in Claude Code. In Claude on the web or on mobile, tell the user to use one of those on the computer where Mistika Workflows is installed.

Otherwise, find out why the tools are missing (step 2).

## 2. Find the installation

Where you can run commands on the user's computer (Claude Code), check it yourself. Everywhere else, ask the user whether Mistika Workflows 11.7 or later is installed, and on which operating system.

SGO installers record the installed products in `installation.xml`:

| System | Installation file |
| --- | --- |
| Windows | `C:\ProgramData\SGO\installation.xml` |
| macOS | `installation.xml` in the SGO Apps folder, by default `/Applications/SGO Apps/installation.xml` |
| Linux | `installation.xml` in the SGO Apps folder, by default `/opt/SGO Apps/installation.xml` or `~/SGO Apps/installation.xml` |

In that file:

- `/installation/paths/app` is the SGO Apps folder.
- The `version` attribute of `/installation/sw/workflows` is the installed Mistika Workflows version. It is empty when Mistika Workflows is not installed.

The MCP server executable is in the SGO Apps folder:

| System | MCP server executable |
| --- | --- |
| Windows | `Mistika Workflows/bin/workflowsMcpServer.exe` |
| macOS | `Mistika Workflows.app/Contents/MacOS/workflowsMcpServer` |
| Linux | `Mistika Workflows/bin/workflowsMcpServer` |

Always check that the executable exists: older installers left the version in the file after uninstalling, and the MCP component can be deselected during the installation.

Then:

- No installation file, an empty version or no executable: Mistika Workflows is not installed. Go to step 3.
- A version older than 11.7: that version has no MCP server. Offer to update it (step 3).
- The executable exists: Mistika Workflows is installed but not connected to this Claude app. Go to step 4.

## 3. Install or update Mistika Workflows

Do this only when the user wants it. First tell the user:

- Mistika Workflows needs a license: the [30-day free trial](https://www.sgo.es/checkout/?add-to-cart=198766) or a [subscription or license](https://www.sgo.es/mistika-workflows-plans/).
- The installer for their operating system is on the [Mistika Workflows page](https://www.sgo.es/mistika-workflows/).

<!-- TODO(sgo): when the stable "latest installer" URL of each operating system is published, list it here (Windows, macOS, Linux) and use it in the download step below. -->

How to proceed depends on where you run:

- **Claude Code**, with the user's confirmation:
  1. Download the installer for the user's operating system from sgo.es.
  2. Check its signature before opening it. On Windows, `Get-AuthenticodeSignature <file>` must report `Valid`, signed by `SOLUCIONES GRAFICAS POR ORDENADOR SL`. On macOS, `spctl --assess --type open --context context:primary-signature -v <file>.dmg` must report `accepted` and `Notarized Developer ID`. If the check fails, delete the file and tell the user.
  3. Open the installer (`Start-Process <file>` on Windows, `open <file>.dmg` on macOS). The user completes it: accepts the license agreement, grants administrator rights and keeps the "AI Agents" components selected, which connect Mistika Workflows to Claude. Never run the installer silently or in unattended mode.
- **Claude Desktop chat or Cowork**: give the user the links above. If you can open web pages in the user's browser, offer to open the page for them.

After the installation:

1. The user starts Mistika Workflows once to activate the license (trial or purchase).
2. The user quits Claude Desktop completely and opens it again (closing the window is not enough), or starts a new Claude Code session, so Claude loads the MCP server.
3. Check for the `workflows_` tools again (step 1). If they are still missing, go to step 4: for example, Claude may have been installed after Mistika Workflows, so the installer did not find it.

## 4. Connect an existing installation

`<server>` is the full path of the MCP server executable found in step 2.

- **Claude Desktop (chat and Cowork)**: run `"<server>" --register-client claude`. It adds the `workflowsMcp` entry to Claude Desktop's configuration, keeps the rest of the configuration, and prints one line of JSON with the result. Then the user quits Claude Desktop completely and opens it again. `"<server>" --list-clients` lists the other AI apps the same command can register.
- **Claude Code**: run `claude mcp add workflowsMcp --scope user -e WORKFLOWS_MCP_TRANSPORT=stdio -- "<server>"`, check it with `claude mcp list` and start a new session. Keep `WORKFLOWS_MCP_TRANSPORT=stdio`: without it the server starts in HTTP mode and Claude Code cannot talk to it.

Where you cannot run commands, give the user the exact command for their system and tell them to run it in a terminal (Command Prompt or PowerShell on Windows, Terminal on macOS).

## 5. When the server does not connect

- **Claude Desktop shows `workflowsMcp` as failed**: its log is `mcp-server-workflowsMcp.log`, in `%APPDATA%\Claude\logs\` on Windows and in `~/Library/Logs/Claude/` on macOS. Read it where you can, or ask the user for it.
- **The tools are there but every call fails with a connection error**: Mistika Workflows is not running. Follow the server's instructions: `workflows_launch_application`, then `workflows_wait_for_application_ready`.
- **Mistika Workflows reports a license problem**: the user activates or renews the license in Mistika Workflows, or gets one from the [plans page](https://www.sgo.es/mistika-workflows-plans/).

## Rules

- Download Mistika Workflows only from sgo.es.
- Install, update or change any configuration only when the user asks for it or agrees. Tell the user what each command does before you run it.
- Never ask for license keys, passwords or payment details in the conversation: the user enters them in Mistika Workflows or on sgo.es.
