# 新手入门/实现HelloWord

> 本分类共 1 篇文章

---


## 制作HellowWorld工程

> 文档路径: 新手入门 > 实现HelloWord > 制作HellowWorld工程

**涉及API:** `Add`, `Asset`, `GetReplicatedProperties`, `HasAuthority`, `MyHelloWorld`, `OnRep_TestValue`, `OnRep_变量名`, `ReceiveBeginPlay`, `ReceiveEndPlay`, `ReceiveTick`, `ScriptGameplayStatics.SpawnActor`, `TestValue`, `UE.LoadClass`, `UGCGameMode`, `UGCMapInfoLib`, `UGCMapInfoLib.GetRootLongPackagePath`, `VSCode`

# 制作HellowWorld工程

附件工程：<a href="https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/HelloWorld.7z">HelloWorld.7z</a>

<br>

## 新建蓝图，绑定Lua脚本

### 1. 继承Actor新建一个蓝图，改名为`MyHelloWorld`
新增一个Cube，让Actor方便在场景中观察

![企业微信截图_16866400992201.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16866400992201.png)

### 2. 点击Lua自动创建蓝图对应的Lua文件
如果安装并配置好了`VSCode`，新建的Lua文件会自动在VSCode中打开

<br>

## 基础函数讲解

<details open>
<summary> <font face="楷体">示例：自动创建的Lua</font> </summary>

```lua
local MyHelloWorld = {}; 
--近似构造函数，客户端，战斗服务器运行
-- function MyHelloWorld:ReceiveBeginPlay()
-- end
	
--每帧都执行，客户端，战斗服务器运行
--DeltaTime为上帧到本帧执行的时间
-- function MyHelloWorld:ReceiveTick(DeltaTime)
-- end
	
--近似析构函数，客户端，战斗服务器运行
-- function MyHelloWorld:ReceiveEndPlay()
-- end
	
return MyHelloWorld;
```

</details>

<br>

## 让蓝图出现在场景中

### 两种形式

#### 1. 直接拖拽蓝图放置在场景中

![企业微信截图_16932919953210.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/KBxLc%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16932919953210.png)

#### 2. 使用代码，运行时动态刷新

<details open>
<summary> <font face="楷体">示例：运行时动态刷出Actor</font> </summary>

```lua
function UGCGameMode:ReceiveBeginPlay()
		--仅在服务器运行
		if self:HasAuthority() then 
        --根据路径加载类
        local Path_Hello = UGCMapInfoLib.GetRootLongPackagePath().."Asset/Blueprint/MyHelloWorld.MyHelloWorld_C"
        local Class_Hello = UE.LoadClass(Path_Hello)

        --刷出Actor
        local BP_Hello = ScriptGameplayStatics.SpawnActor(self, Class_Hello, 
        {X = 21520, Y = 28980, Z = 150},    --坐标
        {Roll = 0, Pitch = 0, Yaw = 0},     --旋转
        {X = 1, Y = 1, Z = 1})              --缩放
    end
end
```

</details>

下图中可以看出，运行前，场景中仅包含直接放置的方块，运行后，场景中一共包含两个方块

![企业微信截图_16866401452513.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16866401452513.png)

<br>

## 打印HelloWorld

### 1. 区分战斗服务器和客户端运行的代码，并分别打印日志

<details open>
<summary> <font face="楷体">示例：战斗服务器和客户端分别打印日志</font> </summary>

```lua
local MyHelloWorld = 
{
    TestValue = 0;
};

function MyHelloWorld:ReceiveBeginPlay()
    if self:HasAuthority() then
        --仅在战斗服务器运行
        self.TestValue = 1
        print("Log HelloWorld: ReceiveBeginPlay Server:"..self.TestValue)

        self.Box.OnComponentBeginOverlap:Add(self.OnBeginOverlap, self);
    else
        --仅在客户端运行
        print("Log HelloWorld: ReceiveBeginPlay Client:"..self.TestValue)
    end
end
```

</details>

`self:HasAuthority()`为`true`时，代表当前代码逻辑运行在战斗服务器，为`false`时则代表代码逻辑运行在客户端，由于此时`TestValue`仅在战斗服务器单独设置值为1，运行查看日志，可以看到，服务器日志显示`TestValue`的值为1，而客户端日志的值为0。

![企业微信截图_16866401552934.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16866401552934.png)

### 2. 添加变量同步，让`TestValue`同步到客户端

<details open>
<summary> <font face="楷体">示例：设置TestValue为同步变量</font> </summary>

```lua
--标记属性为同步
function MyHelloWorld:GetReplicatedProperties()
    return "TestValue"
end

--战斗服务器修改后，自动同步到客户端
--函数名规则OnRep_变量名
function MyHelloWorld:OnRep_TestValue()
    print("Log HelloWorld:"..self.TestValue)
end
```

</details>

- 把需要设置成同步的变量，添加到`GetReplicatedProperties`函数中返回
- 客户端添加名为`OnRep_变量名`的函数，战斗服务器设置变量的值时，客户端的变量会自动同步并调用名为`OnRep_变量名`的函数
- `GetReplicatedProperties`中可以返回多个变量，用逗号分隔

<details open>
<summary> <font face="楷体">示例：设置多个同步变量</font> </summary>

```lua
--返回多个变量
function MyHelloWorld:GetReplicatedProperties()
    return "TestValue","NewValue"
end
```

</details>

查看日志，客户端会在战斗服务器设置变量后，自动同步，并调用对应的OnRep函数

![企业微信截图_16866401917346.png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_16866401917346.png)



---
