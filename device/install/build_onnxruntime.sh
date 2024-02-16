#!/bin/bash
# This cannot be reasonably compiled on the AI64 - there simply isn't enough RAM.
# Instead I build this in a container, and transfer the whl to the AI64.

# Maybe also gcc=10.3.0 gxx=10.3.0
micromamba install cmake numpy packaging -c conda-forge

git clone https://github.com/TexasInstruments/onnxruntime.git --branch tidl-1.14

./build.sh \
    --config RelWithDebInfo \
    --build_shared_lib \
    --parallel \
    --compile_no_warning_as_error \
    --skip_submodule_sync \
    --use_tidl \
    --skip_tests \
    --build_wheel

# Ends up in container/root/onnxruntime/build/Linux/RelWithDebInfo/dist/onnxruntime_tidl-1.14.0-cp310-cp310-linux_aarch64.whl
