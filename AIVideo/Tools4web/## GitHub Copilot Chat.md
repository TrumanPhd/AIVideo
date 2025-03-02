## GitHub Copilot Chat

- Extension Version: 0.22.4 (prod)
- VS Code: vscode/1.95.3
- OS: Mac

## Network

User Settings:
```json
  "github.copilot.advanced": {
    "debug.useElectronFetcher": true,
    "debug.useNodeFetcher": false
  }
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 4.237.22.34 (11 ms)
- DNS ipv6 Lookup: ::ffff:4.237.22.34 (42 ms)
- Electron Fetcher (configured): HTTP 200 (355 ms)
- Node Fetcher: HTTP 200 (90 ms)
- Helix Fetcher: HTTP 200 (376 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.112.21 (47 ms)
- DNS ipv6 Lookup: ::ffff:140.82.112.21 (63 ms)
- Electron Fetcher (configured): HTTP 200 (829 ms)
- Node Fetcher: HTTP 200 (787 ms)
- Helix Fetcher: HTTP 200 (855 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).