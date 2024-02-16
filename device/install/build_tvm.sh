# https://software-dl.ti.com/codegen/docs/tvm/tvm_tidl_users_guide/building.html#tvm-compiler-and-runtime-for-x86-64

git clone https://github.com/TexasInstruments/tvm --branch tidl-j7
git clone https://github.com/TexasInstruments/neo-ai-dlr.git --branch tidl-j7

# USE_TIDL_RT_PATH?
# /usr/include/processor_sdk on the deb image

mkdir build
cd build
cmake .. -DUSE_TIDL=ON -DUSETIDL_RT_PATH=/usr/include/processor_sdk -DDLR_BUILD_TESTS=OFF
