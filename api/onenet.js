export const getEnvironmentData = async () => {
  try {
    const response = await uni.request({
      url: "http://iot-api.heclouds.com/datapoint/current-datapoints", // API接口地址
      method: 'GET',
      header: {
        authorization: "version=2018-10-31&res=products%2FYmNvcyL5e8%2Fdevices%2F1&et=1764873600&method=md5&sign=KbeGKr1j4ZQIQHzz8a6Rog%3D%3D"
      },
      data: {
        product_id: "YmNvcyL5e8", // 设备产品ID
        device_name: "1" // 设备名称
      }
    });

    // 检查返回的数据
    if (response.statusCode === 200) {
      console.log("环境数据：", response.data);
      // 处理返回的数据
      return response.data.data.devices[0];
    } else {
      console.error("获取环境数据失败:", response.statusCode);
    }
  } catch (error) {
    console.error("请求出错:", error);
  }
}


// 格式化日期为 yyyy-MM-ddTHH:mm:ss 格式
const formatDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
}

export const getHistoryData = async (timeRange) => {
  try {
    // 获取当前时间
    const currentTime = new Date();
    
    // 计算开始时间和结束时间
    let startTime, endTime;
    switch (timeRange) {
      case '24h':
        startTime = new Date(currentTime - 24 * 60 * 60 * 1000); // 24小时内
        endTime = currentTime;
        break;
      case '1w':
        startTime = new Date(currentTime - 7 * 24 * 60 * 60 * 1000); // 一周内
        endTime = currentTime;
        break;
      case '30d':
        startTime = new Date(currentTime - 30 * 24 * 60 * 60 * 1000); // 30天内
        endTime = currentTime;
        break;
      default:
        throw new Error("Unsupported time range");
    }

    //格式化时间为 yyyy-MM-ddTHH:mm:ss
    const startTimeStr = formatDate(startTime);
    const endTimeStr = formatDate(endTime);

    //打印一下计算出来的时间范围
    console.log('Start Time:', startTimeStr);
    console.log('End Time:', endTimeStr);

    // 发起请求获取历史数据
    const response = await uni.request({
      url: "http://iot-api.heclouds.com/datapoint/history-datapoints", // 使用历史数据接口
      method: "GET",
      header: {
        authorization: "version=2018-10-31&res=products%2FYmNvcyL5e8%2Fdevices%2F1&et=1764873600&method=md5&sign=KbeGKr1j4ZQIQHzz8a6Rog%3D%3D"
      },
      data: {
        product_id: "YmNvcyL5e8",  // 设备产品ID
        device_name: "1",         // 设备名称
        start: startTimeStr,      // 动态设置开始时间
        end: endTimeStr           // 动态设置结束时间
      }
    });
	// 检查返回的数据
	if (response.statusCode === 200) {
		console.log('环境历史数据:', response);
	  // 处理返回的数据
	  return response.data.data;
	} else {
		console.error("获取环境数据失败:", response.statusCode);
	}
  } catch (error) {
    console.error('获取历史数据失败:', error);
  }
};

