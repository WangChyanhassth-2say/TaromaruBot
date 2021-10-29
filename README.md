# 太郎丸Bot / TaromaruBot

基于[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
和 [nonebot2](https://github.com/nonebot/nonebot2) 的原神QQ机器人  

## 部署步骤参考
1. 配置并运行 go-cqhttp

	可参考[go-cqhttp官方文档](https://docs.go-cqhttp.org/)

2. 安装 python3.7 或更高版本

4. pip安装所需环境
	```
	python3 -m pip install -r requirements.txt
	```
5. 安装chrome

	我安装的版本是Windows 95.0.4638.54（正式版本） （64 位）
	
	如果版本不同请自行下载对应版本的chromedriver并放于 src/data/artifact_analyse_data/ 目录下

6. (可选)修改 python 安装路径下
	Lib/site-packages/selenium/webdriver/common/service.py 文件, 
	改写 start() 下 creationflags 的值, 如下: 
	```
	cmd = [self.path]
	cmd.extend(self.command_line_args())
	self.process = subprocess.Popen(cmd, env=self.env,
					close_fds=system() != 'Windows',
					stdout=self.log_file,
					stderr=self.log_file,
					stdin=PIPE,
					creationflags=0x08000000)
	```
7. 运行 bot.py

	如需修改代码可参考 [nonebot2官方文档](https://v2.nonebot.dev/)
	
	
