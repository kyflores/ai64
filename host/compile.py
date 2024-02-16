# SOC=am68pa TIDL_TOOLS_PATH=/home/kyle/Documents/ai64/host/edgeai-tidl-tools/tidl_tools/ LD_LIBRARY_PATH=$TIDL_TOOLS_PATH python compile.py

import onnx
import onnxruntime as ort
import os

tidl_tools_path = os.environ["TIDL_TOOLS_PATH"]
artifacts_folder = 'model-artifacts/'

tensor_bits = 8
debug_level = 0
max_num_subgraphs = 16
accuracy_level = 1
calibration_frames = 2
calibration_iterations = 5
output_feature_16bit_names_list = ""#"conv1_2, fire9/concat_1"
params_16bit_names_list = "" #"fire3/squeeze1x1_2"
mixed_precision_factor = -1
quantization_scale_type = 0
high_resolution_optimization = 0
pre_batchnorm_fold = 1
inference_mode = 0
num_cores = 1
ti_internal_nc_flag = 1601

data_convert = 3
SOC = os.environ["SOC"]
if (quantization_scale_type == 3):
    data_convert = 0

#set to default accuracy_level 1
activation_clipping = 1
weight_clipping = 1
bias_calibration = 1
channel_wise_quantization = 0


optional_options = {
    # "priority":0,
    #delay in ms
    # "max_pre_empt_delay":10,
    "platform":"J7",
    "version":"7.2",
    "tensor_bits":tensor_bits,
    "debug_level":debug_level,
    "max_num_subgraphs":max_num_subgraphs,
    "deny_list":"", #"MaxPool"
    "deny_list:layer_type":"",
    "deny_list:layer_name":"",
    "model_type":"od",#OD
    "accuracy_level":accuracy_level,
    "advanced_options:calibration_frames": calibration_frames,
    "advanced_options:calibration_iterations": calibration_iterations,
    "advanced_options:output_feature_16bit_names_list" : output_feature_16bit_names_list,
    "advanced_options:params_16bit_names_list" : params_16bit_names_list,
    "advanced_options:mixed_precision_factor" :  mixed_precision_factor,
    "advanced_options:quantization_scale_type": quantization_scale_type,
    #"object_detection:meta_layers_names_list" : meta_layers_names_list,  -- read from models_configs dictionary below
    #"object_detection:meta_arch_type" : meta_arch_type,                  -- read from models_configs dictionary below
    "advanced_options:high_resolution_optimization": high_resolution_optimization,
    "advanced_options:pre_batchnorm_fold" : pre_batchnorm_fold,
    "ti_internal_nc_flag" : ti_internal_nc_flag,
    # below options will be read only if accuracy_level = 9, else will be discarded.... for accuracy_level = 0/1, these are preset internally
    "advanced_options:activation_clipping" : activation_clipping,
    "advanced_options:weight_clipping" : weight_clipping,
    "advanced_options:bias_calibration" : bias_calibration,
    "advanced_options:add_data_convert_ops" : data_convert,
    "advanced_options:channel_wise_quantization" : channel_wise_quantization,
    # Advanced options for SOC 'am69a'
    "advanced_options:inference_mode" : inference_mode,
    "advanced_options:num_cores" : num_cores
}

required_options = {
    "tidl_tools_path":tidl_tools_path,
    "artifacts_folder":artifacts_folder
}
sess_options = ort.SessionOptions()
sess_options.log_severity_level=3

delegate_options = {}
delegate_options.update(required_options)
delegate_options.update(optional_options)

# Compiling Megvii YOLOX, copy some options from TI configs
od_type = "SSD"
model_path = "/home/kyle/Documents/ai64/host/yolox-s-ti-lite_39p1_57p9.onnx"
meta_layers_names_list = "/home/kyle/Documents/ai64/host/yolox_s_ti_lite_metaarch.prototxt"
meta_arch_type = 6


delegate_options['object_detection:meta_layers_names_list'] = meta_layers_names_list
delegate_options['object_detection:meta_arch_type'] = meta_arch_type

os.makedirs(delegate_options['artifacts_folder'], exist_ok=True)
for root, dirs, files in os.walk(delegate_options['artifacts_folder'], topdown=False):
    [os.remove(os.path.join(root, f)) for f in files]
    [os.rmdir(os.path.join(root, d)) for d in dirs]

onnx.shape_inference.infer_shapes_path(model_path, model_path)

EP_list = ['TIDLCompilationProvider','CPUExecutionProvider']
sess = ort.InferenceSession(
    model_path,
    providers=EP_list,
    provider_options=[delegate_options, {}],
    sess_options=sess_options)
