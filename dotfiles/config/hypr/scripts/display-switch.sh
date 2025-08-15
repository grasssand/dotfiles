#!/usr/bin/env bash
# Hyprland 启动时检测 HDMI-A-1 状态，并配置显示器

# 获取当前连接的显示器列表
CONNECTED=$(hyprctl monitors | grep HDMI-A-1)

if [[ -n "$CONNECTED" ]]; then
  # 若 HDMI-A-1 已连接，使用外接屏，并禁用内置屏
  hyprctl keyword monitor "eDP-1, disable"
  # hyprctl keyword monitor "HDMI-A-1, preferred, auto, 1"
# else
#   # 若 HDMI 未连接，则启用内置屏
#   hyprctl keyword monitor ", preferred, auto, 1"
fi
