# Building conda packages

To build conda packages you must first produce wheels for the project, see [this readme](../pip/README.md) for more details on building `TorchServe` wheel.

After producing wheels use the following command to build conda packages:

```
TORCHSERVE_WHEEL=/path/to/torchserve.whl TORCH_MODEL_ARCHIVER_WHEEL=/path/to/torch_model_archiver_wheel ./build_packages.sh
```

Produced conda packages are then stored in the `output` directory
