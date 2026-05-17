# Reference: adapters

The adapter Protocol is the only abstraction surface in Phase 1a. Each adapter
declares a `capabilities: frozenset[Capability]` and is responsible for
satisfying any `requires(...)` call from a functor.

## Built-in adapters

### `hf-transformer`

HuggingFace `AutoModel` wrapper.

| Capability | Supported |
|---|---|
| HIDDEN_STATES | yes |
| ATTENTION | yes |
| SAE_FEATURES | yes (when `sae_release` is supplied) |
| VELOCITY_FIELD | no |
| SSM_STATES | no |
| LOSS_LANDSCAPE | yes |

### `mamba`

Stub for Phase 1b. Discoverable via `cartograph list-adapters`.

| Capability | Supported |
|---|---|
| HIDDEN_STATES | yes (Phase 1b) |
| ATTENTION | **by design: no** (raises `MissingCapabilityError`) |
| SSM_STATES | yes (Phase 1b) |

## Adding your own adapter

```python
from cartograph.core.adapter import Capability
from cartograph.core.registry import register_adapter


@register_adapter("my-llm")
class MyAdapter:
    name = "my-llm"
    capabilities = frozenset({Capability.HIDDEN_STATES})
    ...
```
