import onnxruntime as ort
import numpy as np

sess = ort.InferenceSession(r"D:\物联网2025\小程序\哭闹检测-小程序\backend\model\expression.onnx")
input_name = sess.get_inputs()[0].name

# 生成随机输入，3通道，640x640
input_data = np.random.randn(1, 3, 640, 640).astype(np.float32)

outputs = sess.run(None, {input_name: input_data})
print(outputs)
