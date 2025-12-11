#!/usr/bin/env bash
# Hyprland 启动时检测 HDMI-A-1 状态，并配置显示器

# 获取当前连接的显示器列表
CONNECTED=$(hyprctl monitors | grep "Monitor" | wc -l)

if [ $CONNECTED -gt 1 ]; then
  hyprctl keyword monitor "eDP-1, disable"
  # hyprctl dispatch moveworkspacetomonitor 1 HDMI-A-1
else
  hyprctl keyword monitor ", preferred, auto, 1"
fi
