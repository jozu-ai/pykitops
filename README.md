# PyKitOps

PyKitOps is an open source Python SDK for managing [KitOps](https://kitops.org) ModelKits. KitOps is a packaging, versioning, and sharing system for AI/ML projects that uses open standards so it works with the AI/ML, development, and DevOps tools you are already using, and can be stored in your enterprise container registry. 

PyKitOps makes it easy to create a KitOps ModelKit for your AI/ML project directly in code. This makes PyKitOps preferred when assembling a ModelKit from:

* A Jupyter Notebook or other code editor
* An experimentation tracking tool like MLflow

ModelKits typically include everything someone needs to reproduce an AI/ML project locally or deploy it into production. You can even selectively unpack a ModelKit so different team members can save time and storage space by only grabbing what they need for a task. Because ModelKits are immutable, signable, and live in your existing container registry they're easy for organizations to track, control, and audit.

## Installation:

```bash
pip install kitops
```

## Documentation:
[Python KitOps Docs](https://jozu-ai.github.io/pykitops/)

## Contribute and Star the Project
[pykitops on GitHub](https://github.com/jozu-ai/pykitops)
