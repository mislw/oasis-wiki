# 进阶内容/UI系统/和平控件查询

> 本分类共 2 篇文章

---


## 和平主界面控件

> 文档路径: 进阶内容 > UI系统 > 和平控件查询 > 和平主界面控件

# 和平主界面控件查询

对于和平主界面的常用控件设置，例如开火、站/蹲/趴、状态栏等，请优先采用 [WidgetLayout](https://developer.gp.qq.com/wikieditor/#/catalog/20019) 方案处理。

![1.74143083[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/1.74143083%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 装载子弹 | MainControlPanelTochButton.ShootingUIPanel.CustomReload | 否 |
| 2 | 蹲 | MainControlPanelTochButton.ShootingUIPanel.CustomCrouch | 否 |
| 3 | 卧倒 | MainControlPanelTochButton.ShootingUIPanel.CustomProne | 否 |
| 4 | 右键开火按钮 | MainControlPanelTochButton.ShootingUIPanel.CustomFireBtnR | 否 |
| 5 | 跳跃按钮 | MainControlPanelTochButton.ShootingUIPanel.CustomJumpBtn | 否 |
| 6 | 侧面镜 | MainControlPanelTochButton.ShootingUIPanel.CustomShootRed | 否 |
| 7 | 开镜 | MainControlPanelTochButton.ShootingUIPanel.CustomShootAim | 否 |
| 8 | 切换倍镜 | MainControlPanelTochButton.MainControlBaseUI.ChangeSight_UIBP.CanvasPanel_Sight | 否 |
| 9 | 下车 | VehileControlPanel.BtnLeaveVehicle | 是 |

![2.5fb86a67[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/2.5fb86a67%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 商店 | MainControlPanelTochButton.MainControlBaseUI.CarlaGold_BackpackSocket | 否 |
| 2 | 载具皮肤 | MainControlPanelTochButton.MainControlBaseUI.CanvasPanel_VehicleSkinBtn | 否 |
| 3 | 喷漆面板入口 | MainControlPanelTochButton.MainControlBaseUI.QuickDecal_BP.Emote_SwimingControl_QuickDecal_BP | 否 |
| 4 | 动作 |MainControlPanelTochButton.MainControlBaseUI.QuickExpressionUIBP.lmage_Emote_SettingControl| 否 |
| 5 | 设置 | MainControlPanelTochButton.MainControlBaseUI.CanvasEnterSetting | 否 |
| 6 | 喇叭 | MainControlPanelTochButton.MainControlBaseUI.Canvas_Speaker | 否 |
| 7 | 麦克风 | MainControlPanelTochButton.MainControlBaseUI.Canvas_Microphone | 否 |
| 8 | 疾跑状态 | MainControlPanelTochButton.MainControlBaseUI.CanvasPanel_RunState | 否 |
| 9 | 右上角小地图 | MainControlPanelTochButton.MainControlBaseUI.CanvasPanel_MiniMapAndSetting | 否 |
| 10 | 万能标记 | MainControlPanelTochButton.MainControlBaseU.QuickSign_UIBP.QuickSignCircle_UIBP | 否 |
| 11 | 聊天入口和面板 | MainControlPanelTochButton.MainControlBaseUI.ChatAndChatPanelCanvas | 否 |

![3.74bc62eb[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/3.74bc62eb%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 打开战利品（有背包） | ShortcutMenu_BP.WidgetSwitcher_1 | 是 |
| 2 | 打开战利品（无背包） | ShortcutMenu_BP.WidgetSwitcher_0 | 是 |
| 3 | 视角移动按钮 | MainControlPanelTochButton.MainControlBaseUI.CanvasPanel_FreeCamera | 否 |
| 4 | 进入车辆驾驶按钮 | BasicSkillsMenu_BP.BtnDriverEnter | 是 |
| 5 | 乘坐车辆按钮 | BasicSkillsMenu_BP.BtnPassengerEnter | 是 |
| 6 | 开关门按钮 | BasicSkillsMenu_BP.GridPanel_Door | 是 |

![4.bf11231a[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/4.bf11231a%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 使用医疗品 | MainControlPanelTochButton.ShootingUIPanel.ConsumeListPanel | 否 |
| 2 | 药包列表 | MainControlPanelTochButton.ShootingUIPanel.ConsumeListPanel | 否 |
| 3 | 切换开火模式 | MainControlPanelTochButton.ShootingUIPanel.SwitchWeaponSlot_Mode2.GridPanel_FireMode | 否 |
| 4 | 主武器1 | MainControlPanelTochButton.ShootingUIPanel.SwitchWeaponSlot_Mode2.Image_Selected | 否 |
| 5 | 主武器2 | MainControlPanelTochButton.ShootingUIPanel.SwitchWeaponSlot_Mode2.Image_Selected | 否 |
| 6 | 切换开火模式 | MainControlPanelTochButton.ShootingUIPanel.SwitchWeaponSlot_Mode2.GridPanel_FireMode | 否 |
| 7 | 手枪槽 | MainControlPanelTochButton.ShootingUIPanel.SwitchWeaponSlot_Mode2.MultiLayer_Pistol | 否 |
| 8 | 投掷物 | MainControlPanelTochButton.ShootingUIPanel.GrenadeList.GrenadeListPanel | 否 |
| 9 | 投掷物列表 | MainControlPanelTochButton.ShootingUIPanel.GrenadeListPanel | 否 |
| 10 | 信号区外提示条 | SignalReceivingAreaTIPS_UIBP.Boder_EnterTips | 是 |
| 11 | 信号区倒计时 | SignalReceivingAreaTIPS_UIBP.CanvasPanel_Time | 是 |
| 12 | 救援 | BasicSkillsMenu_BP.GridPanel_Save | 是 |
| 13 | 人物状态栏 | PlayerInfoPanel.VerticalLifeInfo | 是 |

![5.082a5063[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/5.082a5063%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 快速疾跑 | MainControlPanelTochButton.MainControlBaseUI.CanvasPanel_ArrowVfxGroup | 否 |
| 2 | 左探头 | MainControlPanelTochButton.ShootingUIPanel.CustomLeanL | 否 |
| 3 | 获胜提醒 | IngameVictoryTips2_UIBP.CanvasPanel_Tips2 | 是 |
| 4 | 右探头 | MainControlPanelTochButton.ShootingUIPanel.CustomLeanR | 否 |
| 5 | 左键开火按钮 | MainControlPanelTochButton.ShootingUIPanel.CustomFireBtnL | 否 |
| 6 | 摇杆 | 暂无 | 否 |
| 7 | 背包界面入口 | MainControlPanelTochButton.MainControlBaseUI.CanvasPanel_BackpackPanel | 否 |
| 8 | 人称切换按钮 | MainControlPanelTochButton.ShootingUIPanel.CustomSwitchFPP | 否 |
| 9 | 取消投掷 | MainControlPanelTochButton.ShootingUIPanel.CustomCancelThrow | 否 |
| 10 | 组队和队友信息相关 | Ingame_TeamPanel_BP.Canvas_Border_Team | 是 |
| 11 | 倍镜调距离 | MainControlPanelTochButton.ShootingUIPanel.CustomX8Zoom | 否 |

![61.1858f5d8[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/61.1858f5d8%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
|1 | 快速投掷 | RingThrowButUI.CanvasPanel_0 | 是 |

![7.8af1b2c8[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/7.8af1b2c8%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 车辆加速 | VehileControlPanel.VehileControlPanel.CustomizeCanvasPanel_V_67 | 是 |
| 2 | 急刹 |VehileControlPanel.VehileControlPanel.CustomizeCanvasPanel_V_83 | 是 |
| 3 | 下车 |VehileControlPanel.VehileControlPanel.Border_Opacity | 是 |
| 4 | 喇叭 | VehileControlPanel.VehileControlPanel.CanvasPanel_CarSpeaker | 是 |

![91.dbc9e7f5[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/91.dbc9e7f5%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 侧窗开枪 | VehileControlPanel.CanvasPanel_ShootingOnTheVehile | 是 |
| 2 | 换位 | VehileControlPanel.CustomizeCanvasPanel_BP_V_62 | 是 |
| 2* | 换位（飞行载具） | VehileControlPanel.CanvasPanel_HelicopterUI | 是 |

![8.d656249a[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/8.d656249a%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 摩托车重心控制 | VehileControlPanel.CustomizeCanvasPanel_BP_V_96 | 是 |

![92.450c3548[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/92.450c3548%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 快捷换装 | SuitBase_UIBP.CanvasPanel_BackPack_ChangeSuit | 是 |

![93.a9e05913[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/93.a9e05913%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 聊天 | LobbyChat_BP | 是 |



---


## 和平全局观战界面控件

> 文档路径: 进阶内容 > UI系统 > 和平控件查询 > 和平全局观战界面控件

#  和平全局观战界面控件查询

![9.3d99885f[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/9.3d99885f%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-玩家表 | OBUI_UIBP.OB_MapPlayerList.CanvasPanel_ListTitle | 否 |
| 2 | 观战-全局键 | OBUI_UIBP.OB_MapPlayerList.CanvasPanel_ButTop | 否 |
| 3 | 观战-附近键 | OBUI_UIBP.OB_MapPlayerList.CanvasPanel_ButTop | 否 |
| 4 | 观战-列表 | OBUI_UIBP.OB_MapPlayerList.NewButton_ListPage | 否 |
| 5 | 观战-自由镜头 | OBUI_UIBP.CanvasPanel_FreeCam | 否 |
| 6 | 观战-切换玩家 | OBUI_UIBP.CanvasPanel_CrtPlayer | 否 |
| 7 | 观战-隐藏UI | OBUI_UIBP.Border_SetColor_EnterNoUI | 否 |

![10.55324607[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/10.55324607%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-航段表 | OBUI_UIBP.OB_MapPlayerList.OB_RouteMain_UIBP | 否 |
| 2 | 观战-航段键 | OBUI_UIBP.OB_MapPlayerList.NewButton_airline | 否 |

![11.aa66f882[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/11.aa66f882%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-导播键 | OBUI_UIBP.OB_MapPlayerList.NewButton_Director | 否 |
| 2 | 观战-队伍距离预警 | OBUI_UIBP.OB_MapPlayerList.CanvasPanel_MC | 否 |
| 3 | 观战-导播队伍界面 | OBUI_UIBP.OB_MapPlayerList.CanvasPanel_MCList | 否 |

![12.5067ed0e[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/12.5067ed0e%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-关闭地图 | OBUI_UIBP.EntireMap_OBmode.Button_HideMap | 否 |
| 2 | 观战-放大地图 | OBUI_UIBP.EntireMap_OBmode.Button_ZoomIn | 否 |
| 3 | 观战-放缩地图条 | OBUI_UIBP.EntireMap_OBmode.Slider_MapZoom | 否 |
| 4 | 观战-缩小地图 | OBUI_UIBP.EntireMap_OBmode.Button_ZoomOut | 否 |
| 5 | 观战-字号放大 | OBUI_UIBP.EntireMap_OBmode.Button_FontSizeAdd | 否 |
| 6 | 观战-字号减小 | OBUI_UIBP.EntireMap_OBmode.Button_FontSizeSub | 否 |
| 7 | 观战-地图锁定 | OBUI_UIBP.EntireMap_OBmode.Button_SelfLock | 否 |
| 8 | 观战-地图路线 | OBUI_UIBP.EntireMap_OBmode.Button_path | 否 |

![13.1e51a1a2[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/13.1e51a1a2%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-自由镜头 | OBUI_UIBP.CanvasPanel_FreeCam | 否 |
| 2 | 观战-镜头向上 | OBUI_UIBP.Button_UP | 否 |
| 3 | 观战-镜头向下 | OBUI_UIBP.Button_Down | 否 |

![14.9365bbda[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/14.9365bbda%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
|1 | 观战-隐藏列表 | OBUI_UIBP.CanvasPanel_HiddenList | 否 |
| 2 | 观战-关闭隐藏菜单 | OBUI_UIBP.Border_SetColor | 否 |
| 3 | 观战-玩家信息 | OBUI_UIBP.OB_PlayerInfoPanel_BP | 否 |
| 4 | 观战-队伍信息 | OBUI_UIBP.CanvasPanel_TeamInfo | 否 |
| 5 | 观战-全队淘汰数 | OBUI_UIBP.OB_TeammateList.WidgetSwitcher_TeamLOGO | 否 |
| 6 | 观战-队伍剩余玩家 | OBUI_UIBP.OB_TeamLeftHPItem_UIBP | 否 |

![15.16480f24[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/15.16480f24%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-队伍界面 | OBUI_UIBP.OB_TabListGroup_UIBP | 否 |
| 2 | 观战-关闭页面 | OBUI_UIBP.OB_TabList_UIBP.Button_CloseUI | 否 |

![16.cd1ed3aa[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/16.cd1ed3aa%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-本局数据 | OBUI_UIBP.ResultOBlistitem_UIBP | 否 |
| 2 | 观战-继续 | OBUI_UIBP.ResultsOB_UIBP.Button_ShareGameData | 否 |

![17.309dda71[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/17.309dda71%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
|1 | 观战-明星玩家数据 | OBUI_UIBP.ResultsOB_ResultTitle_UIBP.ResultsOB_ResultTitle_Item_UIBP | 否 |
| 2| 观战-退出 | OBUI_UIBP.ResultsOB_ResultTitle_UIBP.Button_out | 否 |

![18.b4523e74[1].png](https://cgugc-video-test-1258633575.cos.ap-shanghai.myqcloud.com/wiki_picture/18.b4523e74%5B1%5D.png)

| 序号| 名称 | 路径 | 是否动态加载 |
| ------ | ------ | ------ | ------ |
| 1 | 观战-拾取道具栏 | MainControlPanelTochButton.PickUpListPanel_BP.GridPanel_PickUpList | 否 |
| 2 | 观战-空投 | OBUI_UIBP.DropBox_BP | 否 |



---
