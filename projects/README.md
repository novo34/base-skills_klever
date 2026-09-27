# JEV Project Registry

The Project Registry is the canonical source for project-level configuration.

Each project records:

- project identity and display name
- GitHub repository
- production branch
- permanent staging branch
- production URL
- staging URL
- staging database availability
- monthly AI budget
- allowed models and default model
- project status and tags

Active projects require a permanent staging environment and a separate staging database.

The registry is deliberately separated from the UI. The future dashboard reads and updates projects through this layer rather than storing configuration in frontend code.
