# JEV Project Registry

The Project Registry is the canonical source for project-level configuration.

Each project records:

- project identity and display name
- one or more GitHub repositories
- one explicitly designated primary repository
- repository role: frontend, backend, infra or other
- repository-specific production/staging branches
- repository-specific production/staging URLs
- repository-specific staging database capability and environment metadata
- monthly AI budget
- allowed models and default model
- project status and tags

The legacy project-level repository/branch/URL fields remain as compatibility aliases for the primary repository. They must match the primary repository mapping.

A multi-repository work order must resolve its target repository explicitly. JEV must not guess which repository should be modified.

Active primary projects require a permanent staging environment and a separate staging database.

The registry is deliberately separated from the UI. The future dashboard reads and updates projects through this layer rather than storing configuration in frontend code.
