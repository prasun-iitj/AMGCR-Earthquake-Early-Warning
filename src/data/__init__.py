"""Paper-traceable data contracts for the EarthESND reproduction work.

The module structure is a project assumption documented in
``docs/EARTHESND_IMPLEMENTATION_SPEC_V1.md``.
"""

from src.data.manifest import DatasetManifest, ManifestRecord, load_manifest, validate_manifest
from src.data.splits import assign_stratified_splits

__all__ = [
    "DatasetManifest",
    "ManifestRecord",
    "assign_stratified_splits",
    "load_manifest",
    "validate_manifest",
]
