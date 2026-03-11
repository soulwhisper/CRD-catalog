# CRD Catalog

A personal archive of Kubernetes Custom Resource Definitions (CRDs) extracted from my home cluster.

## Usage

Schemas are served at `https://soulwhisper.github.io/CRD-catalog/` and can be used with tools like [kubeconform](https://github.com/yannh/kubeconform):

```yaml
# .kubeconform.yaml
schema-location:
  - default
  - "https://soulwhisper.github.io/CRD-catalog/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json"
```

## Schema location

Schemas follow the same structure as [datreeio/CRDs-catalog](https://github.com/datreeio/CRDs-catalog):

```
{api-group}/{kind}_{version}.json
# e.g. cert-manager.io/certificate_v1.json
```
