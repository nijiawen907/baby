import torch

model = torch.load(r"D:\物联网2025\小程序\哭闹检测-小程序\backend\model\expression.pt", map_location=torch.device('cpu'))
model.eval()

dummy_input = torch.randn(1, 3, 640, 640)

torch.onnx.export(
    model,
    dummy_input,
    "expression.onnx",
    opset_version=11,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)
