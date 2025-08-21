# https://github.com/CachyOS/cachyos-fish-config/blob/main/cachyos-config.fish

set -gx LANG zh_CN.UTF-8
set -gx LANGUAGE zh_CN
set -gx DOTDROP_CONFIG $HOME/.dotfiles/config.yaml

# Format man pages
set -gx MANROFFOPT "-c"
set -gx MANPAGER "sh -c 'col -bx | bat -l man -p --theme=\"OneHalfDark\"'"
if not type -q bat
    set -gx MANPAGER "less -R"
end

# Plugins settings
set -U __done_min_cmd_duration 10000
set -U __done_notification_urgency_level low

function history
    builtin history --show-time='%F %T '
end

function backup --argument filename
    cp $filename $filename.bak
end

# Enhanced Copy: 安全递归、保留属性、智能处理目录末尾 /
function copy
    # 参数不足直接提示
    if test (count $argv) -lt 2
        echo "Usage: copy <source...> <dest>"
        return 1
    end

    # 取最后一个参数作为目标，其余为源
    set -l dest $argv[-1]
    set -l sources $argv[1..-2]

    set -l opts "-a"  # 保留权限/时间戳/符号链接

    # 检查是否为目录到目录的单源模式
    if test (count $sources) = 1; and test -d "$sources[1]"; and test -d "$dest"
        set sources (string trim -r -c '/' -- $sources[1])
    end

    # 防御：文件名可能以 - 开头 → 加 --
    command cp $opts -- $sources $dest
end

# 自动根据后缀选择解压器
function untar
    if test (count $argv) -lt 1
        echo "用法: untar <文件名>"
        return 1
    end

    switch $argv[1]
        case '*.tar.zst'
            tar -I zstd -xf $argv[1]
        case '*.tar.xz'
            tar -Jxf $argv[1]
        case '*.tar.gz'
            tar -zxf $argv[1]
        case '*.tar'
            tar -xf $argv[1]
        case '*'
            echo "❌ 不支持的格式: $argv[1]"
            return 1
    end
end

# Init zoxide
zoxide init fish | source

## Useful aliases
# Replace ls with eza
alias ls='eza -al --color=always --group-directories-first --icons' # preferred listing
alias la='eza -a --color=always --group-directories-first --icons'  # all files and dirs
alias ll='eza -l --color=always --group-directories-first --icons'  # long format
alias lt='eza -aT --color=always --group-directories-first --icons' # tree listing
alias l.="eza -a | grep -e '^\.'"                                     # show only dotfiles
alias l='eza -al --color=always --group-directories-first --icons' # preferred listing

# Common use
alias grubup="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias fixpacman="sudo rm /var/lib/pacman/db.lck"
alias tarnow='tar -I "zstd -T0 -6" -cf'
alias wget='wget -c'
alias psmem='ps auxf | sort -nr -k 4'
alias psmem10='ps auxf | sort -nr -k 4 | head -10'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias ......='cd ../../../../..'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias hw='hwinfo --short'                                   # Hardware Info
alias big="expac -H M '%m\t%n' | sort -h | nl"              # Sort installed packages according to size in MB
alias gitpkg='pacman -Q | grep -i "\-git" | wc -l'          # List amount of -git packages
alias update='sudo cachyos-rate-mirrors && sudo pacman -Syu'

# Get fastest mirrors
alias mirror="sudo cachyos-rate-mirrors"

# Cleanup orphaned packages
alias cleanup='sudo pacman -Rns (pacman -Qtdq)'

# Get the error messages from journalctl
alias jctl="journalctl -p 3 -xb"

# Recent installed packages
alias rip="expac --timefmt='%Y-%m-%d %T' '%l\t%n %v' | sort | tail -200 | nl"

# Other alias
alias cat='bat --paging=never'
alias fud='fisher update'
alias x='extract'
