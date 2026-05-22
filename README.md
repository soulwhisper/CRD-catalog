# k8s-schemas

A personal archive of Kubernetes Custom Resource Definitions (CRDs) extracted from upstream.

## Usage

Schemas are served at `https://soulwhisper.github.io/k8s-schemas/` and can be used with tools like [kubeconform](https://github.com/yannh/kubeconform):

```yaml
# .kubeconform.yaml
schema-location:
  - default
  - "https://soulwhisper.github.io/k8s-schemas/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json"
```

## Gratitude and Thanks

I got help from some cool repo like:

- [datreeio/CRDs-catalog](https://github.com/datreeio/CRDs-catalog)
- [bjw-s/home-ops](https://github.com/bjw-s-labs/home-ops/tree/8cc0a68f5d86c7dece9f91d4e83ac2903075e0ad/kubernetes/apps/jobs/publish-k8s-schemas)(how to push)
- [bjw-s-labs/CRD-catalog](https://github.com/bjw-s-labs/CRD-catalog)
- [home-operations/k8s-schemas](https://github.com/home-operations/k8s-schemas)
- [sholdee/crd-schema-publisher](https://github.com/sholdee/crd-schema-publisher)

---

### License

See [LICENSE](https://github.com/soulwhisper/home-ops/blob/main/LICENSE)
