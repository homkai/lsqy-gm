# 后端装备图片上传、分析部分

- server整体基于django，第一次用django...
- 识别图片是 eqprecog/recog.py，基于OpenCV3

## 图片分析识别
现在的模型比较简陋，边缘检测-过滤-定位-切图与识别

欢迎PR

**Django需要python3，但是python3的OpenCV又比较难装，在Stack Overflow上总结出来，Windows、Ubuntu、Mac的OpenCV好装，其他的Linux发行版够呛，反正我用CentOS 7没搞定**