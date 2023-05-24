# A simple pixiv bookmark downloads

一个简单的 Python 脚本，利用 RSSHub 下载 Pixiv 收藏夹。下载过的历史记录会保存在文本文件内，用来避免重复下载。

## Use

先使用 Pip 安装依赖：
```bash
 pip install -r requirements.txt
 ```

 然后运行：
 ```bash
 python main.py
 ```

 初次运行会提示输入设置，然后生成 Settings.cfg 配置文件：

 1. **Pixiv numerical ID** 在 Pixiv 打开个人主页，URL 末尾的数字
 2. **Download folder** 保存下载图片的路径，默认为 `./downloaded_images`
 3. **Download history** 保存下载历史的文本文件，默认为 `./downloaded_images.txt`