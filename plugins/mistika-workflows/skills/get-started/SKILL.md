---
name: get-started
description: Install Mistika Workflows and connect it to Claude step by step, from the free evaluation license to the installer for your system and the connection to Claude Desktop or Claude Code. Use it when someone wants to install, update or license Mistika Workflows, agreed to set it up for a media task, has it installed but its tools are not available, or when its connection to Claude fails.
---

# Get started with Mistika Workflows

Mistika Workflows is SGO's node-based media automation application, for Windows, macOS and Linux. Version 11.7 and later include an MCP server, `workflowsMcpServer` (server name `workflowsMcp`), that gives Claude tools whose names start with `workflows_`: with them Claude builds, configures and runs workflows and templates in the user's own installation. The Mistika Workflows installer installs that server and registers it in the AI apps it finds on the computer, Claude Desktop included (the "AI Agents" components of the installer).

This skill takes the user from "no Mistika Workflows tools" to "tools available". What Mistika Workflows can do, and how to go about a media task, is in the `media-tasks` skill of this plugin. Using the tools is covered by the server's own instructions and `workflows_getting_started`.

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

Do this only when the user wants it. First tell the user that Mistika Workflows needs a license, and that they get it on the [Workflows Creator plans page](https://www.sgo.es/workflows-creator-plans/):

- **The 30-day evaluation is free**: free for the whole evaluation period, with no credit card or payment needed to get it. It is the way to start. On the page, the user chooses **30-Day Trial**, not the paid 30-day license.
- Subscriptions and licenses are on the same page. Do not quote prices or terms: send the user to the page.

The installer always gets the latest version:

| System | Installer |
| --- | --- |
| Windows | https://cdn1.www.sgo.es/sgo/installers/releases/latest-win-workflows.exe |
| macOS | https://cdn1.www.sgo.es/sgo/installers/releases/latest-osx-workflows.dmg |
| Linux | https://cdn1.www.sgo.es/sgo/installers/releases/latest-linux-workflows.run |

Use only these addresses: do not look for installers anywhere else.

How to proceed depends on where you run:

- **Claude Code**, with the user's confirmation:
  1. Download the installer for the user's system into their Downloads folder: `Invoke-WebRequest -Uri <url> -OutFile "$env:USERPROFILE\Downloads\<file>"` on Windows, `curl -fL -o ~/Downloads/<file> <url>` on macOS and Linux.
  2. Check it before opening it:
     - Windows: `Get-AuthenticodeSignature <file>` must report `Valid`, with a signer certificate for `SOLUCIONES GRAFICAS POR ORDENADOR SL`.
     - macOS: mount it with `hdiutil attach -nobrowse -readonly <file>`, then `spctl --assess --type execute -vv "<installer>.app"` on the installer app inside the mounted volume must report `accepted`, `source=Notarized Developer ID` and `SOLUCIONES GRAFICAS POR ORDENADOR SL`.
     - Linux: the `.run` installer is not signed; it is trusted because it comes from the address above over HTTPS. Make it executable with `chmod +x <file>`.

     If a check fails, delete the file and tell the user not to run it.
  3. Open the installer: `Start-Process <file>` on Windows, `open "<installer>.app"` on macOS, and on Linux ask the user to run `<file>` in their terminal (it may need `sudo` to install in `/opt`). The user completes it: accepts the license agreement, grants administrator rights and keeps the "AI Agents" components selected, which connect Mistika Workflows to Claude. Never run the installer silently or in unattended mode.
- **Claude Desktop chat or Cowork**: give the user the installer link for their system and the plans page. If you can open web pages in the user's browser, offer to open them.

After the installation:

1. **In Claude Code, register the server now.** The installer registers Mistika Workflows in Claude Desktop and the other AI apps that were installed at that moment, but not in Claude Code. Run the Claude Code command of step 4 before the user restarts anything.
2. The user starts Mistika Workflows once and activates the license they got on the [plans page](https://www.sgo.es/workflows-creator-plans/). If they do not have one yet, send them there for the free evaluation (**30-Day Trial**).
3. The user quits Claude Desktop completely and opens it again (closing the window is not enough), or starts a new Claude Code session, so Claude loads the MCP server.
4. Check for the `workflows_` tools again (step 1). If they are still missing, go to step 5. If they are available, the setup is done: tell the user to ask for their task (in Claude Code, in the new session). Do not plan the task during the setup.

## 4. Connect an existing installation

`<server>` is the full path of the MCP server executable found in step 2.

- **Claude Desktop (chat and Cowork)**: run `"<server>" --register-client claude`. It adds the `workflowsMcp` entry to Claude Desktop's configuration, keeps the rest of the configuration, and prints one line of JSON with the result. Then the user quits Claude Desktop completely and opens it again. `"<server>" --list-clients` lists the other AI apps the same command can register.
- **Claude Code**: run `claude mcp add workflowsMcp --scope user -e WORKFLOWS_MCP_TRANSPORT=stdio -- "<server>"`, check it with `claude mcp list` and start a new session. Keep `WORKFLOWS_MCP_TRANSPORT=stdio`: without it the server starts in HTTP mode and Claude Code cannot talk to it. In PowerShell, write the separator as `"--"`, with the quotes, so PowerShell passes it on to `claude`.

Where you cannot run commands, give the user the exact command for their system and tell them to run it in a terminal (Command Prompt or PowerShell on Windows, Terminal on macOS).

## 5. When the server does not connect

Find the cause before you name it. Check what you can (step 2, the Claude Code server list, the log); where you cannot check, tell the user the likely causes and the step that fixes each, instead of stating one as fact.

- **Mistika Workflows is installed but the tools do not appear after restarting.** Likely causes, in order:
  - Claude was not completely quit: on Windows, closing the window leaves it running next to the clock; on macOS, closing the window does not quit it either. The user quits it from there and opens it again.
  - The server was never registered in this Claude app: Claude was installed after Mistika Workflows, the installer did not find it, or this is Claude Code. Register it (step 4).
  - The MCP server executable is missing because the "AI Agents" or MCP components were deselected: run the installer again with them selected.
  - The installed version is older than 11.7: update it (step 3).
- **Claude Desktop shows `workflowsMcp` as failed** (Settings > Developer): read its log, `mcp-server-workflowsMcp.log`, where you can, or ask the user for it. On Windows it is in `%LOCALAPPDATA%\Packages\Claude_*\LocalCache\Roaming\Claude\logs\` for the current Claude Desktop, or in `%APPDATA%\Claude\logs\` for older installations: use the folder whose files changed most recently. On macOS it is in `~/Library/Logs/Claude/`.
- **The tools are there but every call fails with a connection error**: Mistika Workflows is not running. Follow the server's instructions: `workflows_launch_application`, then `workflows_wait_for_application_ready`.
- **Mistika Workflows reports a license problem**: the user activates or renews the license in Mistika Workflows, or gets one from the [plans page](https://www.sgo.es/workflows-creator-plans/), where the evaluation is free.

## Rules

- Stay on the setup: install, license and connect Mistika Workflows, and give product facts from the `media-tasks` skill when the user asks. Do not plan how the user's task will be done or promise features (schedules, automations, specific nodes or presets) until the tools are connected and show what is possible.
- Say about licenses only what this skill says. For prices, terms and anything else, send the user to the plans page.
- Download Mistika Workflows only from sgo.es.
- Install, update or change any configuration only when the user asks for it or agrees. Tell the user what each command does before you run it.
- Never ask for license keys, passwords or payment details in the conversation: the user enters them in Mistika Workflows or on sgo.es.
