#!/usr/bin/env bash

# 简单电源菜单（使用 wofi 或 rofi）
CHOICE=$(printf "🔒 锁屏\n🔁 重启\n⏻ 关机\n🚪 登出" | rofi -dmenu -theme ~/.config/rofi/confirm.rasi)

case "$CHOICE" in
  "🔒 锁屏") loginctl lock-session ;;
  "🔁 重启") systemctl reboot ;;
  "⏻ 关机") systemctl poweroff ;;
  "🚪 登出") loginctl terminate-user "$USER" ;;
esac
